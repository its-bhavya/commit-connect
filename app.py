import streamlit as st
import requests
import matplotlib.pyplot as plt
from gemini import parse_user_prompt, get_filters, build_issue_query, find_github_issues

# Set Page Title and Layout
st.set_page_config(page_title="Commit-Connect", page_icon="🔍", layout="wide")

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to:", ["Home", "GitHub Login", "Your Top Languages", "Find Projects", "Profile Visualization"])

# Function to get GitHub user info
def get_github_user_info(token):
    headers = {"Authorization": f"token {token}"}
    response = requests.get("https://api.github.com/user", headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        return None

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
            user_data = get_github_user_info(pat)
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

# Find Projects Page
elif page == "Find Projects":
    st.title("🔎 Find Open Source Projects")
    st.write("This section will help you find open-source issues to contribute to.")
    prompt = st.chat_input("What kind of projects are you looking for to contribute? ")
    if prompt:
        ans_dict = parse_user_prompt(prompt)
        #st.write(ans_dict)
        languages, frameworks_libraries, tools, difficulty, filters = get_filters(prompt)
        #st.write(languages, frameworks_libraries, tools, difficulty, filters)
        query, url= build_issue_query(languages, frameworks_libraries, tools, difficulty, filters)
        st.write(query)
        st.link_button(label="Click Here!", url=url)
        #ans = find_github_issues(prompt)
        #st.write(ans)


# Profile Visualization Page
elif page == "Profile Visualization":
    st.title("📊 Visualize Your GitHub Profile")
    st.write("This section will generate interactive visualizations of your GitHub activity.")



