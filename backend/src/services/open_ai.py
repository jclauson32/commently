import json
import os
from typing import List

from openai import OpenAI

from src.models.contract import BatchRatingResponse, PromptConfig, RatingInput, RatingOutput
from src.services.prompt_manager import PromptManager
from src.services.scrape_creators import CommentsResponse


class OpenAIRatingClient:
    """Client for batch-processing Instagram video comment ratings via OpenAI."""

    PROMPT_NAME = "instagram_comment_rater"
    PROMPT_VERSION = "v1"

    def __init__(self, api_key: str | None = None, prompt_config: PromptConfig | None = None):
        self.client = OpenAI(api_key=api_key or os.environ.get("OPENAI_API_KEY"))
        self.prompt_manager = PromptManager()
        self.prompt_config = prompt_config or self.prompt_manager.load_prompt_config(
            self.PROMPT_NAME, self.PROMPT_VERSION
        )
        self.model = "gpt-4o-mini"

    def rate_comment(self, comment_text: str) -> RatingOutput:
        """Rate a single comment using the versioned prompt contract."""
        rating_input = RatingInput(text=comment_text)
        messages = self.prompt_manager.get_openai_messages(
            self.prompt_config,
            json.dumps([{"id": "single", "text": rating_input.text}]),
        )

        completion = self.client.beta.chat.completions.parse(
            model=self.model,
            messages=messages,
            response_format=BatchRatingResponse,
        )

        batch_result = completion.choices[0].message.parsed
        if not batch_result.ratings:
            raise ValueError("Model returned no ratings for the comment.")

        first_rating = batch_result.ratings[0]
        return RatingOutput(
            category=first_rating.category,
            summary=first_rating.summary,
            positivity_score=first_rating.positivity_score,
            bot_score=first_rating.bot_score,
        )

    def rate_comments_batch(
        self, responses: List[CommentsResponse], chunk_size: int = 100
    ) -> BatchRatingResponse:
        """Rate Instagram video comments in batches using the versioned prompt."""
        all_comments = []
        for response in responses:
            all_comments.extend(response.comments)

        if not all_comments:
            return BatchRatingResponse(total_processed=0, ratings=[])

        lean_payload = [{"id": c.id, "text": c.text} for c in all_comments if c.text]

        master_ratings = []
        total_processed_count = 0

        for i in range(0, len(lean_payload), chunk_size):
            chunk = lean_payload[i : i + chunk_size]

            try:
                messages = self.prompt_manager.get_openai_messages(
                    self.prompt_config,
                    json.dumps(chunk),
                )

                completion = self.client.beta.chat.completions.parse(
                    model=self.model,
                    messages=messages,
                    response_format=BatchRatingResponse,
                )

                chunk_result = completion.choices[0].message.parsed
                master_ratings.extend(chunk_result.ratings)
                total_processed_count += chunk_result.total_processed

                print(f"Processed chunk: {min(i + chunk_size, len(lean_payload))}/{len(lean_payload)}")

            except Exception as e:
                print(f"Failed to process chunk starting at index {i}: {e}")
                raise

        return BatchRatingResponse(
            total_processed=total_processed_count,
            ratings=master_ratings,
        )
