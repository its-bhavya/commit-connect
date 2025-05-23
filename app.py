import streamlit as st
import requests
import base64
import html
from datetime import datetime


import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from utils.github_api import set_token
from utils.github_api import get_user_profile, get_user_repos, get_language_distribution
from utils.github_api import search_repositories_by_language
from gemini import parse_user_prompt, get_filters, find_github_issues, summarize_issue

# Set Page Title and Layout
st.set_page_config(page_title="Commit-Connect", page_icon="🔍", layout="wide")

if "page" not in st.session_state:
    st.session_state.page = "Home"
    
st.markdown(
    """
    <style>
    /* Sidebar base style */
    [data-testid="stSidebar"] {
        background-color: #0A0F1C;
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
    
    /* Inputs */
    [data-testid="stSidebar"] input,
    [data-testid="stSidebar"] select,
    [data-testid="stSidebar"] textarea {
        background-color: #0F192D !important;
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
        padding: 0.2rem 0.7rem !important;
        transition: background-color 0.3s ease;
    }

    [data-testid="stSidebar"] button:hover {
        background-color: #005577 !important;
        cursor: pointer;
    }

    /* Titles or headers in sidebar */
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        color: #00E5FF  !important;
        margin-top: 1.5rem;
    }

    /* Optional: Add a border line at the bottom of each section */
    [data-testid="stSidebar"] .block-container > div {
        border-bottom: 1px solid #333;
        padding-bottom: 2rem;
        margin-bottom: 2rem;
    }

    /* Style Streamlit warning box text */
    div[data-testid="stAlert"] * {
        color: #ffffff !important;
    }

    /* Optional: tweak background */
    div[data-testid="stAlert"] {
        
        border-left: 5px solid !important;
        color: #ffffff;
    }
    a {
        color: white !important;
        text-decoration: underline; /* optional: makes links more visible */
    }

    /Change link color on hover */
    a:hover {
        color: #38BDF8 !important;  
    }

    /* Make the top header bar transparent */
    header[data-testid="stHeader"] {
        background: transparent !important;
        box-shadow: none !important;
    }

    </style>

    """,
    unsafe_allow_html=True
)


