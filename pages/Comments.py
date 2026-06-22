# ==================================================
# SECTION 1 : Imports
# ==================================================

import streamlit as st
import html
from ui.shell import render_sidebar
from ui.auth_guard import require_login
from ui.session_manager import initialize_session

# ==================================================
# SECTION 2 : Page Config & Styling
# ==================================================

st.set_page_config(page_title="Comments")
st.markdown("""
<style>
.comment-card{
    background:#111827;
    border:1px solid #253247;
    border-radius:16px;
    padding:18px;
    margin-bottom:14px;
    max-height:220px;
    overflow-y:auto;
}
</style>
""", unsafe_allow_html=True)
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
💬 Comment Explorer
</h1>
<p style="
color:#94A3B8;
margin-top:10px;
">
Browse all analyzed comments and audience reactions.
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
comments = data["detailed_comments"]

# ==================================================
# SECTION 5 : Analysis Summary
# ==================================================

total_comments = len(comments)
positive_count = len(
    [c for c in comments if c["sentiment"] == "Positive"]
)
negative_count = len(
    [c for c in comments if c["sentiment"] == "Negative"]
)
neutral_count = len(
    [
        c for c in comments
        if c["sentiment"] == "Neutral"
    ]
)
st.markdown("## 📈 Analysis Summary")
c1,c2,c3,c4 = st.columns(4)
with c1:
    st.metric(
        "Comments",
        total_comments
    )
with c2:
    st.metric(
        "Positive",
        positive_count
    )
with c3:
    st.metric(
        "Neutral",
        neutral_count
    )
with c4:
    st.metric(
        "Negative",
        negative_count
    )
st.divider()
st.markdown("<br>", unsafe_allow_html=True)

# ==================================================
# SECTION 6 : Filters
# ==================================================

emotion_labels = list(
    {
        c.get(
            "emotion",
            "Unknown"
        )
        for c in comments
    }
)
st.markdown("## 🔍 Filters")
f1,f2,f3 = st.columns(3)
with f1:
    sentiment_filter = st.selectbox(
        "Sentiment",
        [
            "All",
            "Positive",
            "Neutral",
            "Negative"
        ]
    )
with f2:
    emotion_filter = st.selectbox(
        "Emotion",
        ["All"] + emotion_labels
    )
with f3:
    search_box = st.text_input(
        "Search comments"
    )

# ==================================================
# SECTION 7 : Filter Logic
# ==================================================

filtered = comments
if sentiment_filter != "All":
    filtered = [
        c for c in filtered
        if c["sentiment"]
        == sentiment_filter
    ]
if emotion_filter != "All":
    filtered = [
        c for c in filtered
        if c.get("emotion")
        == emotion_filter
    ]
if search_box:
    filtered = [
        c for c in filtered
        if search_box.lower()
        in c["comment"].lower()
    ]

# ==================================================
# SECTION 8 : Display Comments
# ==================================================

st.divider()
st.markdown(
    f"### 💬 Showing {len(filtered)} comments"
)
for c in filtered:
    sentiment = c["sentiment"]
    color = {
        "Positive":"#22c55e",
        "Neutral":"#3b82f6",
        "Negative":"#ef4444"
    }.get(
        sentiment,
        "#64748B"
    )
    st.markdown(
        f"""
        <div class="comment-card"
        style="border-left:4px solid {color};">
        <b>{sentiment}</b>
        <br><br>
        {html.escape(c["comment"])}
        <br><br>
        🎭 {c.get("emotion","Unknown")}
        </div>
        """,unsafe_allow_html=True
    )