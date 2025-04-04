import requests
import streamlit as st

# Load GitHub PAT securely
GITHUB_PAT = st.secrets["GITHUB_PAT"]
HEADERS = {"Authorization": f"token {GITHUB_PAT}"}


def get_user_profile():
    """Fetch authenticated user’s GitHub profile"""
    url = "https://api.github.com/user"
    res = requests.get(url, headers=HEADERS)
    if res.status_code == 200:
        return res.json()
    else:
        st.error("Failed to fetch GitHub profile.")
        return None