def set_background():
    """
    Set a full-page background image in Streamlit using a web link.
    """
    image_url = "https://wallpaperaccess.com/full/2454628.png"
    
    bg_image = f"""
    <style>
        .stApp {{
            background-image: url('{image_url}');
            background-size: cover;
            background-attachment: fixed;
            background-position: center;
            background-color: 0A0F1C;
        }}
        
        /* Styling interactive elements */
        .stButton > button {{
            transition: 0.3s;
            border-radius: 8px;
            padding: 8px 16px;
        }}

        
        .stButton > button:hover {{
            background-color: #006d8e  !important;
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
with st.sidebar:
    if st.button("Home"):
        st.session_state.page = "Home"
    if st.button("GitHub Login"):
        st.session_state.page = "Login"
    if st.button("Your Top Languages"):
        st.session_state.page = "Your Top Languages"
    if st.button("Projects For You"):
        st.session_state.page = "Get Projects"
    if st.button("Smart Issue Recs"):
        st.session_state.page = "Find Projects"
    if st.button("Profile"):
        st.session_state.page = "Profile Visualization"

# Home Page
if st.session_state.page == "Home":
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
                color: #E0F7FA;
            }

            .text-box {
                background-color: #0F192DCC; /* Deep navy-blue with opacity */
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
                max-width: 80%;
            }

            .text-box h1 {
                color: #00E5FF;
            }

            .text-box p {
                font-size: 22px;
                color: #A0D7F3;
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
elif st.session_state.page == "Login":
    
    st.title(":material/login: Log in with GitHub")
    st.write("Enter your GitHub Personal Access Token (PAT) to proceed.")

    if "help_visible" not in st.session_state:
        st.session_state.help_visible = False
    if "pat" not in st.session_state:
        st.session_state.pat = ""

    col1, col2 = st.columns([2, 1])

    with col1:
        pat = st.text_input("GitHub Personal Access Token", type="password", key="github_pat")
        st.session_state.pat = pat

    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Help"):
            st.session_state.help_visible = not st.session_state.help_visible

    if st.session_state.help_visible:
        st.markdown(
            """
            <div style="border-radius: 10px; background-color: #1e293b; padding: 15px; color: white;">
                <h4> How to Generate a GitHub PAT?</h4>
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
elif st.session_state.page == "Your Top Languages":
    # 🖼️ Custom Background CSS (same as Profile Visualization page)
    st.markdown(
        """
        <style>
        .stApp {
            background-image: url("https://images.unsplash.com/photo-1614851099511-773084f6911d?fm=jpg&q=60&w=3000&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8N3x8Z3JhZGllbnQlMjBiYWNrZ3JvdW5kfGVufDB8fDB8fHww"); /* Replace with your actual background URL */
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title(":material/award_star: Your Top Languages")

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
                st.session_state.top_languages = top_languages  # Store it globally
                st.session_state.all_languages = all_languages

                st.success(f"Top languages detected: {', '.join(top_languages)}")

                # 🎨 Beautified Transparent Pie Chart
                import matplotlib.pyplot as plt
                import matplotlib as mpl

                # Set a modern font theme
                mpl.rcParams['font.family'] = 'sans-serif'
                mpl.rcParams['font.size'] = 10

                # Custom colors
                colors = ["#FF6F61", "#6B5B95", "#88B04B", "#FFA07A", "#20B2AA", "#FFB347", "#779ECB"]

                # Create Pie Chart with transparent background
                fig, ax = plt.subplots(figsize=(6, 6), dpi=100, facecolor='none')
                fig.patch.set_alpha(0.0)  # Transparent figure background
                ax.set_facecolor('none')  # Transparent axis background

                wedges, texts, autotexts = ax.pie(
                    lang_data.values(),
                    labels=lang_data.keys(),
                    autopct="%1.1f%%",
                    startangle=140,
                    colors=colors[:len(lang_data)],
                    wedgeprops={'edgecolor': 'white', 'linewidth': 2, 'antialiased': True},
                    textprops={'fontsize': 10, 'color': 'white'}
                )

                for autotext in autotexts:
                    autotext.set_color('white')
                    autotext.set_weight('bold')
                    autotext.set_size(9)

                ax.axis("equal")
                plt.title("Your Top Languages", fontsize=14, fontweight='bold', color="white")
                st.pyplot(fig)

            else:
                st.info("No language data found in your repositories.")
        else:
            st.warning("Could not fetch repositories. Please try again.")
    else:
        st.warning("Please log in first on the 'Login' page.")

# Get Projectss
elif st.session_state.page == "Get Projects":
    st.title(":material/folder_code: Get matched with projects that fit your profile, perfectly.")

    # Get top and all languages from session
    top_languages = st.session_state.get("top_languages", [])
    all_languages = st.session_state.get("all_languages", [])

    if all_languages:
        # 1. LANGUAGE FILTER (Always Visible)
        selected_languages = st.multiselect(
            "🧠 Select languages to filter repositories:",
            all_languages,
            default=all_languages[:len(all_languages)]
        )

        # 2. ADVANCED FILTERS (Inside Expander)
        with st.expander("⚙️ Advanced Filters"):
            sort_option = st.selectbox(
                "🔽 Sort Repositories By",
                [
                    "Best match",
                    "Most stars",
                    "Fewest stars",
                    "Most forks",
                    "Fewest forks",
                    "Recently updated",
                    "Least recently updated"
                ]
            )

            if sort_option == "Best match":
                sort_by, order = None, None
            elif sort_option == "Most stars":
                sort_by, order = "stars", "desc"
            elif sort_option == "Fewest stars":
                sort_by, order = "stars", "asc"
            elif sort_option == "Most forks":
                sort_by, order = "forks", "desc"
            elif sort_option == "Fewest forks":
                sort_by, order = "forks", "asc"
            elif sort_option == "Recently updated":
                sort_by, order = "updated", "desc"
            elif sort_option == "Least recently updated":
                sort_by, order = "updated", "asc"

            min_stars = st.slider("⭐ Minimum Stars", 0, 50, 0)
            min_forks = st.slider(" Minimum Forks", 0, 50, 0)
            recent_days = st.slider("🕒 Updated Within (days)", 0, 800, 90)

        # Defaults if not set
        min_stars = min_stars if 'min_stars' in locals() else 0
        recent_days = recent_days if 'recent_days' in locals() else 90

        # 3. SEARCH BUTTON
        if st.button("Fetch Repositories"):
            if not selected_languages:
                st.warning("Please select at least one language.")
            else:
                repos = search_repositories_by_language(
                    languages=selected_languages,
                    min_stars=min_stars,
                    recent_days=recent_days,
                    min_forks = min_forks,
                    sort_by=sort_by,
                    order=order
                )
                if "error" in repos:
                    st.error(repos["error"])
                elif len(repos) == 0:
                    st.info("No repositories found.")
                else:
                    st.success(f"Found {len(repos)} repositories:")
                    for repo in repos:
                        st.markdown(
                            f"🔗 [{repo['name']}]({repo['html_url']}) — Languages: {repo['language']} "
                            f"| Stars: {repo['stargazers_count']}| Forks: {repo['forks_count']} Updated: {repo['updated_at'][:10]}"
                        )
    else:
        st.warning("No languages found in session. Please load your GitHub profile first.")

# Find Projects Page
elif st.session_state.page == "Find Projects":
    st.title(":material/search: Describe your idea, and let AI fetch relevant open-source issues you can start with.")
    prompt = st.text_input("What kind of projects are you looking for to contribute? ",placeholder="Can you suggest some beginner-friendly issues in Flask related projects?")


    sort_option = st.selectbox(
    "🔽 Sort Results By",
    [
        "Best match",
        "Recently updated",
        "Least recently updated"
    ]
)

    if sort_option == "Best match":
        sort_by, order = None, None
    elif sort_option == "Recently updated":
        sort_by, order = "updated", "desc"
    elif sort_option == "Least recently updated":
        sort_by, order = "updated", "asc"
    

    
    state_filter = st.selectbox("Issue State", ["open", "closed"])
    assignment_filter = st.selectbox("Assignment", ["all", "assigned", "unassigned"])
    st.markdown(f"🔍 Showing **{state_filter}** issues that are **{assignment_filter}**")

    

    # 🕒 Recently updated slider
    recent_days = st.slider("🕒 Updated within (days)", 0, 365, 90)

    if prompt:
        result = parse_user_prompt(prompt)
        #st.write(result)
        languages, frameworks_libraries, tools, difficulty, filters = get_filters(prompt)
        #query, query_url = build_issue_query(languages, frameworks_libraries, tools, difficulty, filters)
        #st.write(query)
        json_data = find_github_issues(user_input=prompt,
            state=state_filter,
            assigned=assignment_filter,
            recent_days=recent_days
        )
        total_issues = len(json_data)

        st.markdown(f"### Showing {total_issues} issues")
        display_issues(json_data)

# Profile Visualization Page
# Profile Visualization Page
elif st.session_state.page == "Profile Visualization":
    import requests
    import pandas as pd
    import matplotlib.pyplot as plt
    import plotly.express as px
    from datetime import datetime
    from collections import Counter

    st.title(":material/bar_chart: Visualize Your GitHub Profile")

     # 👇 Custom background image ONLY for this page
    profile_bg = '''
    <style>
    [data-testid="stAppViewContainer"] {
        background-image: url("https://static.vecteezy.com/system/resources/previews/019/511/518/non_2x/blue-background-abstract-illustration-with-gradient-blur-design-free-vector.jpg");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }

    [data-testid="stHeader"] {
        background: rgba(0,0,0,0);
    }

    [data-testid="stSidebar"] {
        background-color: #0A0F1C;
        padding: 2rem 1rem;
        border-radius: 0 25px 25px 0;
        box-shadow: 4px 0 15px rgba(0,0,0,0.4);
        transition: all 0.3s ease;
    }

    .stDataFrame, .stPlotlyChart {
        
        border-radius: 10px;
        padding: 1rem;
    }
    </style>
    '''
    st.markdown(profile_bg, unsafe_allow_html=True)

    # Use stored PAT
    if "pat" in st.session_state and st.session_state.pat:
        pat = st.session_state.pat
        headers = {"Authorization": f"token {pat}"}
    else:
        st.error("GitHub PAT not found. Please login again.")
        st.stop()

    if st.button("Fetch Data"):
    # Fetch GitHub Data
        url = f"https://api.github.com/user"
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            user_data = response.json()
            username = user_data.get("login")
            if username:
                st.success(f"Logged in as: {username}")

                # Get user repositories
                repo_response = requests.get(f"https://api.github.com/users/{username}/repos", headers=headers)
                if repo_response.status_code == 200:
                    repos = repo_response.json()

                    # Extract Data
                    repo_names = [repo["name"] for repo in repos]
                    stars = [repo["stargazers_count"] for repo in repos]
                    forks = [repo["forks_count"] for repo in repos]
                    languages = []
                    for repo in repos:
                        repo_name = repo["name"]
                        lang_url = f"https://api.github.com/repos/{username}/{repo_name}/languages"
                        lang_response = requests.get(lang_url, headers=headers)
                        if lang_response.status_code == 200:
                            lang_data = lang_response.json()
                            languages.append(', '.join(lang_data.keys()))
                        else:
                            languages.append('')

                    # Convert to DataFrame
                    df = pd.DataFrame({"Repository": repo_names, "Languages": languages, "Stars": stars, "Forks": forks})

                    # 📊 Pretty Bar Chart for Stars
                    st.subheader("Stars per Repository")
                    if not df.empty:
                        bar_fig = px.bar(
                            df.sort_values("Stars", ascending=False),
                            x="Stars",
                            y="Repository",
                            orientation="h",
                            color="Stars",
                            color_continuous_scale="Sunsetdark",
                            title="Repository Stars Overview",
                            labels={"Stars": "Star Count", "Repository": "Repository Name"},
                        )
                        bar_fig.update_layout(
                            xaxis=dict(
                                range=[0, 20],
                                tickmode='linear',
                                tick0=0,
                                dtick=1  # Ensures integer steps
                            ),
                            plot_bgcolor="rgba(0,0,0,0)",
                            paper_bgcolor="rgba(0,0,0,0)",
                            font=dict(size=14),
                            title_x=0.5,
                        )
                        st.plotly_chart(bar_fig)
                    else:
                        st.info("No repository data found.")

                    # 📈 Commit History Line Graph
                    st.subheader("📅 Commit History (Last 30 Days)")
                    commit_dates = []

                    for repo in repos:  # Limit to first 3 repos to reduce API load
                        repo_name = repo["name"]
                        commits_url = f"https://api.github.com/repos/{username}/{repo_name}/commits"
                        params = {"per_page": 100}
                        commits_resp = requests.get(commits_url, headers=headers, params=params)

                        if commits_resp.status_code == 200:
                            commits = commits_resp.json()
                            for commit in commits:
                                try:
                                    date_str = commit["commit"]["committer"]["date"]
                                    date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ").date()
                                    commit_dates.append(date_obj)
                                except Exception:
                                    continue

                    if commit_dates:
                        commit_df = pd.DataFrame(commit_dates, columns=["date"])
                        commit_df = commit_df.groupby("date").size().reset_index(name="commits")

                        line_fig = px.line(
                            commit_df,
                            x="date",
                            y="commits",
                            title="Your GitHub Commit History",
                            markers=True,
                            line_shape="spline",
                            labels={"date": "Date", "commits": "Number of Commits"},
                        )

                        line_fig.update_layout(
                            plot_bgcolor="rgba(0,0,0,0)",
                            paper_bgcolor="rgba(0,0,0,0)",
                            font=dict(size=14),
                            title_x=0.5,
                            hovermode="x unified",
                        )

                        st.plotly_chart(line_fig)
                    else:
                        st.info("No commit data available.")

                    # 📌 Display Table
                    st.subheader("📋 Repository Data")
                    st.dataframe(df)
                else:
                    st.error("Failed to fetch repositories.")
            else:
                st.error("Username not found.")
        else:
            st.error("Failed to fetch data. Check the token and try again.")
