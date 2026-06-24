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
    authenticity_score: int = Field(
        ge=1,
        le=10,
        description="Likelihood the comment is from an LLM or authenticity, from 1 (clearly human) to 10 (clearly automated).",
    )


class FewShotExample(BaseModel):
    """
    A single demonstration example used for few-shot prompting.

    Pairs a raw input string (typically JSON containing an ID and text)
    with the expected structured `RatingOutput`.
    """

    input: str
    output: RatingOutput


class PromptConfig(BaseModel):
    """Versioned prompt definition consumed by the eval pipeline."""

    version_id: str
    timestamp: datetime
    system_prompt: str
    few_shot_examples: List[FewShotExample] = Field(default_factory=list)


class CommentRating(BaseModel):
    """
    The final evaluated rating for a specific comment.

    This extends the base rating metrics by associating them directly
    with the original comment's unique identifier.
    """

    comment_id: str
    category: str
    summary: str
    positivity_score: int = Field(ge=1, le=10)
    authenticity_score: int = Field(ge=1, le=10)


class BatchRatingResponse(BaseModel):
    """
    The aggregated result of processing a batch of comments.

    Contains the total number of successfully processed comments,
    averaged metrics for the batch, and a list of their individual evaluations.
    """

    total_processed: int = Field(
        description="The number of comments rated in this batch."
    )

    avg_sentiment_score: float = Field(
        description="The average positivity score across all processed comments."
    )

    avg_authenticity_score: float = Field(
        description="The average bot score across all processed comments."
    )

    ratings: List[CommentRating]
