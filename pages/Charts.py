import streamlit as st
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import re
from ui.theme import load_theme
from ui.auth_guard import require_login
from ui.shell import render_sidebar
from ui.session_manager import initialize_session

st.set_page_config(
    page_title="Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)
load_theme()
initialize_session()
render_sidebar()
require_login()

st.markdown("""
<div class="hero-card">
<h1>
📊 Analytics Intelligence
</h1>
<p class="page-subtitle">
Transform audience reactions into actionable insights.
</p>
</div>
""",unsafe_allow_html=True)

# ------------------ Check Data ------------------

if not st.session_state.get("analysis_data"):
    st.markdown("""

    <div class="dashboard-card">

    <h3>

    🎬 No Analysis Available

    </h3>

    <p>

    Analyze a video from Dashboard to unlock Analytics.

    </p>

    </div>

    """,

                unsafe_allow_html=True)

    st.stop()

data = st.session_state["analysis_data"]
st.markdown("""

<h2 class="section-title">
📈 Analytics Overview
</h2>
""",unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
total_comments = data.get(
    "total_comments",
    0
)
positive = data["sentiment_counts"].get(
    "Positive",
    0
)
negative = data["sentiment_counts"].get(
    "Negative",
    0
)
with c1:
    st.markdown(f"""
    <div class="metric-card">
    <div class="metric-title">
    Comments Analyzed
    </div>
    <div class="metric-value">
    {total_comments}
    </div>
    </div>
    """,unsafe_allow_html=True)

with c2:

    st.markdown(f"""

    <div class="metric-card">

    <div class="metric-title">

    Positive Comments

    </div>

    <div class="metric-value">

    {positive}

    </div>

    </div>

    """,

    unsafe_allow_html=True)

with c3:

    st.markdown(f"""

    <div class="metric-card">

    <div class="metric-title">

    Negative Comments

    </div>

    <div class="metric-value">

    {negative}

    </div>

    </div>

    """,

    unsafe_allow_html=True)
st.divider()

# ------------------ Common Colors ------------------

colors = {
    "Positive": "#22c55e",   # green
    "Neutral": "#3b82f6",    # blue
    "Negative": "#ef4444"    # red
}
st.markdown("""
<h2 class="section-title">
😊 Sentiment Intelligence
</h2>
""",unsafe_allow_html=True)

# ------------------ PIE CHART ------------------

col1, col2 = st.columns(2)
labels = list(data["sentiment_percentages"].keys())
values = list(data["sentiment_percentages"].values())
pie_colors = [colors[label] for label in labels]
fig1, ax1 = plt.subplots(
    figsize=(6, 6)
)
ax1.pie(
    values,
    labels=labels,
    autopct="%1.1f%%",
    startangle=90,
    colors=pie_colors,
    wedgeprops={
        "width": 0.45
    },
    textprops={
        "color": "#020826"
    }
)
ax1.axis("equal")


with col1:
    st.markdown("""
    <div class="chart-card">
    <div class="chart-title">
    📈 Sentiment Distribution
    </div>
    """, unsafe_allow_html=True)
    st.pyplot(fig1)
    st.markdown("</div>", unsafe_allow_html=True)

# ------------------ BAR CHART ------------------

labels = list(data["sentiment_counts"].keys())
values = list(data["sentiment_counts"].values())

bar_colors = [colors[label] for label in labels]

fig2, ax2 = plt.subplots()

ax2.bar(labels, values, color=bar_colors)
ax2.set_ylabel(
    "Comments",
    color="#020826"
)

ax2.grid(
    axis="y",
    alpha=0.25
)


ax2.tick_params(colors="#020826")



with col2:

    st.markdown("""
    <div class="chart-card">
    <div class="chart-title">
    📊 Sentiment Comparison
    </div>
    """, unsafe_allow_html=True)

    st.pyplot(fig2)

    st.markdown("</div>", unsafe_allow_html=True)
st.markdown("""

<h2 class="section-title">

🎭 Emotion Intelligence

</h2>

""",

unsafe_allow_html=True)
emotion_left, emotion_right = st.columns(2)


# ------------------ EMOTION PIE CHART ------------------


emotion_counts = data.get("emotion_counts", {})

emotion_labels = list(emotion_counts.keys())
emotion_values = list(emotion_counts.values())
if not emotion_values:
    emotion_labels = ["No Data"]
    emotion_values = [1]
emotion_colors = [
    "#22c55e",  # Joy
    "#ef4444",  # Anger
    "#3b82f6",  # Sadness
    "#f59e0b",  # Fear
    "#a855f7",  # Surprise
    "#ec4899",  # Love
    "#84cc16",  # Disgust
    "#6b7280"   # Neutral
]

fig3, ax3 = plt.subplots(
    figsize=(6,6)
)

ax3.pie(
    emotion_values,
    labels=None,
    autopct="%1.1f%%",
    pctdistance=0.7,
    startangle=90,
    colors=emotion_colors[:len(emotion_labels)]
)

ax3.legend(
    emotion_labels,
    loc="center left",
    bbox_to_anchor=(1, 0.5),
    frameon=False
)

ax3.axis("equal")


with emotion_left:

    st.markdown("""
    <div class="chart-card">
    <div class="chart-title">
    🎭 Emotion Distribution
    </div>
    """, unsafe_allow_html=True)

    st.pyplot(fig3)

    st.markdown("</div>", unsafe_allow_html=True)


# ------------------ BAR CHART ------------------


# ------------------ EMOTION BAR CHART ------------------


fig4, ax4 = plt.subplots()
ax4.bar(emotion_labels, emotion_values, color=emotion_colors[:len(emotion_labels)])
ax4.set_ylabel(
    "Comments",
    color="#020826"
)
ax4.tick_params(
    colors="#020826"
)
ax4.grid(
    axis="y",
    alpha=0.25
)
with emotion_right:

    st.markdown("""
    <div class="chart-card">
    <div class="chart-title">
    📊 Emotion Comparison
    </div>
    """, unsafe_allow_html=True)

    st.pyplot(fig4)

    st.markdown("</div>", unsafe_allow_html=True)


st.markdown("""

<h2 class="section-title">

☁️ Audience Vocabulary

</h2>

""",

unsafe_allow_html=True)
# ------------------ WORD CLOUD ------------------

st.markdown("""
<div class="chart-card">
<div class="chart-title">
☁️ Audience Word Cloud
</div>
""", unsafe_allow_html=True)

# Simple stopwords (no nltk dependency)
STOPWORDS = {
    "the","is","and","to","in","it","of","for","on","this","that",
    "with","as","was","are","but","be","have","you","i"
}

def clean_text(text):
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^A-Za-z ]+", "", text)
    text = text.lower()
    return " ".join(w for w in text.split() if w not in STOPWORDS and len(w) > 2)

comments = data.get(
    "detailed_comments",
    []
)

text_blob = " ".join(
    clean_text(
        c.get("comment", "")
    )
    for c in comments
)
if not text_blob.strip():
    st.markdown("""
    <div class="dashboard-card">
    <h3>
    📭 No Vocabulary Available
    </h3>
    <p>
    No audience keywords were detected.
    </p>
    </div>
    """,unsafe_allow_html=True)
else:
    wc = WordCloud(
        width=800,
        height=400,
        background_color="#f9f4ef",
        colormap="viridis"
    ).generate(text_blob)
    fig_wc, ax_wc = plt.subplots(figsize=(12, 4))
    ax_wc.imshow(wc, interpolation="bilinear")
    ax_wc.axis("off")
    st.pyplot(fig_wc)

st.markdown("""
<div class="hero-card">
<h2>
🚀 Insight Center
</h2>
<p>
Use Charts together with Comments and History to understand audience behaviour patterns.
</p>
</div>
""",unsafe_allow_html=True)

st.markdown("""
<div class="footer">
© 2026 Sentilytics
<br>
AI Social Intelligence Platform
</div>
""",unsafe_allow_html=True)