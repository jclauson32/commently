import React, { useState } from 'react';
import { rateComments } from './api/client';
import type { CommentRating } from './types/comments';

export default function App() {
  const [url, setUrl] = useState<string>('');
  const [ratings, setRatings] = useState<CommentRating[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const result = await rateComments({ url });
      setRatings(result.data);
    } catch (err: any) {
      setError(err.message || 'Something went wrong');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '2rem', maxWidth: '600px', margin: '0 auto' }}>
      <h1>Instagram Comment Rater</h1>
      
      <form onSubmit={handleSubmit}>
        <input
          type="url"
          placeholder="Paste Instagram Post URL here"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          required
          style={{ width: '100%', padding: '0.5rem', marginBottom: '1rem' }}
        />
        <button type="submit" disabled={loading} style={{ padding: '0.5rem 1rem' }}>
          {loading ? 'Analyzing...' : 'Analyze Comments'}
        </button>
      </form>

      {error && <p style={{ color: 'red' }}>{error}</p>}

      <div style={{ marginTop: '2rem' }}>
        {ratings.map((rating) => (
          <div key={rating.comment_id} style={{ border: '1px solid #ccc', padding: '1rem', marginBottom: '1rem' }}>
            <h3>Category: {rating.category}</h3>
            <p><strong>Summary:</strong> {rating.summary}</p>
            <p>Positivity: {rating.positivity_score}/10 | Bot Likelihood: {rating.bot_score}/10</p>
          </div>
        ))}
      </div>
    </div>
  );
}