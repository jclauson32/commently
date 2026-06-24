export interface CommentRating {
  comment_id: string;
  category: string;
  positivity_score: number;
  authenticity_score: number;
  summary: string;
}

export interface RateCommentsResponse {
  status: string;
  message: string;
  total_processed: number;
  avg_sentiment: number;
  avg_authenticity: number;
  data: CommentRating[];
}

export interface RateCommentsRequest {
  url: string;
}