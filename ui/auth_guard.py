# ==================================================
# SECTION 1 : Imports
# ==================================================

import streamlit as st

# ==================================================
# SECTION 2 : Require Login
# ==================================================

def require_login():
    if "access_token" not in st.session_state:
        st.warning(
            "🔒 Please login first."
        )
        st.switch_page(
            "pages/Login.py"
        )
        st.stop()

# ==================================================
# SECTION 3 : Auth Headers
# ==================================================

def get_auth_headers():
    return {
        "Authorization":
        f"Bearer {st.session_state['access_token']}"
    }