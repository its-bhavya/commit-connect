import streamlit as st
import requests
import base64
import html

import pandas as pd
import matplotlib.pyplot as plt
from utils.github_api import set_token
from utils.github_api import get_user_profile, get_user_repos, get_language_distribution
from utils.github_api import search_repositories_by_language
from gemini import parse_user_prompt, get_filters, find_github_issues, summarize_issue

# Set Page Title and Layout
st.set_page_config(page_title="Commit-Connect", page_icon="🔍", layout="wide")

st.markdown(
    """
    <style>
    /* Sidebar base style */
    [data-testid="stSidebar"] {
        background-color: #0f0f0f;
        padding: 2rem 1rem;
        border-radius: 0 25px 25px 0;
        box-shadow: 4px 0 15px rgba(0,0,0,0.4);
        transition: all 0.3s ease;
    }

    /* Sidebar widgets */
    [data-testid="stSidebar"] * {
        color: #ffffff !important;
        font-family: 'Segoe UI', sans-serif;
        font-size: 3vh;
        padding-bottom: 0.5vh;
    }

    /* All Titles and Markdown Text*/
    h1 {
        color: white !important;
    }
    .stMarkdown h1, .stMarkdown p {
        color: white !important;
    }
    h2, h3, .stMarkdown h3, .stMarkdown h2, .block-container h2, section.main h2 ,, h4, .stMarkdown h4, h5, .stMarkdown h5, h6, .stMarkdown h6{
        color: white !important;
    }

    ul, ul li, ol, ol li {
        color: white !important;
    }

    /* Apply white to anything that might behave like a subheader */
    div[data-testid="stVerticalBlock"] h2 {
        color: white !important;
    }

    /* Make input label white */
    div[data-testid="stTextInput"] label {
        color: white !important;
    }

    /*Make selectbox label white*/
    div[data-testid="stMultiSelect"] label {
        color: white !important;
    }

    /*Make slider label white*/
    div[data-testid="stSlider"] label {
        color: white !important;
    }

    /* Style Streamlit warning box text */
    div[data-testid="stAlert"] * {
        color: #ffffff !important;
    }

    /* Optional: tweak background */
    div[data-testid="stAlert"] {
        background-color: rgba(255, 255, 150, 0.1) !important;
        border-left: 5px solid #facc15 !important;
        color: #ffffff;
    }
    a {
        color: white !important;
        text-decoration: underline; /* optional: makes links more visible */
    }

    /* Optional: change link color on hover */
    a:hover {
        color: #facc15 !important;  /* light yellow hover */
    }

    /* Make the top header bar transparent */
    header[data-testid="stHeader"] {
        background: transparent !important;
        box-shadow: none !important;
    }

    /* Make the buttons and icons in the header white */
    header[data-testid="stHeader"] svg {
        fill: white !important;
        stroke: white !important;
    }

    /* Make the text labels black (e.g., "Deploy", "⋮") */
    header[data-testid="stHeader"] button span,
    header[data-testid="stHeader"] div[role="button"] span {
        color: white !important;
        font-weight: 800;
    }
    /* Inputs */
    [data-testid="stSidebar"] input,
    [data-testid="stSidebar"] select,
    [data-testid="stSidebar"] textarea {
        background-color: #1f1f1f !important;
        color: white !important;
        border: 1px solid #333 !important;
        border-radius: 10px !important;
        padding: 1.5rem !important;
    }

    /* Buttons */
    [data-testid="stSidebar"] button {
        background-color: #292929 !important;
        color: white !important;
        border-radius: 10px !important;
        border: none !important;
        padding: 0.6rem 1rem !important;
        transition: background-color 0.3s ease;
    }

    [data-testid="stSidebar"] button:hover {
        background-color: #444 !important;
        cursor: pointer;
    }

    /* Titles or headers in sidebar */
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        color: #f39c16 !important;
        margin-top: 1.5rem;
    }

    /* Optional: Add a border line at the bottom of each section */
    [data-testid="stSidebar"] .block-container > div {
        border-bottom: 1px solid #333;
        padding-bottom: 2rem;
        margin-bottom: 2rem;
    }
    </style>


    """,
    unsafe_allow_html=True
)


