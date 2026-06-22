# ==================================================
# SECTION 1 : Imports
# ==================================================

import streamlit as st
import requests
import pandas as pd
from ui.theme import load_theme
from ui.shell import render_sidebar
from ui.auth_guard import (
    require_login,
    get_auth_headers
)
from ui.session_manager import initialize_session

# ==================================================
# SECTION 2 : Page Config
# ==================================================

st.set_page_config(
    page_title="History",
    page_icon="🕒",
    layout="wide"
)
load_theme()
initialize_session()
render_sidebar()
require_login()

# ==================================================
# SECTION 3 : Hero Card
# ==================================================

st.markdown("""
<div class="hero-card">
<h1 style="
margin:0;
font-size:42px;
">
🕒 Analysis History
</h1>
<p style="
color:#94A3B8;
margin-top:10px;
">
Browse previous analyses and revisit insights.
</p>
</div>
""", unsafe_allow_html=True)

# ==================================================
# SECTION 4 : Authentication Check
# ==================================================

headers = get_auth_headers()

# ==================================================
# SECTION 5 : Load History
# ==================================================

response = requests.get(
    "http://127.0.0.1:8000/history",
    headers=headers
)
if response.status_code != 200:
    st.error("Failed to load history")
    st.stop()

history = response.json()

# ==================================================
# SECTION 6 : History Summary
# ==================================================

total_analyses = len(history)
unique_videos = len(
    set(
        item.get("youtube_video_id","N/A")
        for item in history
    )
)
c1,c2,c3 = st.columns(3)
with c1:
    st.metric(
        "Analyses",
        total_analyses
    )
with c2:
    st.metric(
        "Unique Videos",
        unique_videos
    )
with c3:
    st.metric(
        "Status",
        "Active"
    )
st.divider()
if not history:
    st.info("No analyses found")
    st.stop()

# ==================================================
# SECTION 7 : Search
# ==================================================

search = st.text_input("🔍 Search by Video ID")
if search:
    history = [
        item
        for item in history
        if search.lower()
        in str(
            item.get("video_id","")
        ).lower()
    ]
if not history:
    st.info("No matching analyses found.")
    st.stop()
df = pd.DataFrame(history)

# ==================================================
# SECTION 8 : Analysis Records
# ==================================================

st.subheader("📄 Analysis Records")
st.dataframe(
    df,
    use_container_width=True
)

# ==================================================
# SECTION 9 : Actions
# ==================================================

st.subheader("⚙️ Actions")
selected = st.selectbox(
    "Select Analysis",
    options=[
        item["analysis_id"]
        for item in history
    ]
)
if st.button("View Analysis"):
    response = requests.get(
        f"http://127.0.0.1:8000/history/{selected}",
        headers=headers
    )
    if response.status_code == 200:
        analysis = response.json()
        st.session_state["loaded_analysis"] = analysis
        st.session_state["analysis_data"] = analysis
        st.success("Analysis loaded")

# ==================================================
# SECTION 10 : Analysis Preview
# ==================================================

analysis = st.session_state["loaded_analysis"]

if analysis:

    st.subheader("📊 Analysis Preview")

    col1,col2,col3 = st.columns(3)

    with col1:

        st.metric(
            "Comments",
            analysis["total_comments"]
        )

    with col2:

        st.metric(
            "Engagement",
            analysis["engagement_score"]
        )

    with col3:

        st.metric(
            "Virality",
            analysis["virality_prediction"]
        )

    st.json(
        analysis["sentiment_counts"]
    )

# ==================================================
# SECTION 11 : Delete Analysis
# ==================================================

if st.button(
    "🗑 Delete Selected Analysis",
    type="secondary"

):
    delete_response = requests.delete(
        f"http://127.0.0.1:8000/history/{selected}",
        headers=headers
    )
    if delete_response.status_code == 200:
        st.success(
            "Analysis deleted"
        )
        st.rerun()
    else:
        st.error(
            "Delete failed"
        )