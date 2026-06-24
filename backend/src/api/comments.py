import os
from fastapi import APIRouter, HTTPException, Request
from src.models.requests import RateCommentsRequest
from src.services.open_ai import OpenAIRatingClient
from src.services.scrape_creators import ScrapeCreatorClient

router = APIRouter()

try:
    scraper = ScrapeCreatorClient(
        provider="instagram",
        api_key=os.environ["SCRAPE_CREATORS_API_KEY"],
    )
    ai_client = OpenAIRatingClient(api_key=os.environ["OPENAI_API_KEY"])
except KeyError as e:
    raise RuntimeError(f"Missing required environment variable: {e}")


@router.post("/rate-comments")
async def rate_comments(payload: RateCommentsRequest, request: Request) -> dict:
    """
    Fetches and evaluates the sentiment and authenticity-likelihood of comments on an Instagram post.

    This endpoint accepts a valid Instagram post URL, retrieves the first page of comments
    via the scraper client, and processes them through the OpenAI rating client to evaluate
    positivity, categorization, and authenticity probability.

    Args:
        payload (RateCommentsRequest): The request payload containing the target URL.
            - url (HttpUrl): A fully validated URL string pointing to the Instagram post.
        request (Request): The raw FastAPI HTTP request object used to access
            globally shared application state clients.
    Returns:
        dict: A structured payload detailing the evaluation results.
            - status (str): Indicates the success of the operation (e.g., "success").
            - message (str): Human-readable summary of the batch processing.
            - total_processed (int): The exact count of comments evaluated.
            - data (list[dict]): A collection of dictionaries containing individual comment ratings:
                - comment_id (str): The unique ID of the scraped comment.
                - category (str): The AI-assigned thematic category.
                - positivity_score (int): A score from 0-10 rating the comment's positivity.
                - authenticity_score (int): A score from 0-10 rating the likelihood of it being a authenticity.
                - summary (str): A concise AI-generated summary of the comment's text.

    Raises:
        HTTPException: Raises a 500 Internal Server Error if scraping fails, the API limits
            are reached, or the OpenAI client encounters an error.
    """
    try:
        page = scraper.get_instagram_comments(str(payload.url))
        batch_result = ai_client.rate_comments_batch([page])

        ratings_list = [
            {
                "comment_id": rating.comment_id,
                "category": rating.category,
                "positivity_score": rating.positivity_score,
                "authenticity_score": rating.authenticity_score,
                "summary": rating.summary,
            }
            for rating in batch_result.ratings
        ]

        return {
            "status": "success",
            "message": f"Successfully rated {batch_result.total_processed} comments.",
            "total_processed": batch_result.total_processed,
            "avg_sentiment": batch_result.avg_sentiment_score,
            "avg_authenticity": batch_result.avg_authenticity_score,
            "data": ratings_list,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
