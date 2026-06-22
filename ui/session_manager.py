# ==================================================
# SECTION 1 : Imports
# ==================================================

import streamlit as st


# ==================================================
# SECTION 2 : Default Values
# ==================================================

DEFAULTS = {

    "access_token": None,

    "logged_in": False,

    "registration_success": False,

    "analysis_data": None,

    "video_id": None,

    "loaded_analysis": None
}


# ==================================================
# SECTION 3 : Initialize
# ==================================================

def initialize_session():

    for key, value in DEFAULTS.items():

        if key not in st.session_state:

            st.session_state[key] = value


# ==================================================
# SECTION 4 : Logout
# ==================================================

def logout():

    st.session_state.clear()

    st.switch_page("app.py")