import type { RateCommentsRequest, RateCommentsResponse } from '../types/comments';

// Replace with your local FastAPI URL (default is usually port 8000)
const API_BASE_URL = 'http://localhost:8000';

export async function rateComments(payload: RateCommentsRequest): Promise<RateCommentsResponse> {
  const response = await fetch(`${API_BASE_URL}/rate-comments`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || 'Failed to analyze comments');
  }

  return response.json();
}