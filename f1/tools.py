from datetime import datetime, timedelta, timezone
import requests
from ddgs import DDGS
from langchain_core.tools import tool
from .config import NEWS_API_KEY


def get_race_results(race):
    session_key = race["session_key"]

    positions = requests.get(
        "https://api.openf1.org/v1/position",
        params={"session_key": session_key},
        timeout=15,
    ).json()

    drivers = requests.get(
        "https://api.openf1.org/v1/drivers",
        params={"session_key": session_key},
        timeout=15,
    ).json()

    final_positions = {}
    for position in positions:
        final_positions[position["driver_number"]] = position["position"]

    driver_names = {}
    for driver in drivers:
        driver_names[driver["driver_number"]] = driver

    lines = [f"{race['location']} GP 2026 results:"]
    top_ten = sorted(final_positions.items(), key=lambda item: item[1])[:10]

    for number, position in top_ten:
        driver = driver_names.get(number, {})
        name = driver.get("full_name", f"Driver {number}")
        team = driver.get("team_name", "Unknown team")
        lines.append(f"P{position}: {name} ({team})")

    return "\n".join(lines)


@tool
def get_latest_or_next_race(question: str) -> str:
    """Get the latest completed Formula 1 race results or the next race in 2026."""
    try:
        response = requests.get(
            "https://api.openf1.org/v1/sessions",
            params={"year": 2026, "session_name": "Race"},
            timeout=15,
        )
        races = response.json()
        now = datetime.now(timezone.utc)
        completed = []
        upcoming = []

        for race in races:
            start = datetime.fromisoformat(race["date_start"].replace("Z", "+00:00"))
            end = datetime.fromisoformat(race["date_end"].replace("Z", "+00:00"))
            if not race["is_cancelled"] and end < now:
                completed.append(race)
            if not race["is_cancelled"] and start > now:
                upcoming.append(race)

        completed.sort(key=lambda race: race["date_end"])
        upcoming.sort(key=lambda race: race["date_start"])
        question = question.lower()
        lines = []

        if "next" in question and upcoming:
            race = upcoming[0]
            lines.append(f"Next race: {race['location']} GP")
            lines.append(f"Date: {race['date_start'][:10]}")
            lines.append(f"Country: {race['country_name']}")

        if any(word in question for word in ["latest", "last", "previous", "recent"]) and completed:
            if lines:
                lines.append("")
            lines.append(get_race_results(completed[-1]))

        return "\n".join(lines) or "No matching 2026 race information was found."
    except Exception as error:
        return f"Could not get race information: {error}"


@tool
def get_race_by_name(question: str) -> str:
    """Get 2026 results for one named Formula 1 race, country, or location."""
    try:
        races = requests.get(
            "https://api.openf1.org/v1/sessions",
            params={"year": 2026, "session_name": "Race"},
            timeout=15,
        ).json()

        for race in races:
            location = race["location"].lower()
            country = race["country_name"].lower()
            if location in question.lower() or country in question.lower():
                return get_race_results(race)

        return "That race was not found in the 2026 calendar."
    except Exception as error:
        return f"Could not get race results: {error}"


@tool
def get_f1_news(question: str) -> str:
    """Get recent Formula 1 news."""
    try:
        response = requests.get(
            "https://newsapi.org/v2/everything",
            params={
                "q": f"Formula 1 {question}",
                "apiKey": NEWS_API_KEY,
                "sortBy": "publishedAt",
                "pageSize": 5,
                "from": (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d"),
            },
            timeout=15,
        )
        articles = response.json().get("articles", [])
        lines = []

        for article in articles:
            lines.append(f"Title: {article['title']}")
            lines.append(f"Description: {article['description']}")
            lines.append(f"Published: {article['publishedAt']}")
            lines.append("")

        return "\n".join(lines) or "No recent F1 news was found."
    except Exception as error:
        return f"Could not get news: {error}"


@tool
def search_f1_web(question: str) -> str:
    """Search the web for general Formula 1 information."""
    try:
        with DDGS() as search:
            results = search.text(f"Formula 1 {question}", max_results=5)

        lines = []
        for result in results:
            lines.append(f"Title: {result['title']}")
            lines.append(f"Information: {result['body']}")
            lines.append("")

        return "\n".join(lines) or "No F1 information was found."
    except Exception as error:
        return f"Could not search the web: {error}"
