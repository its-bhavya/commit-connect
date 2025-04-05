import requests
import streamlit as st
from datetime import datetime, timedelta


# Store token here
token = None

def set_token(pat):
    global token
    token = pat


def get_user_profile():
    global token
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
def get_user_repos():
    global token
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

# fecting repo by language 

def search_repositories_by_language(languages=None, min_stars=0, recent_days=90):
    """
    Search public repositories on GitHub based on language, stars, and updated date.
    :param token: GitHub Personal Access Token
    :param languages: List of languages to filter repos
    :param min_stars: Minimum stars
    :param recent_days: Updated within recent_days
    :return: List of recommended repositories
    """
    global token
    if not languages:
        return {"error": "Please provide at least one language."}

    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    recent_cutoff = (datetime.utcnow() - timedelta(days=recent_days)).strftime("%Y-%m-%d")

    results = []
    for lang in languages:
        query = f"language:{lang} stars:>={min_stars} pushed:>={recent_cutoff}"
        url = f"https://api.github.com/search/repositories?q={query}&sort=stars&order=desc&per_page=20"

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            results.extend(data.get("items", []))
        else:
            print(f"Error for {lang}: {response.status_code} - {response.json().get('message', '')}")

    return results