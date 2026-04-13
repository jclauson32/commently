import requests
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, HttpUrl

class User(BaseModel):
    #is_verified: bool
    #id: str
    #pk: str
    #is_unpublished: Optional[bool] = None
    #profile_pic_url: HttpUrl
    username: str
    #fbid_v2: Optional[str] = None

class Comment(BaseModel):
    id: str
    text: str
    created_at: datetime
    comment_like_count: int
    user: User

class CommentsResponse(BaseModel):
    post_url: str
    success: bool
    #credits_remaining: int
    comments: List[Comment]
    cursor: Optional[str] = None

class ScrapeCreatorClient:
    """ Scrape Creators API Client"""

    BASE_URL = "https://api.scrapecreators.com/v2/"

    def __init__(self, provider: str, api_key: str):
        self.provider = provider
        self.api_key = api_key
    
    def get_instagram_comments(self, post_url: str, cursor: str = None) -> CommentsResponse:
        if not post_url:
            raise ValueError("No post url provided. Please provide one.")
        data = {"url": post_url}
        if cursor:
            data["cursor"] = cursor
        
        # Note from Scrape Creators: Not gonna lie, 
        # this is one of our most error prone endpoints. 
        # You should expect ~90% success rate.
        res = self._scrape_creators_request("instagram/post/comments", data, method="GET")
        
        return CommentsResponse(post_url=post_url, **res)


    def _scrape_creators_request(self, endpoint: str, data: dict, method: str = "POST"):
        
        url = f"{self.BASE_URL.rstrip('/')}/{endpoint.lstrip('/')}"
        headers = {
        "x-api-key": self.api_key,
        **self._scrape_creators_extra_headers()
    }
        try:

            response = requests.request(method, url, headers=headers, params=data)
            
            # Raise an HTTPError for bad responses (4xx or 5xx)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"API Request failed: {e}")
            if response is not None:
                print(f"Response text: {response.text}")
            raise
        
    def _scrape_creators_extra_headers(self)->dict:
        """
        Stub for extra headers.
        """
        return {}