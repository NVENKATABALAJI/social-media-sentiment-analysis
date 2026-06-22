# ==================================================
# SECTION 1 : Imports
# ==================================================

import streamlit as st
import requests
import re
from ui.theme import load_theme
from ui.shell import (
    render_header,
    render_navigation,
    render_footer,
    render_logout,
    render_cta
)
from ui.auth_guard import (
    require_login,
    get_auth_headers
)
from ui.session_manager import initialize_session

# ==================================================
# SECTION 2 : Helper Functions
# ==================================================

def load_current_user():
    try:
        response = requests.get(
            "http://127.0.0.1:8000/me",
            headers=get_auth_headers()
        )
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return None
def load_dashboard_stats():
    try:
        response = requests.get(
            "http://127.0.0.1:8000/dashboard/stats",
            headers=get_auth_headers()
        )
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return None
def load_recent_analyses():
    try:
        response = requests.get(
            "http://127.0.0.1:8000/history",
            headers=get_auth_headers()
        )
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return []

# ==================================================
# SECTION 3 : Page Config
# ==================================================

st.set_page_config(
    page_title="YouTube Sentiment Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)
load_theme()
initialize_session()
require_login()
render_header()
render_navigation()

# ==================================================
# SECTION 4 : Authentication Check
# ==================================================


# ==================================================
# SECTION 5 : Load User Data
# ==================================================

user = load_current_user()
stats = load_dashboard_stats()
if "recent_videos" not in st.session_state:
    st.session_state["recent_videos"] = []
recent_history = load_recent_analyses()

# ==================================================
# SECTION 6 : Hero Section
# ==================================================

if user:

    st.markdown(f"""

    <div class="hero-card">

        <div style="display:flex;justify-content:space-between;">

            <div>

                <div class="hero-badge">

                    🚀 AI Analytics Workspace

                </div>

                <h1>

                    Welcome back,

                    {user['username']}

                </h1>

                <p>

                    Monitor audience reactions,

                    measure engagement and

                    discover actionable insights.

                </p>

            </div>

            <div>

                <h2>

                    🟢 Live

                </h2>

            </div>

        </div>

    </div>

    """,

    unsafe_allow_html=True
    )

# ==================================================
# SECTION 7 : Dashboard Stats
# ==================================================

if stats:
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Analyses</div>
            <div class="metric-value">{stats['total_analyses']}</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Videos</div>
            <div class="metric-value">{stats['unique_videos']}</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Avg Score</div>
            <div class="metric-value">
            {stats['average_engagement_score']}%
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-title">Status</div>
            <div class="metric-value">Live</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown(
        """
        <hr style="
        border:1px solid #1E293B;
        margin-top:25px;
        margin-bottom:25px;
        ">
        """,
        unsafe_allow_html=True
    )

# ==================================================
# SECTION 8 : Sidebar
# ==================================================



# ==================================================
# SECTION 9 : Utility Functions
# ==================================================

def extract_video_id(url_or_id: str) -> str:
    pattern = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
    match = re.search(pattern, url_or_id)
    return match.group(1) if match else url_or_id
def call_backend(video_id: str):
    """Safe API call with error handling"""
    try:
        resp = requests.get(
            f"http://127.0.0.1:8000/analyze/{video_id}",
            headers=get_auth_headers(),
            timeout=20
        )
        if resp.status_code != 200:
            # Try to read backend error
            try:
                detail = resp.json().get("detail", "Unknown error")
            except Exception:
                detail = resp.text
            raise Exception(detail)
        return resp.json()
    except requests.exceptions.ConnectionError:
        raise Exception("Backend not running. Start FastAPI server on port 8000.")
    except requests.exceptions.Timeout:
        raise Exception("Backend timeout. Try again or reduce comments fetched.")
    except Exception as e:
        raise Exception(str(e))
st.markdown("""

<h2 class="section-heading">

🎯 Analysis Workspace

</h2>

""",

unsafe_allow_html=True
)
st.markdown("<br>", unsafe_allow_html=True)
# ==================================================
# SECTION 10 : Analyze Video Input
# ==================================================

st.markdown("""
<div class="dashboard-card">
<h2>
🎬 Analyze New Video
</h2>
<p style="color:#94A3B8;">
Paste a YouTube URL or Video ID to generate AI-powered sentiment insights.
</p>
""", unsafe_allow_html=True)
user_input = st.text_input(
    "🔗 Paste YouTube Video URL or Video ID",
    key="video_input"
)
analyze_clicked = st.button(
    "🚀 Analyze Video",
    use_container_width=True
)
st.markdown("</div>", unsafe_allow_html=True)
if analyze_clicked:
    if not user_input.strip():
        st.warning(
            "⚠️ Please enter a YouTube URL or Video ID"
        )
        st.stop()

    video_id = extract_video_id(user_input)
    with st.spinner("🔍 Analyzing YouTube comments..."):
        try:
            data = call_backend(video_id)
        except Exception as e:
            st.error(f"❌ {e}")
            st.stop()
    st.session_state["analysis_data"] = data
    st.session_state["video_id"] = video_id
    if video_id not in st.session_state["recent_videos"]:
        st.session_state["recent_videos"].insert(

            0,

            video_id

        )

    st.session_state["recent_videos"] = (

        st.session_state["recent_videos"][:5]

    )
    st.success("Analysis completed!")

# ==================================================
# SECTION 11 : Analytics Snapshot
# ==================================================

data = st.session_state["analysis_data"]
if data:
    st.markdown("### 📋 Analysis Overview")

    dominant_sentiment = max(
        data["sentiment_counts"],
        key=data["sentiment_counts"].get
    )

    positive_rate = round(

        data["sentiment_counts"].get(
            "Positive",
            0
        ) / max(
            data["total_comments"],
            1
        ) * 100,

        1

    )

    overview1, overview2 = st.columns(2)

    with overview1:

        st.markdown("""

        <div class="dashboard-card">

        <h3>🎥 Video Information</h3>

        """,

        unsafe_allow_html=True)

        st.metric(

            "Video ID",

            st.session_state.get(

                "video_id",

                "N/A"

            )

        )

        st.metric(

            "Comments",

            data.get(

                "total_comments",

                0

            )

        )

        st.metric(

            "Positive Rate",

            f"{positive_rate}%"

        )

        st.markdown(

            "</div>",

            unsafe_allow_html=True

        )

    with overview2:

        st.markdown("""

        <div class="dashboard-card">

        <h3>📈 Platform Summary</h3>

        """,

        unsafe_allow_html=True)

        st.metric(

            "Dominant Sentiment",

            dominant_sentiment

        )

        st.metric(

            "Engagement Score",

            data.get(

                "engagement_score",

                0

            )

        )

        st.metric(

            "Platform Status",

            "🟢 Live"

        )

        st.markdown(

            "</div>",

            unsafe_allow_html=True

        )

    st.divider()
    pos = data["sentiment_counts"].get("Positive",0)
    neu = data["sentiment_counts"].get("Neutral",0)
    neg = data["sentiment_counts"].get("Negative",0)
    total = max(pos+neu+neg,1)
    st.markdown("### 📊 Analytics Snapshot")
    left,right = st.columns(2)

    # LEFT CARD

    with left:
        st.markdown("""
        <div class="dashboard-card">
        <h3>😊 Sentiment Summary</h3>
        """, unsafe_allow_html=True)
        st.metric(
            "Positive",
            pos,
            f"{round(pos/total*100,1)}%"
        )
        st.progress(pos / total)
        st.metric(
            "Neutral",
            neu,
            f"{round(neu/total*100,1)}%"
        )
        st.progress(neu / total)
        st.metric(
            "Negative",
            neg,
            f"{round(neg/total*100,1)}%"
        )
        st.progress(neg / total)
        st.markdown("</div>", unsafe_allow_html=True)

    # RIGHT CARD

    with right:
        st.markdown("""
        <div class="dashboard-card">
        <h3>📈 Analysis Summary</h3>
        """, unsafe_allow_html=True)
        st.metric(
            "Comments Analyzed",
            data.get("total_comments",0)
        )
        st.metric(
            "Engagement Score",
            data.get("engagement_score",0)
        )
        st.markdown("</div>", unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="dashboard-card">
    <h3>
    🎥 Ready to Analyze
    </h3>
    <p style="color:#94A3B8;">
    Follow these steps:
    </p>
    <ul style="line-height:2;">
    <li>
    ① Paste a YouTube URL
    </li>
    <li>
    ② Click Analyze Video
    </li>
    <li>
    ③ Explore Charts
    </li>
    <li>
    ④ Review Comments
    </li>
    <li>
    ⑤ Export Reports
    </li>
    </ul>
    </div>
    """,unsafe_allow_html=True)
st.markdown("""

<h2 class="section-heading">

⚙️ Workspace Center

</h2>

""",

unsafe_allow_html=True
)
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""

<div class="section-banner">

⚡ Quick Actions

</div>

""",

unsafe_allow_html=True
)
col1,col2,col3,col4 = st.columns(4)
with col1:
    st.page_link(
        "pages/Charts.py",
        label="📊 Open Charts",
        use_container_width=True
    )
with col2:
    st.page_link(
        "pages/Comments.py",
        label="💬 Open Comments",
        use_container_width=True
    )
with col3:

    st.page_link(

        "pages/History.py",

        label="🕒 Open History",

        use_container_width=True

    )

with col4:

    st.page_link(

        "pages/Downloads.py",

        label="📥 Export Data",

        use_container_width=True

    )

st.divider()
if st.session_state["recent_videos"]:

    st.markdown("""

    <div class="section-banner">

    🕒 Recently Analyzed Videos

    </div>

    """,

                unsafe_allow_html=True
                )

    for index, video in enumerate(

        st.session_state["recent_videos"],

        start=1

    ):

        st.markdown(

            f"{index}. `{video}`"

        )

    st.divider()

# ==================================================
# SECTION 12 : Recent Analyses
# ==================================================

st.markdown("""

<div class="section-banner">

🕒 Recent Analyses

</div>

""",

unsafe_allow_html=True
)

if recent_history:

    rows = []

    for item in recent_history[:5]:

        rows.append(

            {

                "Video ID":

                item.get(

                    "youtube_video_id",

                    "N/A"

                ),

                "Comments":

                item.get(

                    "total_comments",

                    0

                ),

                "Engagement":

                item.get(

                    "engagement_score",

                    0

                ),

                "Analysis ID":

                item.get(

                    "analysis_id",

                    "N/A"

                )

            }

        )

    st.dataframe(

        rows,

        use_container_width=True,

        hide_index=True

    )

else:

    st.info(

        "No analyses available yet."

    )
    st.divider()

# ==================================================
# SECTION 13 : Footer
# ==================================================
render_cta()

render_logout()

render_footer()