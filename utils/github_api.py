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
    

## Fetch User Details (username, profile)

import requests
import streamlit as st

GITHUB_API_URL = "https://api.github.com"
GITHUB_PAT = st.secrets["GITHUB_PAT"]

def get_user_profile():
    headers = {"Authorization": f"token {GITHUB_PAT}"}
    response = requests.get(f"{GITHUB_API_URL}/user", headers=headers)
    data = response.json()

    profile = {
        "username": data["login"],
        "name": data.get("name"),
        "bio": data.get("bio"),
        "avatar_url": data.get("avatar_url"),
        "html_url": data.get("html_url"),
        "location": data.get("location")
    }
    return profile



