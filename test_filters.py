import streamlit as st
from utils.github_api import (
    get_user_profile,
    get_user_repositories,
    extract_top_languages,
    search_repositories_by_language
)

st.set_page_config(page_title="Repository Finder", page_icon="🔍")
st.title("🔍 Explore Open-Source Repositories")
st.write("This is a test to check if Streamlit is running.")
try:
    profile = get_user_profile()
    username = profile.get("login")
    st.success(f"Welcome, **{username}**!")

    repos = get_user_repositories(username)
    top_languages = extract_top_languages(repos)

    if not top_languages:
        st.warning("No top languages found in your GitHub profile.")
    else:
        language = st.selectbox("📌 Select a language", top_languages)
        min_stars = st.slider("⭐ Minimum Stars", 0, 1000, 50)
        sort_option = st.selectbox("🗂️ Sort by", ["stars", "updated"])

        if st.button("🔎 Search Projects"):
            with st.spinner("Fetching repositories..."):
                projects = search_repositories_by_language(language, min_stars, sort=sort_option)

            if not projects:
                st.warning("No repositories found. Try changing filters.")
            else:
                for repo in projects:
                    st.markdown(f"""
                    ---  
                    ### [{repo['full_name']}]({repo['html_url']})
                    ⭐ **Stars**: {repo['stargazers_count']}  
                    🕒 **Last Updated**: {repo['updated_at']}  
                    📄 **Description**: {repo['description'] or 'No description'}  
                    """)
except Exception as e:
    st.error(f"❌ Error: {e}")
