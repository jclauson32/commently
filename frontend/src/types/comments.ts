export interface CommentRating {
  comment_id: string;
  category: string;
  positivity_score: number;
  bot_score: number;
  summary: string;
}

export interface RateCommentsResponse {
  status: string;
  message: string;
  total_processed: number;
  data: CommentRating[];
}

export interface RateCommentsRequest {
  url: string;
}