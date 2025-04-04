import streamlit as st
import requests

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

# Main Content Based on Selection
if page == "Home":
    st.title("🔍 Commit-Connect")
    st.write("Find open-source projects that match your skills!")



elif page == "GitHub Login":
    st.title("🔑 Log in with GitHub")
    st.write("Enter your GitHub Personal Access Token (PAT) to proceed.")

    if "help_visible" not in st.session_state:
        st.session_state.help_visible = False

    
    # PAT Input Field with Help Button
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
                st.success(f"Logged in as {user_data['login']}")
                
                # Display user info
                st.image(user_data["avatar_url"], width=100)
                st.write(f"**Name:** {user_data.get('name', 'N/A')}")
                st.write(f"**Bio:** {user_data.get('bio', 'N/A')}")
                st.write(f"**Public Repos:** {user_data['public_repos']}")
                st.write(f"**Followers:** {user_data['followers']} | **Following:** {user_data['following']}")
            else:
                st.error("Invalid Token! Please check and try again.")
        else:
            st.warning("Please enter your GitHub Personal Access Token.")

elif page == "Your Top Languages":
    st.title("📊 Your Top Languages")
    st.write("This section will display your most used programming languages.")

elif page == "Find Projects":
    st.title("🔎 Find Open Source Projects")
    st.write("This section will help you find open-source issues to contribute to.")

elif page == "Profile Visualization":
    st.title("📊 Visualize Your GitHub Profile")
    st.write("This section will generate interactive visualizations of your GitHub activity.")
