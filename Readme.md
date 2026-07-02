---
title: F1 AI Agent
emoji: 🏎️
colorFrom: red
colorTo: gray
sdk: docker
pinned: false
---
# 🏎️ F1 AI Agenta

An agentic AI assistant for Formula 1 — powered by Mistral LLM, OpenF1 API, and LangChain.

## What it does

Ask any question about Formula 1 in natural language — the agent decides which tool to use and fetches accurate, real-time information.

- 🏁 **Latest race results** — real-time data from OpenF1 API
- 📰 **F1 news** — latest headlines from NewsAPI
- 🔍 **General F1 info** — web search for anything else

## How it works

The agent has 3 tools:
- `get_f1_results` — fetches live and recent race results from OpenF1
- `search_f1_news` — fetches latest F1 news from NewsAPI
- `search_web` — DuckDuckGo search for general F1 questions

The LLM (Mistral) decides which tool to use based on the question — this is what makes it agentic, not just a chatbot.

## Tech Stack

- **Backend** — Django REST Framework
- **AI / Agent** — LangChain + Mistral AI
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
HUGGINGFACEHUB_API_TOKEN=your_key
NEWS_API_KEY=your_key
```

```bash
cd f1
python manage.py runserver
```

## Author

**Ayan Islam** — [GitHub](https://github.com/ayangithub00) · [LinkedIn](https://linkedin.com/in/ayan-islam-5a0212237)