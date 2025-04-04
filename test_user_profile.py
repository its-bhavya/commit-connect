import streamlit as st
from utils.github_api import get_user_profile

st.title("🔐 GitHub User Profile")

# Get profile
profile = get_user_profile()

# Display profile info
st.image(profile["avatar_url"], width=100)
st.markdown(f"**Name:** {profile['name']}")
st.markdown(f"**Username:** [{profile['username']}]({profile['html_url']})")
st.markdown(f"**Bio:** {profile['bio']}")
st.markdown(f"**Location:** {profile['location']}")

# Show full JSON for debug
with st.expander("Raw API Response"):
    st.json(profile)


