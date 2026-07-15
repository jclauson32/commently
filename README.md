# Commently


See how a piece of media's comments are rated by an LLM! Commently will rate a post's comments and give a comment by comment breakdown of each's sentiment and authenticity 😀

[Commently Explained](https://www.loom.com/share/883c745fe45e47008afdfee0e9431ece)
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

This project implements a robust, automated evaluation framework designed to benchmark model efficiency. By establishing a deterministic "Golden Dataset" (backend/test/benchmark_data.json) file and an automated regression testing pipeline, we ensure that every change to a system prompt is validated against human-verified truth before reaching production.

## Backend Stack:
- FastAPI to service requests to the user from the backend
- Pydantic for data dalidation
- ScrapeCreatorsAPI (Used over instagram's native API to bypass the 20 comment limit)
- Anthropic / OpenAI API used for comment rating in batch

## Frontend Stack:
- Typescript
- React
- Vite (Build tool)
- Node.js & npm (Development environment)


## Creating The Golden Dataset
### Uses comments from these 10 non-profit organizations' instagrams, grading them manually by giving them a positivity (agreement) and authenticity rating.
    - charity: water https://www.charitywater.org/ (@charitywater)
    - Rescue City https://www.rescuecity.nyc/ (@rescuecity)
    - Pencils of Promise https://pencilsofpromise.org/ (@pencilsofpromise)
    - Gigis Playhouse https://gigisplayhouse.org/ (@gigisplayhouse)
    - Minnesota Zoo https://mnzoo.org/ (@mnzoo)
    - Feed My Starving Children https://www.fmsc.org/ (@fmsc_org)
    - United Way Dane County https://www.unitedwaydanecounty.org/ (unitedwaydaneco)
    - Cure International Children's Hospital https://cure.org/ (@cureintl)
    - She Recovers https://sherecovers.org/ (@she_recovers)
    - Wounded Warriors Project https://www.woundedwarriorproject.org/ (@wwp)

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

   cd backend && pip install -r src/requirements.txt
   ```
### Install frontend dependencies:
    cd frontend && npm install


### Set your environment variables:
    
    export SCRAPE_CREATORS_API_KEY="your_key"

    export ANTHROPIC_API_KEY="your_key"
    export OPENAI_API_KEY="your_key"
# Run the development environment:

## Backend

- Inside backend directory
uvicorn src.main:app --reload
## Frontend
- Inside frontend directory
npm install

npm run dev

### Roadmap and Future features

    - Use the official Instagram API (We are currently using the ScrapeCreators API because Instagrams official API only allows looking at a maximum of 50 messages.)
    - Expand this to be used on any Social Media Site (Tiktok, Facebook, Linkedin, etc.)
    - See an overview of a profile and Overall Positivity / Authenticity for every video on a profile.
    - Publicly accessible URL, not just local hosted.
    - Create users accounts so users can see saved videos/profiles and enter in their own respective Anthropic / OpenAI API keys.
    - Expand the metrics list.
    - Create a marketing suite providing organizations and individuals with Metrics over time. 
### Privacy & Ethics

We believe in transparent data usage. This tool is designed to process public data only and does not store user-identifiable information. We encourage all users to use these insights to promote inclusivity and positive community growth.

---



### Legal Statement
The analysis provided by this tool is for informational purposes only. Commently does not guarantee the accuracy, completeness, or reliability of the sentiment and authenticity scores generated. By using this service, you agree to comply with the platform's terms of service from which data is sourced. The developers assume no liability for actions taken based on these insights, and all usage of this tool must align with applicable local laws and platform data policies.

---
*Built to serve the digital community.*

Copyright (c) 2026 Joseph Clauson. All rights reserved.
