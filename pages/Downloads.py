# ==================================================
# SECTION 1 : Imports
# ==================================================

import streamlit as st
import pandas as pd
from ui.theme import load_theme
from ui.shell import render_sidebar
from ui.auth_guard import require_login
from ui.session_manager import initialize_session

# ==================================================
# SECTION 2 : Page Config
# ==================================================

st.set_page_config(
    page_title="Downloads",
    page_icon="📥",
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
📥 Export Center
</h1>
<p style="
color:#94A3B8;
margin-top:10px;
">
Download sentiment reports and analyzed comments.
</p>
</div>
""", unsafe_allow_html=True)

# ==================================================
# SECTION 4 : Check Analysis Data
# ==================================================

if not st.session_state["analysis_data"]:
    st.warning("⚠️ Please analyze a video from Dashboard first.")
    st.stop()
data = st.session_state["analysis_data"]

# ==================================================
# SECTION 5 : Export Summary
# ==================================================

total_comments = len(
    data["detailed_comments"]
)
positive = data["sentiment_counts"].get(
    "Positive",
    0
)
negative = data["sentiment_counts"].get(
    "Negative",
    0
)
c1,c2,c3 = st.columns(3)
with c1:
    st.metric(
        "Comments",
        total_comments
    )
with c2:
    st.metric(
        "Positive",
        positive
    )
with c3:
    st.metric(
        "Negative",
        negative
    )
st.divider()

# ==================================================
# SECTION 6 : Summary Report
# ==================================================

st.subheader(
    "📊 Summary Report"
)
summary_df = pd.DataFrame({
    "Sentiment": list(data["sentiment_counts"].keys()),
    "Count": list(data["sentiment_counts"].values()),
    "Percentage (%)": list(data["sentiment_percentages"].values())
})
st.dataframe(summary_df, use_container_width=True)
st.download_button(
    label="⬇️ Download Summary CSV",
    data=summary_df.to_csv(index=False),
    file_name=f"{data['video_id']}_sentiment_summary.csv",
    mime="text/csv"
)
st.divider()

st.subheader(
    "💬 Comments Dataset"
)
comments_df = pd.DataFrame(data["detailed_comments"])

# ==================================================
# SECTION 7 : Filters
# ==================================================

st.subheader(
    "🔍 Filters"
)
sentiment_filter = st.selectbox(
    "Filter by Sentiment",
    ["All", "Positive", "Neutral", "Negative"]
)
if sentiment_filter != "All":
    comments_df = comments_df[comments_df["sentiment"] == sentiment_filter]

# ==================================================
# SECTION 8 : Comments Dataset
# ==================================================

st.dataframe(comments_df, use_container_width=True)

# ==================================================
# SECTION 9 : Download Reports
# ==================================================

st.download_button(
    label="⬇️ Download Comments CSV",
    data=comments_df.to_csv(index=False),
    file_name=f"{data['video_id']}_comments_dataset.csv",
    mime="text/csv"
)
