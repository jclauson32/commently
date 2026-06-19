import os

from src.open_ai import OpenAIRatingClient
from src.scrape_creators import ScrapeCreatorClient

POST_URL = "https://www.instagram.com/yungstarbeam/p/DY2vQkqliwv/"

scraper = ScrapeCreatorClient(
    provider="instagram",
    api_key=os.environ["SCRAPE_CREATORS_API_KEY"],
)
page_1 = scraper.get_instagram_comments(POST_URL)
page_2 = scraper.get_instagram_comments(POST_URL, cursor=page_1.cursor)

ai_client = OpenAIRatingClient(api_key=os.environ.get("OPENAI_API_KEY"))

batch_result = ai_client.rate_comments_batch([page_1, page_2])

print(f"Successfully rated a batch of {batch_result.total_processed} comments.\n")

for rating in batch_result.ratings:
    print(
        f"Comment ID: {rating.comment_id} | "
        f"Category: {rating.category} | "
        f"Positivity: {rating.positivity_score}/10 | "
        f"Bot likelihood: {rating.bot_score}/10 | "
        f"Summary: {rating.summary}"
    )
