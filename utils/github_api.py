import requests
import streamlit as st
from datetime import datetime, timedelta


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

# fecting repo by language 

def fetch_user_repositories_by_language(token, languages=None, min_stars=0, recent_days=90):
    """
    Fetch the authenticated user's repositories filtered by language, stars, and updated date.
    :param token: GitHub Personal Access Token
    :param languages: List of languages to filter repos
    :param min_stars: Minimum number of stars the repo should have
    :param recent_days: How recent (in days) the repo should have been updated
    :return: List of filtered repositories or error
    """
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    url = "https://api.github.com/user/repos?per_page=100"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return {"error": f"Failed to fetch repos: {response.status_code} — {response.json().get('message', '')}"}

    all_repos = response.json()
    if not languages:
        languages = []

    recent_cutoff = datetime.utcnow() - timedelta(days=recent_days)

    filtered = [
        repo for repo in all_repos
        if repo["language"] and repo["language"].lower() in [lang.lower() for lang in languages]
        and repo["stargazers_count"] >= min_stars
        and datetime.strptime(repo["updated_at"], "%Y-%m-%dT%H:%M:%SZ") > recent_cutoff
    ]
    return filtered