def set_background():
    """
    Set a full-page background image in Streamlit using a web link.
    """
    image_url = "https://images.unsplash.com/photo-1650473395434-8674d953ef2f?q=80&w=1932&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
    
    bg_image = f"""
    <style>
        .stApp {{
            background-image: url('{image_url}');
            background-size: cover;
            background-attachment: fixed;
            background-position: center;
            background-color: black;
        }}
        
        /* Styling interactive elements */
        .stButton > button {{
            transition: 0.3s;
            border-radius: 8px;
            padding: 8px 16px;
        }}

        
        .stButton > button:hover {{
            background-color: #ff9800 !important;
            color: white !important;
            transform: scale(1.05);
        }}

        /* Animation for elements */
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        .element {{
            animation: fadeIn 0.6s ease-in-out;
        }}
    </style>
    """
    st.markdown(bg_image, unsafe_allow_html=True)

set_background()

def display_issues(issues):
    # --- Display Issues ---
    counter = 1
    for issue in issues:
        with st.container():
            
            st.markdown("<hr style='border: 1px solid #ccc;'>", unsafe_allow_html=True)
            st.markdown(f"## Issue #{counter}")
            
            safe_title = html.escape(issue["title"])
            st.markdown(f"🔗 [{safe_title}]({issue['html_url']}) | 🏷️ Labels: {', '.join([label['name'] for label in issue['labels']]) if issue['labels'] else 'None'} | {issue['state'].capitalize()} | {"Assigned Already" if issue['assignees'] else 'Unassigned'}")
            if issue['body']:
                summary_key = f"summarized_text_{counter}"
                if summary_key not in st.session_state:
                    if st.button("Click here to learn more!", key=f"Learn more {counter}"):
                        # Generate summary only once and store it
                        st.session_state[summary_key] = summarize_issue(issue['body'])
                if summary_key in st.session_state:
                    safe_desc = html.escape(st.session_state[summary_key])
                    st.write(safe_desc)
            counter += 1

    st.markdown("---")
    st.caption("All issues are displayed.")


# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to:", ["Home", "GitHub Login", "Your Top Languages","Project by Language", "Find Projects", "Profile Visualization"])

