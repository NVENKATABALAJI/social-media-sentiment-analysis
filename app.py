# ==================================================
# SECTION 1 : Imports
# ==================================================

import streamlit as st
from ui.theme import load_theme
from ui.session_manager import initialize_session

# ==================================================
# SECTION 2 : Page Config
# ==================================================

st.set_page_config(
    page_title="Sentilytics",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

load_theme()
initialize_session()

# ==================================================
# SECTION 3 : Hero Banner
# ==================================================

left,right = st.columns([1.6,1])

with left:

    st.markdown("""

    <div class="hero-card">

    <h1 style="
    font-size:64px;
    margin:0;
    ">

    🧠 Sentilytics

    </h1>

    <h2 style="
    color:#A5B4FC;
    margin-top:10px;
    ">

    Understand Your Audience
    Before Your Competitors Do.

    </h2>

    <p style="
    color:#94A3B8;
    font-size:20px;
    line-height:1.8;
    ">

    AI-powered social intelligence platform
    for creators, marketers and businesses.

    Analyze audience sentiment, emotions,
    engagement and discover actionable insights
    in seconds.

    </p>

    </div>

    """,

    unsafe_allow_html=True
    )

with right:

    st.markdown("""

    <div class="dashboard-card">

    <h3>

    📈 Platform Highlights

    </h3>

    <br>

    <h2>

    ⚡ Real-time Analysis

    </h2>

    <p style="color:#94A3B8;">

    Analyze audience reactions instantly.

    </p>

    <br>

    <h2>

    🎭 Emotion Detection

    </h2>

    <p style="color:#94A3B8;">

    Discover audience emotions.

    </p>

    <br>

    <h2>

    🚀 Engagement Prediction

    </h2>

    <p style="color:#94A3B8;">

    Predict content performance.

    </p>

    </div>

    """,

    unsafe_allow_html=True
    )
# ==================================================
# SECTION 4 : Get Started
# ==================================================

st.markdown("## 🚀 Start Your Journey")

col1,col2,col3 = st.columns(3)

with col1:

    st.markdown("""

    <div class="dashboard-card">

    <h2>

    🔐 Login

    </h2>

    <p style="color:#94A3B8;">

    Already have an account?

    Access your workspace.

    </p>

    </div>

    """,

    unsafe_allow_html=True
    )

    st.page_link(

        "pages/Login.py",

        label="Open Workspace",

        use_container_width=True
    )

with col2:

    st.markdown("""

    <div class="dashboard-card">

    <h2>

    📝 Register

    </h2>

    <p style="color:#94A3B8;">

    Create a new account

    and start using Sentilytics.

    </p>

    </div>

    """,

    unsafe_allow_html=True
    )

    st.page_link(

        "pages/Register.py",

        label="Create Account",

        use_container_width=True
    )

with col3:

    st.markdown("""

    <div class="dashboard-card">

    <h2>

    🚀 Get Started

    </h2>

    <p style="color:#94A3B8;">

    Explore the platform

    and begin your first analysis.

    </p>

    </div>

    """,

    unsafe_allow_html=True
    )

    st.page_link(

        "pages/Login.py",

        label="Start Exploring",

        use_container_width=True
    )

# ==================================================
# SECTION 5 : Why Choose Sentilytics
# ==================================================

st.markdown("## ⭐ Why Choose Sentilytics")

col1,col2,col3,col4 = st.columns(4)

with col1:

    st.markdown("""

    <div class="metric-card">

    <h2>⚡</h2>

    <h4>Real-Time AI</h4>

    <p style="color:#94A3B8;">

    Analyze audience reactions instantly.

    </p>

    </div>

    """,

    unsafe_allow_html=True
    )

with col2:

    st.markdown("""

    <div class="metric-card">

    <h2>🎭</h2>

    <h4>Emotion Detection</h4>

    <p style="color:#94A3B8;">

    Discover audience emotions.

    </p>

    </div>

    """,

    unsafe_allow_html=True
    )

with col3:

    st.markdown("""

    <div class="metric-card">

    <h2>📈</h2>

    <h4>Actionable Insights</h4>

    <p style="color:#94A3B8;">

    Transform data into decisions.

    </p>

    </div>

    """,

    unsafe_allow_html=True
    )

with col4:

    st.markdown("""

    <div class="metric-card">

    <h2>🔒</h2>

    <h4>Secure Workspace</h4>

    <p style="color:#94A3B8;">

    Safe and protected experience.

    </p>

    </div>

    """,

    unsafe_allow_html=True
    )

# ==================================================
# SECTION 6 : Trusted By Numbers
# ==================================================

st.markdown("## 📊 Trusted By Numbers")

col1,col2,col3,col4 = st.columns(4)

with col1:

    st.markdown("""

    <div class="metric-card">

    <h2>500+</h2>

    <p>Videos Analyzed</p>

    </div>

    """,

    unsafe_allow_html=True)

with col2:

    st.markdown("""

    <div class="metric-card">

    <h2>50K+</h2>

    <p>Comments Processed</p>

    </div>

    """,

    unsafe_allow_html=True)

with col3:

    st.markdown("""

    <div class="metric-card">

    <h2>85%</h2>

    <p>Prediction Accuracy</p>

    </div>

    """,

    unsafe_allow_html=True)

with col4:

    st.markdown("""

    <div class="metric-card">

    <h2>24/7</h2>

    <p>AI Availability</p>

    </div>

    """,

    unsafe_allow_html=True)

# ==================================================
# SECTION 7 : Footer
# ==================================================

st.markdown("""

<div class="footer">

© 2026 Sentilytics

<br>

AI Social Intelligence Platform

</div>

""",

unsafe_allow_html=True)