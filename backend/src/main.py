import os

from fastapi import FastAPI, HTTPException

from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl

from src.services.open_ai import OpenAIRatingClient
from src.services.scrape_creators import ScrapeCreatorClient

app = FastAPI(title="Comment Rater API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],# Vite port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Initialize clients globally to avoid re-initializing on every request.
# Make sure your environment variables are set before starting the server!
try:
    scraper = ScrapeCreatorClient(
        provider="instagram",
        api_key=os.environ["SCRAPE_CREATORS_API_KEY"],
    )
    ai_client = OpenAIRatingClient(
        api_key=os.environ["OPENAI_API_KEY"]
    )
except KeyError as e:
    raise RuntimeError(f"Missing required environment variable: {e}")

# Pydantic model for request validation
class RateCommentsRequest(BaseModel):
    url: HttpUrl  # Validates that the input is a properly formatted URL

@app.post("/rate-comments")
async def rate_comments(request: RateCommentsRequest):
    try:
        
        page = scraper.get_instagram_comments(str(request.url))
        
      
        batch_result = ai_client.rate_comments_batch([page])

        ratings_list = [
            {
                "comment_id": rating.comment_id,
                "category": rating.category,
                "positivity_score": rating.positivity_score,
                "bot_score": rating.bot_score,
                "summary": rating.summary
            }
            for rating in batch_result.ratings
        ]

        return {
            "status": "success",
            "message": f"Successfully rated {batch_result.total_processed} comments.",
            "total_processed": batch_result.total_processed,
            "data": ratings_list
        }

    except Exception as e:
        # Catch errors (e.g., rate limits, invalid post URLs) and return a 500 error
        raise HTTPException(status_code=500, detail=str(e))