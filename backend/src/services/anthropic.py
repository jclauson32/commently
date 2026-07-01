import json
import os
from typing import List
from anthropic import Anthropic

from src.models.contract import (
    BatchRatingResponse,
    PromptConfig,
    RatingInput,
    RatingOutput,
)
from src.services.prompt_manager import PromptManager
from src.services.scrape_creators import CommentsResponse


class AnthropicRatingClient:
    """Client for batch-processing Instagram video comment ratings via Anthropic."""

    PROMPT_NAME = "instagram_comment_rater"
    PROMPT_VERSION = "v2"

    def __init__(
        self, api_key: str | None = None, prompt_config: PromptConfig | None = None
    ):
        """Anthropic API Client Initialization"""
        self.client = Anthropic(api_key=api_key or os.environ.get("ANTHROPIC_API_KEY"))
        self.prompt_manager = PromptManager()
        self.prompt_config = prompt_config or self.prompt_manager.load_prompt_config(
            self.PROMPT_NAME, self.PROMPT_VERSION
        )
        self.model = "claude-3-5-sonnet-20240620"

    def _get_structured_response(self, messages: List[dict], response_model: type):
        """Helper to map OpenAI-style messages to Anthropic's format."""
        # Convert Pydantic model to JSON Schema for tool use
        schema = response_model.model_json_schema()

        # Anthropic requires system messages separated from user/assistant messages
        system_msg = next((m["content"] for m in messages if m["role"] == "system"), "")
        user_msgs = [m for m in messages if m["role"] != "system"]

        response = self.client.messages.create(
            model=self.model,
            system=system_msg,
            messages=user_msgs,
            max_tokens=4096,
            tools=[
                {
                    "name": "structured_output",
                    "description": "Output data according to schema",
                    "input_schema": schema,
                }
            ],
            tool_choice={"type": "tool", "name": "structured_output"},
        )

        # Extract tool output
        tool_use = next(block for block in response.content if block.type == "tool_use")
        return response_model.model_validate(tool_use.input)

    def rate_comment(self, comment_text: str) -> RatingOutput:
        """Rate a single comment using the versioned prompt contract."""
        messages = self.prompt_manager.get_openai_messages(
            self.prompt_config,
            json.dumps([{"id": "single", "text": comment_text}]),
        )

        # We wrap the output in BatchRatingResponse to reuse the same structure
        batch_result = self._get_structured_response(messages, BatchRatingResponse)

        first_rating = batch_result.ratings[0]
        return RatingOutput(
            category=first_rating.category,
            summary=first_rating.summary,
            positivity_score=first_rating.positivity_score,
            authenticity_score=first_rating.authenticity_score,
        )

    def rate_comments_batch(
        self, responses: List[CommentsResponse], chunk_size: int = 100
    ) -> BatchRatingResponse:
        """Rate Instagram video comments in batches using Anthropic's tool-use API."""
        all_comments = []
        for response in responses:
            all_comments.extend(response.comments)

        if not all_comments:
            return BatchRatingResponse(
                total_processed=0,
                avg_sentiment_score=0.0,
                avg_authenticity_score=0.0,
                ratings=[],
            )

        lean_payload = [{"id": c.id, "text": c.text} for c in all_comments if c.text]
        master_ratings = []
        total_processed_count = 0

        for i in range(0, len(lean_payload), chunk_size):
            chunk = lean_payload[i : i + chunk_size]

            try:
                # Prepare messages for Anthropic
                messages = self.prompt_manager.get_openai_messages(
                    self.prompt_config,
                    json.dumps(chunk),
                )

                # Use helper to get structured response (Tool Use)
                chunk_result = self._get_structured_response(
                    messages, BatchRatingResponse
                )

                master_ratings.extend(chunk_result.ratings)
                total_processed_count += chunk_result.total_processed

                print(
                    f"Processed chunk: {min(i + chunk_size, len(lean_payload))}/{len(lean_payload)}"
                )

            except Exception as e:
                print(f"Failed to process chunk starting at index {i}: {e}")
                raise

        # Calculate averages locally
        if total_processed_count > 0:
            sum_sentiment = sum(r.positivity_score for r in master_ratings)
            sum_authenticity = sum(r.authenticity_score for r in master_ratings)

            avg_sentiment = sum_sentiment / total_processed_count
            avg_authenticity = sum_authenticity / total_processed_count
        else:
            avg_sentiment = 0.0
            avg_authenticity = 0.0

        return BatchRatingResponse(
            total_processed=total_processed_count,
            avg_sentiment_score=round(avg_sentiment, 2),
            avg_authenticity_score=round(avg_authenticity, 2),
            ratings=master_ratings,
        )