# Home Page
if page == "Home":
    st.markdown(
        """
        <style>
            .center-container {
                display: flex;
                justify-content: center;
                align-items: center;
                height: 65vh;
                text-align: center;
                flex-direction: column;
                color: #FFFFFF;
            }

            .text-box {
                background-color: #28025330; /* Black with 50% opacity */
                padding: 30px;
                border-radius: 15px;
                
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
                max-width: 80%;
            }
        </style>

        <div class="center-container">
            <div class="text-box">
                <h1>Commit-Connect</h1>
                <p style="font-size: 22px;">Find open-source projects that match your skills!</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


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
                    <li>Go to <a href="https://github.com/settings/tokens" target="_blank" style="color: #38bdf8;">GitHub Tokens</a></li>
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
            set_token(pat)
            user_data = get_user_profile()
            if user_data:
                st.session_state.pat = pat
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
        repos = get_user_repos()
        if repos:
            lang_data = get_language_distribution(repos)

            if lang_data:
                all_languages = sorted(lang_data, key=lang_data.get, reverse=True)
                top_languages = all_languages[:3]
                st.session_state.top_languages = top_languages  #Store it globally
                st.session_state.all_languages = all_languages

                # Display as a pie chart
                st.markdown("<h3 style='color: white;'>🛠 Your Top Programming Languages</h3>", unsafe_allow_html=True)
                fig, ax = plt.subplots()
                ax.pie(lang_data.values(), labels=lang_data.keys(), autopct="%1.1f%%", startangle=140, colors=plt.cm.Paired.colors)
                ax.axis("equal")  # Ensures pie chart is circular
                st.pyplot(fig)

                st.success(f"Top languages detected: {', '.join(top_languages)}")
            else:
                st.info("No language data found in your repositories.")
    else:
        st.warning("Please log in first on the 'GitHub Login' page.")


# project by languages
elif page == "Project by Language":
    st.title("🎯 Repositories by Language")

    top_languages = st.session_state.get("top_languages", [])
    all_languages = st.session_state.get("all_languages", [])

    if all:
        st.success(f"🔍 Searching using your favorite languages: {', '.join(all_languages)}")
         # Let user choose from their top languages
        selected_languages = st.multiselect(
            "🔎 Select languages to filter repositories:",
            all_languages,
            default=all_languages[:len(all_languages)]
        )
    min_stars = st.slider("⭐ Minimum Stars", 0, 50, 0)
    recent_days = st.slider("🕒 Updated Within (days)", 0, 365, 90)

    if st.button("🔍 Fetch Repositories"):
            repos = search_repositories_by_language(languages=all_languages, min_stars= min_stars,recent_days =recent_days)

            if "error" in repos:
                st.error(repos["error"])
            elif len(repos) == 0:
                st.info("No repositories matched the selected filters.")
            else:
                st.success(f"Found {len(repos)} repositories:")
                for repo in repos:
                    st.markdown(f"🔗 [{repo['name']}]({repo['html_url']}) — ⭐ {repo['stargazers_count']} | 🧠 {repo['language']} | 🕒 Updated: {repo['updated_at'][:10]}")
    else:
        st.warning(" select at least one language.")

# Find Projects Page
elif page == "Find Projects":
    st.title("🔎 Find Open Source Projects")
    st.write("This section will help you find open-source issues to contribute to.")
    prompt = st.text_input("What kind of projects are you looking for to contribute? ")
    if prompt:
        result = parse_user_prompt(prompt)
        #st.write(result)
        languages, frameworks_libraries, tools, difficulty, filters = get_filters(prompt)
        #query, query_url = build_issue_query(languages, frameworks_libraries, tools, difficulty, filters)
        #st.write(query)
        json_data = find_github_issues(user_input=prompt)
        total_issues = len(json_data)

        st.markdown(f"### Showing {total_issues} issues")
        display_issues(json_data)

# Profile Visualization Page
elif page == "Profile Visualization":
    st.title("📊 Visualize Your GitHub Profile")
    st.write("This section will generate interactive visualizations of your GitHub activity.")
    #use stored pat
    if "pat" in st.session_state and st.session_state.pat:
        pat = st.session_state.pat
        headers = {"Authorization": f"token {pat}"}

    if st.button("Fetch Data"):
    # Fetch GitHub Data
        url = f"https://api.github.com/user"
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            user_data = response.json()
            username = user_data.get("login")
            st.success(f"Logged in as: {username}")
            if username:
                    st.success(f"Logged in as: {username}")
       # get user repositories 
            repo_response = requests.get(f"https://api.github.com/users/{username}/repos", headers=headers)
            if repo_response.status_code == 200:
                repos = repo_response.json()
        # Extract Data
            repo_names = [repo["name"] for repo in repos]
            stars = [repo["stargazers_count"] for repo in repos]
            forks = [repo["forks_count"] for repo in repos]

        # Convert to DataFrame
            df = pd.DataFrame({"Repository": repo_names, "Stars": stars, "Forks": forks})

        # Display Table
            st.subheader("📌 Repository Data")
            st.dataframe(df)

        # Plot Chart
            st.subheader("⭐ Stars per Repository")
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.barh(df["Repository"], df["Stars"], color="orange")
            ax.set_xlabel("Stars")
            ax.set_ylabel("Repository")
            ax.set_title("GitHub Stars per Repository")
            st.pyplot(fig)
        

        else:
            st.error("Failed to fetch data. Check the username and try again.")

