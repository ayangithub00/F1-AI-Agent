from langchain_core.tools import tool
from ddgs import DDGS
import requests
from datetime import datetime, timedelta

@tool
def search_web(query: str) -> str:
    """Search the web for F1 information including live race results, current standings, latest news and real-time data."""
    try:
        current_date = datetime.now().strftime("%B %Y")
        enhanced_query = f"{query} {current_date} Formula 1"
        with DDGS() as ddgs:
            results = ddgs.text(enhanced_query, max_results=7)
            if not results:
                return "No results found."
            return "\n\n".join([
                f"Title: {r['title']}\nSnippet: {r['body']}"
                for r in results
            ])
    except Exception as e:
        return f"Search failed: {str(e)}"
    

@tool
def search_f1_news(query: str) -> str:
    """Search for latest F1 news, race results and current events from today."""
    import os
    api_key = os.getenv("NEWS_API_KEY")
    try:
        response = requests.get(
            "https://newsapi.org/v2/everything",
            params={
                "q": f"Formula 1 F1 {query}",
                "apiKey": api_key,
                "sortBy": "publishedAt",
                "pageSize": 5,
                "from": (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d")
            }
        )
        articles = response.json().get("articles", [])
        if not articles:
            return "No recent news found."
        return "\n\n".join([
            f"Title: {a['title']}\nDescription: {a['description']}\nPublished: {a['publishedAt']}"
            for a in articles
        ])
    except Exception as e:
        return f"News search failed: {str(e)}"
    
@tool
def get_f1_results(query: str) -> str:
    """Get official F1 race results, current standings, driver info and live race data."""
    import requests
    try:
        # Get all 2026 race sessions
        sessions_response = requests.get(
            "https://api.openf1.org/v1/sessions",
            params={"year": 2026, "session_name": "Race"}
        )
        sessions = sessions_response.json()

        # Get latest completed session
        from datetime import datetime, timezone
        now = datetime.now(timezone.utc)
        completed = [s for s in sessions if s['date_end'] < now.isoformat() and not s['is_cancelled']]
        
        if not completed:
            return "No completed races found."

        latest = completed[-1]
        session_key = latest['session_key']
        race_name = latest['location']

        # Get final positions
        positions_response = requests.get(
            "https://api.openf1.org/v1/position",
            params={"session_key": session_key}
        )
        positions = positions_response.json()

        # Get last known position for each driver
        driver_positions = {}
        for p in positions:
            driver_positions[p['driver_number']] = p['position']

        top10 = sorted(driver_positions.items(), key=lambda x: x[1])[:10]

        # Get driver names
        drivers_response = requests.get(
            "https://api.openf1.org/v1/drivers",
            params={"session_key": session_key}
        )
        drivers = {d['driver_number']: d for d in drivers_response.json()}

        output = f"Latest Race: {race_name} GP 2026\n\n"
        for driver_num, pos in top10:
            driver = drivers.get(driver_num, {})
            name = driver.get('full_name', f'Driver #{driver_num}')
            team = driver.get('team_name', '')
            output += f"P{pos}: {name} ({team})\n"

        return output

    except Exception as e:
        return f"Failed to fetch F1 data: {str(e)}"