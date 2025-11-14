import streamlit as st
import pandas as pd
import requests

BASE_URL = "https://www.thesportsdb.com/api/v1/json/123"
ATP_LEAGUE_ID = 4464


def get_atp_season(season):
    """Fetch all ATP season events."""
    url = f"{BASE_URL}/eventsseason.php?id={ATP_LEAGUE_ID}&s={season}"
    r = requests.get(url)
    data = r.json()
    events = data.get("events", []) or []
    return pd.DataFrame(events)

st.title("🎾 ATP Tennis Season Explorer")
st.write("""
This page analyzes data from the **ATP World Tour API**.
Choose a season and chart type to explore official ATP events.
""")


season = st.selectbox(
    "Select a Season:",
    ["2025", "2024", "2023", "2022", "2021"],
    index=2
)


df = get_atp_season(season)

if df.empty:
    st.warning("No data found for this season.")
    st.stop()

df["dateEvent"] = pd.to_datetime(df["dateEvent"], errors="ignore")
df["month"] = pd.to_datetime(df["dateEvent"], errors="coerce").dt.month

st.write(f"### ATP Events for {season}")
st.dataframe(df[["dateEvent", "strEvent", "strVenue", "strCity", "strCountry"]])


events_by_month = df.groupby("month").size()
events_by_country = df.groupby("strCountry").size().sort_values(ascending=False)


chart_choice = st.radio(
    "Choose the Chart You Want to View:",
    ["Events per Month", "Events per Country"]
)

st.subheader(f"📊 {chart_choice}")


if chart_choice == "Events per Month":
    st.line_chart(events_by_month)

else:
    st.bar_chart(events_by_country)