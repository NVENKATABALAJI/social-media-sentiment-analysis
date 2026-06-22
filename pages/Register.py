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
    page_title="Register",
    page_icon="📝",
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

st.markdown(
"""
<div class="hero-card">
<h1 style="margin:0; font-size:42px;">
📝 Create Account
</h1>
<p style="color:#94A3B8; margin-top:10px;">
Create your Sentilytics workspace.
</p>
</div>
""",unsafe_allow_html=True
)

# ==================================================
# SECTION 4 : Registration Form
# ==================================================

st.markdown(
    "## 👤 New Account"
)
email = st.text_input(
    "📧 Email"
)
username = st.text_input(
    "👤 Username"
)
password = st.text_input(
    "🔒 Password",
    type="password"
)

# ==================================================
# SECTION 5 : Register Button
# ==================================================

register_clicked = st.button(
    "🚀 Create Account",
    use_container_width=True
)

# ==================================================
# SECTION 6 : Registration
# ==================================================

if register_clicked:
    if not email.strip():
        st.warning(
            "Please enter email."
        )
        st.stop()
    if not username.strip():
        st.warning(
            "Please enter username."
        )
        st.stop()
    if not password.strip():
        st.warning(
            "Please enter password."
        )
        st.stop()
    payload = {
        "email": email,
        "username": username,
        "password": password
    }
    try:
        response = requests.post(
            "http://127.0.0.1:8000/register",
            json=payload
        )
        if response.status_code == 200:

            st.session_state[
                "registration_success"
            ] = True

        else:
            st.error(
                response.json()["detail"]
            )
    except Exception as e:
        st.error(
            f"❌ {e}"
        )
if st.session_state[
    "registration_success"
]:

    st.success(
        "✅ Account created successfully"
    )

    if st.button(
        "➡️ Go to Login",
        use_container_width=True
    ):

        st.session_state[
            "registration_success"
        ] = False

        st.switch_page(
            "pages/Login.py"
        )

# ==================================================
# SECTION 7 : Footer
# ==================================================

st.divider()
st.caption(
    "📊 Sentilytics | AI Social Intelligence Platform"
)