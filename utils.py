import requests
import pandas as pd

BASE_URL = "https://www.thesportsdb.com/api/v1/json/123"
ATP_LEAGUE_ID = 4464

def get_upcoming_atp():
    """Fetch next ATP World Tour events."""
    url = f"{BASE_URL}/eventsnextleague.php?id={ATP_LEAGUE_ID}"
    r = requests.get(url)
    data = r.json()
    events = data.get("events", []) or []
    return pd.DataFrame(events)


def get_atp_season(season="2025"):
    """Fetch all ATP events for a season."""
    url = f"{BASE_URL}/eventsseason.php?id={ATP_LEAGUE_ID}&s={season}"
    r = requests.get(url)
    data = r.json()
    events = data.get("events", []) or []
    return pd.DataFrame(events)
