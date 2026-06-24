import type { RateCommentsRequest, RateCommentsResponse } from '../types/comments';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

/**
 * Submits an Instagram URL to the backend to scrape and evaluate its comments.
 * * This function sends a POST request to the `/rate-comments` endpoint, where
 * the backend will process the comments through an AI rating pipeline to 
 * determine sentiment, authenticity-likelihood, and generate individual summaries.
 * * @param {RateCommentsRequest} payload - The request object containing the target Instagram `url`.
 * @returns {Promise<RateCommentsResponse>} A promise resolving to the structured evaluation results.
 * @throws {Error} Throws an error if the network request fails, or the backend returns a non-200 status.
 */
export async function rateComments(payload: RateCommentsRequest): Promise<RateCommentsResponse> {
  try {
    const response = await fetch(`${API_BASE_URL}/rate-comments`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    });

    // Handle HTTP errors (4xx, 5xx)
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      // Use the specific backend detail if available, otherwise fallback to the HTTP status text
      throw new Error(errorData.detail || `Backend error: ${response.status} ${response.statusText}`);
    }

    return await response.json();

  } catch (error) {
    // Catch network errors (e.g., backend is offline, CORS issues) and rethrow cleanly for the UI
    console.error('[API Error] rateComments failed:', error);
    throw error instanceof Error
      ? error
      : new Error('An unexpected network error occurred while analyzing comments.');
  }
}