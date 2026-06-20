from pydantic import BaseModel, HttpUrl

class RateCommentsRequest(BaseModel):
    url: HttpUrl 