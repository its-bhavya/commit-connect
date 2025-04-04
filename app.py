import streamlit as st
import requests
import matplotlib.pyplot as plt
from utils.github_api import get_user_profile, get_user_repos, get_language_distribution
from utils.github_api import search_repositories_by_language
from gemini import parse_user_prompt, get_filters, build_issue_query, find_github_issues
from display_issues import display_issues

# Set Page Title and Layout
st.set_page_config(page_title="Commit-Connect", page_icon="🔍", layout="wide")

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to:", ["Home", "GitHub Login", "Your Top Languages","Project by Language", "Find Projects", "Profile Visualization"])

# Home Page
if page == "Home":
    st.title("🔍 Commit-Connect")
    st.write("Find open-source projects that match your skills!")

# GitHub Login Page
elif page == "GitHub Login":
    st.title("🔑 Log in with GitHub")
    st.write("Enter your GitHub Personal Access Token (PAT) to proceed.")

    if "help_visible" not in st.session_state:
        st.session_state.help_visible = False
    if "pat" not in st.session_state:
        st.session_state.pat = ""

    col1, col2 = st.columns([2, 1])

    with col1:
        pat = st.text_input("🔐 GitHub Personal Access Token", type="password", key="github_pat")

    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("❓ Help"):
            st.session_state.help_visible = not st.session_state.help_visible

    if st.session_state.help_visible:
        st.markdown(
            """
            <div style="border-radius: 10px; background-color: #1e293b; padding: 15px; color: white;">
                <h4>🔑 How to Generate a GitHub PAT?</h4>
                <ol>
                    <li>Go to <a href="https://github.com/settings/tokens" target="_blank">GitHub Tokens</a></li>
                    <li>Click <b>'Generate new token'</b></li>
                    <li>Select <b>'repo'</b> and <b>'read:user'</b> scopes</li>
                    <li>Copy and paste it here</li>
                </ol>
            </div>
            """,
            unsafe_allow_html=True,
        )

    if st.button("Login"):
        if pat:
            user_data = get_user_profile(pat)
            if user_data:
                st.session_state.pat = pat  # Store PAT in session state
                st.success(f"Logged in as {user_data['login']}")

                st.image(user_data["avatar_url"], width=100)
                st.write(f"**Name:** {user_data.get('name', 'N/A')}")
                st.write(f"**Bio:** {user_data.get('bio', 'N/A')}")
                st.write(f"**Public Repos:** {user_data['public_repos']}")
                st.write(f"**Followers:** {user_data['followers']} | **Following:** {user_data['following']}")
            else:
                st.error("Invalid Token! Please check and try again.")
        else:
            st.warning("Please enter your GitHub Personal Access Token.")

# Your Top Languages Page
elif page == "Your Top Languages":
    st.title("📊 Your Top Languages")
    st.write("This section will display your most used programming languages.")

    # Check if PAT exists in session state
    if "pat" in st.session_state and st.session_state.pat:
        pat = st.session_state.pat

        # Fetch and process languages
        repos = get_user_repos(pat)
        if repos:
            lang_data = get_language_distribution(repos)

            if lang_data:
                # Display as a pie chart
                st.subheader("🛠 Your Top Programming Languages")
                fig, ax = plt.subplots()
                ax.pie(lang_data.values(), labels=lang_data.keys(), autopct="%1.1f%%", startangle=140, colors=plt.cm.Paired.colors)
                ax.axis("equal")  # Ensures pie chart is circular
                st.pyplot(fig)
            else:
                st.info("No language data found in your repositories.")
    else:
        st.warning("Please log in first on the 'GitHub Login' page.")


# project by languages
elif page == "Project by Language":
    st.title("🎯 Repositories by Language")

    pat = st.text_input("Enter your GitHub Personal Access Token (PAT)", type="password", key="lang_pat")

    selected_languages = st.multiselect(
        "Select languages you want to filter by:",
        ["Python", "JavaScript", "Java", "HTML", "C++", "Go", "C", "TypeScript"]
    )

    min_stars = st.slider("⭐ Minimum Stars", 0, 50, 0)
    recent_days = st.slider("🕒 Updated Within (days)", 0, 365, 90)

    if st.button("🔍 Fetch Repositories"):
        if pat and selected_languages:
            repos = search_repositories_by_language(pat, selected_languages, min_stars, recent_days)

            if "error" in repos:
                st.error(repos["error"])
            elif len(repos) == 0:
                st.info("No repositories matched the selected filters.")
            else:
                st.success(f"Found {len(repos)} repositories:")
                for repo in repos:
                    st.markdown(f"🔗 [{repo['name']}]({repo['html_url']}) — ⭐ {repo['stargazers_count']} | 🧠 {repo['language']} | 🕒 Updated: {repo['updated_at'][:10]}")
        else:
            st.warning("Please enter your token and select at least one language.")

# Find Projects Page
elif page == "Find Projects":
    st.title("🔎 Find Open Source Projects")
    st.write("This section will help you find open-source issues to contribute to.")
    prompt = st.chat_input("What kind of projects are you looking for to contribute? ")
    if prompt:
        result = parse_user_prompt(prompt)
        #st.write(result)
        languages, frameworks_libraries, tools, difficulty, filters = get_filters(prompt)
        #query, query_url = build_issue_query(languages, frameworks_libraries, tools, difficulty, filters)
        #st.write(query)
        json_data = find_github_issues(user_input=prompt)
        total_issues = len(json_data)

        if languages:
            languages = ','.join(languages).title()
        if frameworks_libraries:
            frames = ','.join(frameworks_libraries).title()
        if tools:
            tools = ','.join(tools).title()
        if filters:
            filters = ",".join(filters).title()
        
        st.markdown(f"### Showing {total_issues} issues")
        display_issues(json_data)

# Profile Visualization Page
elif page == "Profile Visualization":
    st.title("📊 Visualize Your GitHub Profile")
    st.write("This section will generate interactive visualizations of your GitHub activity.")
