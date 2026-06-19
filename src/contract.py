from datetime import datetime
from typing import List

from pydantic import BaseModel, Field


class RatingInput(BaseModel):
    """Interface contract input: raw text to classify and summarize."""

    text: str = Field(description="The comment text to rate.")


class RatingOutput(BaseModel):
    """Interface contract output: structured JSON with category, summary, and scores."""

    category: str = Field(
        description="Sentiment or intent category (e.g. positive, negative, neutral, spam)."
    )
    summary: str = Field(description="Brief summary of the comment's meaning or tone.")
    positivity_score: int = Field(
        ge=1,
        le=10,
        description="Positivity from 1 (highly negative/toxic) to 10 (highly positive/joyful).",
    )
    bot_score: int = Field(
        ge=1,
        le=10,
        description="Likelihood the comment is from an LLM or bot, from 1 (clearly human) to 10 (clearly automated).",
    )


class FewShotExample(BaseModel):
    input: str
    output: RatingOutput


class PromptConfig(BaseModel):
    """Versioned prompt definition consumed by the eval pipeline."""

    version_id: str
    timestamp: datetime
    system_prompt: str
    few_shot_examples: List[FewShotExample] = Field(default_factory=list)


class CommentRating(BaseModel):
    comment_id: str
    category: str
    summary: str
    positivity_score: int = Field(ge=1, le=10)
    bot_score: int = Field(ge=1, le=10)


class BatchRatingResponse(BaseModel):
    total_processed: int = Field(description="The number of comments rated in this batch.")
    ratings: List[CommentRating]
