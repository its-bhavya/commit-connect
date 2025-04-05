import streamlit as st

def login():
    """Simulated GitHub login function (Replace with actual OAuth flow)"""
    if "github_pat" not in st.session_state:
        # Simulate retrieving the PAT after login
        user_pat = "ghp_yourgeneratedPAT"  # Replace this with actual OAuth flow result
        st.session_state["github_pat"] = user_pat
        st.success("✅ Logged in successfully!")
