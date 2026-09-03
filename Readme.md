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

The LangGraph workflow:
- **Intelligent Routing**: Instantly routes queries to live tools based on context (race results, upcoming calendar, recent news, web search, or instant conversational greetings).
- **Live Tool Retrieval**: Fetches real-time data from OpenF1 API, NewsAPI, or DuckDuckGo.
- **Answer Generation**: Synthesizes a factual, natural language response using Mistral AI based strictly on retrieved facts.
- **Conversation Memory**: Maintains multi-turn session history for context-aware follow-up questions.

The assistant uses OpenF1 for live race results & calendar, NewsAPI for recent news, and DuckDuckGo for general F1 web search.

## Tech Stack

- **Backend** — FastAPI
- **AI / Agent** — LangGraph + Mistral AI
- **Live Data** — OpenF1 API
- **News** — NewsAPI
- **Web Search** — DuckDuckGo (`ddgs`)
- **Frontend** — HTML, CSS, JavaScript

## Setup

```bash
git clone https://github.com/ayangithub00/F1-AI-Agent.git
cd F1-AI-Agent
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create `.env` inside the `f1` folder:
```env
MISTRAL_API_KEY=your_mistral_api_key
NEWS_API_KEY=your_news_api_key
SESSION_SECRET=your_secret_key_optional
```

Run the application:
```bash
uvicorn f1.main:app --reload
```
or from inside the `f1` folder:
```bash
cd f1
uvicorn main:app --reload
```

## Author

**Ayan Islam** — [GitHub](https://github.com/ayangithub00) · [LinkedIn](https://linkedin.com/in/ayan-islam-5a0212237)
