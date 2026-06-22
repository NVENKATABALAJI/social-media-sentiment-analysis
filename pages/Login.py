# ==================================================
# SECTION 1 : Imports
# ==================================================

import streamlit as st
import requests
from ui.theme import load_theme
from ui.session_manager import initialize_session

# ==================================================
# SECTION 2 : Page Config
# ==================================================

st.set_page_config(
    page_title="Login",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="collapsed"
)
load_theme()
initialize_session()
st.markdown("""
<style>
section[data-testid="stSidebar"]{
display:none;
}
button[kind="header"]{
display:none;
}
</style>
""",unsafe_allow_html=True)

# ==================================================
# SECTION 3 : Hero Card
# ==================================================

st.markdown("""
<div class="hero-card">
<h1 style="
margin:0;
font-size:42px;
">
🔐 Welcome Back
</h1>
<p style="
color:#94A3B8;
margin-top:10px;
">
Login to access your analytics workspace.
</p>
</div>
""", unsafe_allow_html=True)

# ==================================================
# SECTION 4 : Login Form
# ==================================================

st.markdown(
    "## 👤 Account Login"
)
email = st.text_input(
    "📧 Email"

)
password = st.text_input(
    "🔒 Password",
    type="password"
)

# ==================================================
# SECTION 5 : Login Button
# ==================================================

login_clicked = st.button(
    "🚀 Login",
    use_container_width=True
)

# ==================================================
# SECTION 6 : Authentication
# ==================================================

if login_clicked:
    if not email.strip():
        st.warning(
            "Please enter email."
        )
        st.stop()
    if not password.strip():
        st.warning(
            "Please enter password."
        )
        st.stop()
    try:
        response = requests.post(
            "http://127.0.0.1:8000/login",
            data={
                "username": email,
                "password": password
            }
        )
        if response.status_code != 200:
            st.error(
                response.json()["detail"]
            )
        else:
            token = response.json()[
                "access_token"
            ]
            st.session_state["access_token"] = token

            st.session_state[
                "username"
            ] = email.split("@")[0]

            st.switch_page(
                "pages/Dashboard.py"
            )
    except Exception as e:
        st.error(
            f"❌ {e}"
        )

# ==================================================
# SECTION 7 : Footer
# ==================================================

st.divider()
st.caption(
    "📊 Sentilytics | AI Social Intelligence Platform"
)