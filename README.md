# Commently


See how a piece of media's comments are rated by an LLM! Commently will rate a post's comments and give a comment by comment breakdown of each's sentiment and authenticity 😀

---

## The Mission
Strip away the noise to get the *quality* and *intent* behind the comments of public posts.

## How it Works
Using sentiment analysis and authenticity scoring, our tool processes engagement threads to identify patterns typical of non-human interactions while also highlighting the emotional tone of the discussion.

### Key Features
* **Aggregate Insights:** Get an immediate high-level summary of a post’s sentiment and authenticity scores.
* **Automated LLM Evaluation Framework:** Versioned prompts to allow tracking and benchmarking of Prompts.
* **Comment By Comment Breakdown:** View detailed breakdowns for each comment, identifying category-specific behaviors.

## Automated LLM Evaluation Framework
### The Problem

In modern software development, teams often ship prompt changes "blind," as rigorous prompt validation is a new domain. This leads to silent regressions in model behavior, inconsistent output quality, and a lack of visibility into how small prompt adjustments impact downstream system performance.

This project implements a robust, automated evaluation framework designed to benchmark model efficiency. By establishing a deterministic "Golden Dataset" prompts folder and an automated regression testing pipeline, we ensure that every change to a system prompt is validated against human-verified truth before reaching production.
## Getting Started
To run this project locally, ensure you have your API keys configured in your environment.

### Prerequisites
* Python 3.10+
* Node.js 18+
* An active [Scrape Creators](https://scrapecreators.com) API key
* An active OpenAI or Anthropic API key

## Install backend dependencies
### Clone the repository and install backend dependencies:
   ```
   git clone https://github.com/jclauson32/commently.git

   cd backend && pip install -r requirements.txt
   ```
### Install frontend dependencies:
    cd frontend && npm install


### Set your environment variables:
    
    export SCRAPE_CREATORS_API_KEY="your_key"

    export ANTHROPIC_API_KEY="your_key"
    export OPENAI_API_KEY="your_key"
# Run the development environment:

## Backend
uvicorn main:app --reload
## Frontend
npm install

npm run dev

### Privacy & Ethics

We believe in transparent data usage. This tool is designed to process public data only and does not store user-identifiable information. We encourage all users to use these insights to promote inclusivity and positive community growth.

---

### Legal Statement
The analysis provided by this tool is for informational purposes only. Commently does not guarantee the accuracy, completeness, or reliability of the sentiment and authenticity scores generated. By using this service, you agree to comply with the platform's terms of service from which data is sourced. The developers assume no liability for actions taken based on these insights, and all usage of this tool must align with applicable local laws and platform data policies.

---
*Built to serve the digital community.*

Copyright (c) 2026 Joseph Clauson. All rights reserved.
