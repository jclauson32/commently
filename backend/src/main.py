import os

from fastapi import FastAPI, HTTPException

from fastapi.middleware.cors import CORSMiddleware

from src.models.requests import RateCommentsRequest
from src.services.open_ai import OpenAIRatingClient
from src.services.scrape_creators import ScrapeCreatorClient

from src.api.comments import router as comments_router

app = FastAPI(title="Comment Rater API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
try:
    # add to state for use in app routes
    app.state.scraper = ScrapeCreatorClient(
        provider="instagram",
        api_key=os.environ["SCRAPE_CREATORS_API_KEY"],
    )
    app.state.ai_client = OpenAIRatingClient(api_key=os.environ["OPENAI_API_KEY"])
except KeyError as e:
    raise RuntimeError(f"Missing required environment variable: {e}")

# region routers

app.include_router(comments_router)

# endregion
