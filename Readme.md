---
title: F1 AI Agent
emoji: 🏎️
colorFrom: red
colorTo: gray
sdk: docker
pinned: false
---
# 🏎️ F1 AI Agent

An F1 AI assistant powered by Mistral, LangGraph, and live F1 tools.

## What it does

Ask any question about Formula 1 in natural language — the agent decides which tool to use and fetches accurate, real-time information.

- 🏁 **Latest race results** — real-time data from OpenF1 API
- 📰 **F1 news** — latest headlines from NewsAPI
- 🔍 **General F1 info** — web search for anything else

## How it works

The LangGraph workflow has four simple steps:
- Classify the question
- Fetch information with the right tool
- Write an answer using the fetched information
- Verify the answer before returning it

The assistant uses OpenF1 for race information, NewsAPI for recent news, and DuckDuckGo for general F1 information.

## Tech Stack

- **Backend** — FastAPI
- **AI / Agent** — LangGraph + Mistral AI
- **Live Data** — OpenF1 API
- **News** — NewsAPI
- **Web Search** — DuckDuckGo (ddgs)
- **Frontend** — HTML, CSS, JS

## Setup

```bash
git clone https://github.com/ayangithub00/F1-AI-Agent.git
cd F1-AI-Agent
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Add `.env`:
```
MISTRAL_API_KEY=your_key
NEWS_API_KEY=your_key
```

Save this file inside the `f1` folder.

```bash
uvicorn f1.main:app --reload
```

## Author

**Ayan Islam** — [GitHub](https://github.com/ayangithub00) · [LinkedIn](https://linkedin.com/in/ayan-islam-5a0212237)
