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

st.set_page_config(page_title="ATP Season Explorer", page_icon="🎾", layout="centered")

st.markdown(
    """
    <h1 style="text-align:center; margin-bottom:0px;">🎾 ATP Tennis Season Explorer</h1>
    <p style="text-align:center; font-size:18px; color:#bdbdbd;">
        Explore official ATP tournaments by season with interactive charts.
    </p>
    """,
    unsafe_allow_html=True,
)

st.markdown("---")

col1, col2 = st.columns([1, 1])

with col1:
    season = st.selectbox(
        "📅 Select a Season:",
        ["2025", "2024", "2023", "2022", "2021"],
        index=2,
        help="Choose which ATP season to explore",
    )

with col2:
    chart_choice = st.radio(
        "📊 Chart Type:",
        ["Events per Month", "Events per Country"],
        horizontal=True,
    )

df = get_atp_season(season)

if df.empty:
    st.warning("No data found for this season.")
    st.stop()

df["dateEvent"] = pd.to_datetime(df["dateEvent"], errors="coerce")
df["month"] = df["dateEvent"].dt.month

events_by_month = df.groupby("month").size()
events_by_country = df.groupby("strCountry").size().sort_values(ascending=False)

st.markdown("### 🗂️ Events Table")
st.caption(f"Showing all {len(df)} ATP events for **{season}**.")

pretty_cols = ["dateEvent", "strEvent", "strVenue", "strCity", "strCountry"]
st.dataframe(df[pretty_cols], hide_index=True, use_container_width=True)

st.markdown("---")

if chart_choice == "Events per Month":
    st.markdown("### 📈 Events per Month")
    st.caption("Number of ATP tournaments occurring each month.")
    st.line_chart(events_by_month)

else:
    st.markdown("### 🌍 Events per Country")
    st.caption("How many ATP tournaments were held in each country.")
    st.bar_chart(events_by_country)

st.markdown("---")
