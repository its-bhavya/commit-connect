import requests
import streamlit as st


def get_user_profile(token):
    """Fetch authenticated user’s GitHub profile"""
    url = "https://api.github.com/user"
    headers = {"Authorization": f"token {token}"}
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        return res.json()
    else:
        st.error("Failed to fetch GitHub profile.")
        return None
    
# Function to fetch repositories of the authenticated user
def get_user_repos(token):
    headers = {"Authorization": f"token {token}"}
    repos_url = "https://api.github.com/user/repos"
    response = requests.get(repos_url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        st.error("❌ Failed to fetch repositories. Please check your token.")
        return None

# Function to count language usage across repositories
def get_language_distribution(repos):
    language_count = {}
    for repo in repos:
        language = repo.get("language")
        if language:
            language_count[language] = language_count.get(language, 0) + 1
    return language_count
