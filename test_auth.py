import streamlit as st
from utils.github_api import get_user_profile

st.title("🔧 Backend Dev Test: GitHub Auth")

user = get_user_profile()

if user:
    st.success("✅ GitHub profile fetched successfully!")
    st.image(user["avatar_url"], width=100)
    st.write(f"**Username:** {user['login']}")
    st.write(f"**Name:** {user.get('name', 'N/A')}")
    st.write(f"**Bio:** {user.get('bio', 'No bio')}")
else:
    st.error("❌ Failed to fetch GitHub profile.")

