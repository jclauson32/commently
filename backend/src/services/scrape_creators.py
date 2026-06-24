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
        """
        Initializes the ScrapeCreatorClient.

        Args:
            provider (str): The social media platform provider (e.g., 'instagram').
            api_key (str): The authentication key for the Scrape Creators service.
        """
        self.provider = provider
        self.api_key = api_key
    
    def get_instagram_comments(self, post_url: str, cursor: str = None) -> CommentsResponse:
        """
        Retrieves a collection of comments from a specific Instagram post.

        This method sends a GET request to the Scrape Creators API. It handles 
        pagination via the 'cursor' parameter if more comments are available.

        Args:
            post_url (str): The full URL of the Instagram post to scrape.
            cursor (str, optional): The pagination token for fetching subsequent 
                pages of comments. Defaults to None.

        Returns:
            CommentsResponse: A structured response containing the post URL, 
                success status, and a list of Comment objects.

        Raises:
            ValueError: If the provided post_url is empty or invalid.
            requests.exceptions.RequestException: If the API request fails 
                due to network issues or API errors.
        """
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
        """
        Executes a secure HTTP request to the Scrape Creators API.

        Args:
            endpoint (str): The API endpoint path (e.g., 'instagram/post/comments').
            data (dict): The payload or query parameters to be sent with the request.
            method (str): The HTTP method to use (default: 'POST').

        Returns:
            dict: The JSON-parsed response from the API.

        Raises:
            requests.exceptions.RequestException: If the network request fails or 
                returns a non-200 status code.
        """
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