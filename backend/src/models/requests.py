from pydantic import BaseModel, HttpUrl


class RateCommentsRequest(BaseModel):
    """Pydantic model for request validation"""

    url: HttpUrl  # https://pydantic.dev/docs/validation/2.3/usage/types/urls/
