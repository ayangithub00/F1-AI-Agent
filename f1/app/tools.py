from langchain_core.tools import tool
from ddgs import DDGS
import requests
from datetime import datetime, timedelta, timezone
import os

@tool
def search_web(query: str) -> str:
    """Search the web for F1 information including news, standings, driver stats and race results."""
    try:
        enhanced_query = f"{query} 2026 Formula 1"
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
    api_key = os.getenv("NEWS_API_KEY")
    try:
        response = requests.get(
            "https://newsapi.org/v2/everything",
            params={
                "q": f"Formula 1 F1 {query}",
                "apiKey": api_key,
                "sortBy": "publishedAt",
                "pageSize": 5,
                "from": (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
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
    """Get the most recent completed F1 race results, next race info, for the 2026 season."""
    try:
        sessions_response = requests.get(
            "https://api.openf1.org/v1/sessions",
            params={"year": 2026, "session_name": "Race"}
        )
        sessions = sessions_response.json()
        now = datetime.now(timezone.utc)

        completed = [s for s in sessions if s['date_end'] < now.isoformat() and not s['is_cancelled']]
        upcoming = [s for s in sessions if s['date_start'] > now.isoformat() and not s['is_cancelled']]

        output = ""

        if upcoming:
            next_race = upcoming[0]
            output += f"Next Race: {next_race['location']} GP\n"
            output += f"Date: {next_race['date_start'][:10]}\n"
            output += f"Country: {next_race['country_name']}\n\n"

        if completed:
            latest = completed[-1]
            session_key = latest['session_key']
            race_name = latest['location']

            positions_response = requests.get(
                "https://api.openf1.org/v1/position",
                params={"session_key": session_key}
            )
            positions = sorted(positions_response.json(), key=lambda x: x['date'])

            driver_final_position = {}
            for p in positions:
                driver_final_position[p['driver_number']] = p['position']

            top10 = sorted(driver_final_position.items(), key=lambda x: x[1])[:10]

            drivers_response = requests.get(
                "https://api.openf1.org/v1/drivers",
                params={"session_key": session_key}
            )
            drivers = {d['driver_number']: d for d in drivers_response.json()}

            output += f"Latest Race: {race_name} GP 2026\n\n"
            for driver_num, pos in top10:
                driver = drivers.get(driver_num, {})
                name = driver.get('full_name', f'Driver #{driver_num}')
                team = driver.get('team_name', '')
                output += f"P{pos}: {name} ({team})\n"

        return output

    except Exception as e:
        return f"Failed to fetch F1 data: {str(e)}"

@tool
def get_race_by_name(query: str) -> str:
    """Get F1 race results for a SPECIFIC race mentioned by name or location, like Monaco, Barcelona, Silverstone, Spain, Australia etc. Use this whenever the user asks about a specific past race by name."""
    try:
        sessions_response = requests.get(
            "https://api.openf1.org/v1/sessions",
            params={"year": 2026, "session_name": "Race"}
        )
        sessions = sessions_response.json()

        query_lower = query.lower()
        matched = None
        for s in sessions:
            if s['location'].lower() in query_lower or s['country_name'].lower() in query_lower:
                matched = s
                break

        if not matched:
            return "Could not find that specific race in the 2026 calendar."

        session_key = matched['session_key']
        race_name = matched['location']

        positions_response = requests.get(
            "https://api.openf1.org/v1/position",
            params={"session_key": session_key}
        )
        positions = sorted(positions_response.json(), key=lambda x: x['date'])

        driver_final_position = {}
        for p in positions:
            driver_final_position[p['driver_number']] = p['position']

        top10 = sorted(driver_final_position.items(), key=lambda x: x[1])[:10]

        drivers_response = requests.get(
            "https://api.openf1.org/v1/drivers",
            params={"session_key": session_key}
        )
        drivers = {d['driver_number']: d for d in drivers_response.json()}

        output = f"{race_name} GP 2026 Results:\n\n"
        for driver_num, pos in top10:
            driver = drivers.get(driver_num, {})
            name = driver.get('full_name', f'Driver #{driver_num}')
            team = driver.get('team_name', '')
            output += f"P{pos}: {name} ({team})\n"

        return output
    except Exception as e:
        return f"Failed: {str(e)}"
