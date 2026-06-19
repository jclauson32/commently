import json
import os
import pytest

from src.open_ai import OpenAIRatingClient
from src.scrape_creators import CommentsResponse, Comment
from src.contract import BatchRatingResponse, CommentRating
from pathlib import Path

def test_llm_batch_benchmark():
    # Load the benchmark data
    current_dir = Path(__file__).parent

    file_path = current_dir / "benchmark_data.json"

    with open(file_path, "r") as f:
        dataset = json.load(f)

    # Create a fast lookup dictionary for our ground truth
    expected_lookup = {
        item["id"]: {
            "positivity": item["expected_positivity"],
            "bot_score": item["expected_bot_score"]
        }
        for item in dataset
    }

    real_comments = [
        Comment.model_construct(id=item["id"], text=item["comment"]) 
        for item in dataset
    ]
    real_payload = [CommentsResponse.model_construct(comments=real_comments)]

    rater = OpenAIRatingClient() 

    batch_result = rater.rate_comments_batch(responses=real_payload, chunk_size=50)


    assert len(batch_result.ratings) == len(dataset), "LLM did not return ratings for all comments!"

    positivity_error_margin = 0.0
    bot_error_margin = 0.0
    total_cases = len(batch_result.ratings)

    for rating in batch_result.ratings:
        expected = expected_lookup[rating.comment_id]
        
        # Pydantic guarantees these are integers as defined in your Field constraints
        positivity_error_margin += abs(rating.positivity_score - expected["positivity"])
        bot_error_margin += abs(rating.bot_score - expected["bot_score"])

    # variance metrics
    avg_positivity_error = positivity_error_margin / total_cases
    avg_bot_error = bot_error_margin / total_cases

    print(f" avg positivity error: {avg_positivity_error}, avg bot error: {avg_bot_error}")
    # write metrics to GitHub Actions Summary UI
    if "GITHUB_STEP_SUMMARY" in os.environ:
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a") as summary_file:
            summary_file.write("### Batched LLM Benchmark Results\n")
            summary_file.write(f"- **Total Processed:** {batch_result.total_processed}\n")
            summary_file.write(f"- **Avg Positivity Variance:** ±{avg_positivity_error:.1f} points\n")
            summary_file.write(f"- **Avg Bot Scoring Variance:** ±{avg_bot_error:.1f} points\n")

    # Pipeline Gates
    assert avg_positivity_error < 3.0, f"Regression: Positivity grading off by ±{avg_positivity_error:.1f}"
    assert avg_bot_error < 3.0, f"Regression: Bot scoring off by ±{avg_bot_error:.1f}"