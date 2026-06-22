import streamlit as st
from ui.session_manager import logout


# ==================================================
# HEADER
# ==================================================

def render_header():

    username = st.session_state.get(
        "username",
        "Guest"
    )

    st.markdown(f"""

    <div class="app-header">

        <div class="header-left">

            <div class="logo-circle">

                🧠

            </div>

            <div>

                <div class="brand-name">

                    Sentilytics

                </div>

                <div class="brand-subtitle">

                    AI Social Intelligence Platform

                </div>

            </div>

        </div>

        <div class="header-right">

            <div class="notification">

                🔔

            </div>

            <div class="profile-pill">

                👤 {username}

            </div>

        </div>

    </div>

    """,

    unsafe_allow_html=True
    )


# ==================================================
# NAVIGATION
# ==================================================

def render_navigation():

    st.markdown("### Navigation")

    col1,col2,col3,col4,col5 = st.columns(5)

    with col1:

        st.page_link(
            "pages/Dashboard.py",
            label="📈 Dashboard",
            use_container_width=True
        )

    with col2:

        st.page_link(
            "pages/Charts.py",
            label="📊 Charts",
            use_container_width=True
        )

    with col3:

        st.page_link(
            "pages/Comments.py",
            label="💬 Comments",
            use_container_width=True
        )

    with col4:

        st.page_link(
            "pages/History.py",
            label="🕒 History",
            use_container_width=True
        )

    with col5:

        st.page_link(
            "pages/Downloads.py",
            label="📥 Downloads",
            use_container_width=True
        )

    st.markdown("<br>", unsafe_allow_html=True)


# ==================================================
# CTA SECTION
# ==================================================

def render_cta():

    st.markdown("""

    <div class="dashboard-card">

        <h2>

        🚀 Unlock Better Audience Insights

        </h2>

        <p>

        Analyze videos, discover audience emotions,
        measure engagement and make smarter content decisions.

        </p>

    </div>

    """,

    unsafe_allow_html=True
    )


# ==================================================
# FOOTER
# ==================================================

def render_footer():

    st.markdown("""

    <div class="footer">

        <h3>

        🧠 Sentilytics

        </h3>

        <p>

        AI-powered YouTube sentiment analytics platform.

        </p>

        <p>

        © 2026 Sentilytics

        </p>

    </div>

    """,

    unsafe_allow_html=True
    )


# ==================================================
# LOGOUT
# ==================================================

def render_logout():

    col1,col2,col3 = st.columns([8,2,2])

    with col3:

        if st.button(

            "🚪 Logout",

            use_container_width=True

        ):

            logout()