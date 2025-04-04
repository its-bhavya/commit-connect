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

    # PAT Input Field
    pat = st.text_input("🔐 GitHub Personal Access Token", type="password")

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
