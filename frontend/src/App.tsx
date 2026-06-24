import React, { useState } from 'react';
import { rateComments } from './api/client';
import type { RateCommentsResponse } from './types/comments';

export default function App() {
  const [url, setUrl] = useState<string>('');
  const [result, setResult] = useState<RateCommentsResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null); // Clear previous results

    try {
      const response = await rateComments({ url });
      setResult(response); // Store the entire object
    } catch (err: any) {
      setError(err.message || 'An error occurred while processing your request.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <main style={{ padding: '4rem 2rem', maxWidth: '700px', margin: '0 auto', textAlign: 'left' }}>
      <header style={{ marginBottom: '3rem' }}>
        <h1>Authentic Reach Analysis</h1>
        <p style={{ fontSize: '1.2rem', color: 'var(--text)' }}>
          Helpful tools to measure the sentiment and authenticity of discussions on your public posts.
        </p>
      </header>
      
      <form onSubmit={handleSubmit} style={{ marginBottom: '4rem' }}>
        <input
          type="url"
          placeholder="Paste Instagram Post URL..."
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          required
          className="search-input"
        />
        <button type="submit" disabled={loading} className="primary-button">
          {loading ? 'Analyzing...' : 'Analyze Comments'}
        </button>
      </form>

      {error && <div className="error-box">{error}</div>}

      {result && (
        <section style={{ marginBottom: '3rem' }}>
          <h2 style={{ marginBottom: '1rem' }}>Analysis Overview</h2>
          <div style={{ display: 'flex', gap: '1.5rem', flexWrap: 'wrap' }}>
            <div className="stat-card">Avg Sentiment: <strong>{result.avg_sentiment}/10</strong></div>
            <div className="stat-card">Avg Authenticity: <strong>{result.avg_authenticity}/10</strong></div>
            <div className="stat-card">Comments Analyzed: <strong>{result.total_processed}</strong></div>
          </div>
        </section>
      )}

      {result?.data && (
        <section>
          <h2 style={{ marginBottom: '2rem' }}>Individual Comments</h2>
          {result.data.map((rating) => (
            <article key={rating.comment_id} className="rating-card">
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                <span className="badge">{rating.category}</span>
              </div>
              <p style={{ marginBottom: '1rem', fontStyle: 'italic' }}>"{rating.summary}"</p>
              <div style={{ display: 'flex', gap: '1rem', fontSize: '0.9rem', color: 'var(--text)' }}>
                <span>Positivity: <strong>{rating.positivity_score}/10</strong></span>
                <span>Authenticity: <strong>{rating.authenticity_score}/10</strong></span>
              </div>
            </article>
          ))}
        </section>
      )}
    </main>
  );
}