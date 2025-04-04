import streamlit as st

# Set Page Title and Layout
st.set_page_config(page_title="Commit-Connect", page_icon="🔍", layout="wide")

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to:", ["Home", "GitHub Login", "Your Top Languages", "Find Projects", "Profile Visualization"])

# Main Content Based on Selection
if page == "Home":
    st.title("🔍 Commit-Connect")
    st.write("Find open-source projects that match your skills!")

elif page == "GitHub Login":
    st.title("🔑 Log in with GitHub")
    st.write("Enter your GitHub Personal Access Token (PAT) to proceed.")

elif page == "Your Top Languages":
    st.title("📊 Your Top Languages")
    st.write("This section will display your most used programming languages.")

elif page == "Find Projects":
    st.title("🔎 Find Open Source Projects")
    st.write("This section will help you find open-source issues to contribute to.")

elif page == "Profile Visualization":
    st.title("📊 Visualize Your GitHub Profile")
    st.write("This section will generate interactive visualizations of your GitHub activity.")
