import requests
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class Comment(BaseModel):
    id: str
    text: str
    timestamp: datetime


class CommentsResponse(BaseModel):
    data: List[Comment]


class CreateCommentResponse(BaseModel):
    id: str


class InstagramClient:
    """Instagram Graph API client for media comments."""

    INSTAGRAM_LOGIN_BASE_URL = "https://graph.instagram.com"
    FACEBOOK_LOGIN_BASE_URL = "https://graph.facebook.com"

    def __init__(
        self,
        access_token: str,
        api_version: Optional[str] = None,
        use_facebook_login: bool = True,
    ):
        """
        Initializes the Instagram Graph API client.

        Args:
            access_token (str): Instagram or Facebook User access token with comment permissions.
            api_version (str, optional): Graph API version such as 'v23.0'.
            use_facebook_login (bool): Use graph.facebook.com when true, otherwise graph.instagram.com.
        """
        if not access_token:
            raise ValueError("No access token provided. Please provide one.")

        base_url = (
            self.FACEBOOK_LOGIN_BASE_URL
            if use_facebook_login
            else self.INSTAGRAM_LOGIN_BASE_URL
        )

        self.access_token = access_token
        self.base_url = (
            f"{base_url.rstrip('/')}/{api_version.strip('/')}" if api_version else base_url
        )

    def create_comment(
        self, media_id: str, message: str
    ) -> CreateCommentResponse:
        """
        Creates an Instagram comment on a media object.

        Args:
            media_id (str): IG Media ID to comment on.
            message (str): Text to include in the comment.

        Returns:
            CreateCommentResponse: The created comment ID.
        """
        if not media_id:
            raise ValueError("No media id provided. Please provide one.")
        if not message:
            raise ValueError("No message provided. Please provide one.")

        response = self._instagram_request(
            f"{media_id}/comments", {"message": message}, method="POST"
        )

        return CreateCommentResponse(**response)

    def get_comments(
        self, media_id: str, fields: Optional[List[str]] = None, limit: Optional[int] = None
    ) -> CommentsResponse:
        """
        Gets top-level comments on an Instagram media object.

        Returns a maximum of 50 comments per query. Replies are only included if
        requested through field expansion.

        Args:
            media_id (str): IG Media ID whose comments should be fetched.
            fields (list[str], optional): Comment fields to request.
            limit (int, optional): Maximum comments to return, capped by the API at 50.

        Returns:
            CommentsResponse: Graph API comments response.
        """
        if not media_id:
            raise ValueError("No media id provided. Please provide one.")

        data = {}
        if fields:
            data["fields"] = ",".join(fields)
        if limit:
            data["limit"] = limit

        response = self._instagram_request(f"{media_id}/comments", data, method="GET")

        return CommentsResponse(**response)

    def _instagram_request(self, endpoint: str, data: dict, method: str = "GET"):
        """
        Executes a request against the Instagram Graph API.

        Args:
            endpoint (str): The API endpoint path (e.g., '<IG_MEDIA_ID>/comments').
            data (dict): The payload or query parameters to be sent with the request.
            method (str): The HTTP method to use.

        Returns:
            dict: The JSON-parsed response from the API.

        Raises:
            requests.exceptions.RequestException: If the network request fails or
                returns an unsuccessful status code.
        """
        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        params = {"access_token": self.access_token, **data}
        payload = dict(data)
        request_kwargs = {"params": params}
        if method.upper() not in {"GET", "POST"}:
            request_kwargs["data"] = payload

        response = None
        try:
            response = requests.request(method, url, **request_kwargs)

            response.raise_for_status()

            return response.json()

        except requests.exceptions.RequestException as e:
            print(f"API Request failed: {e}")
            if response is not None:
                print(f"Response text: {response.text}")
            raise
