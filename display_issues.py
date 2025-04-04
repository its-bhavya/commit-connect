import streamlit as st
import requests
import math
from gemini import find_github_issues

# --- Function to Display Issues ---
def display_issues(issues):
    # --- Display Issues ---
    for issue in issues:
        with st.container():
            st.markdown("---")
            st.markdown(f"### [{issue['title']}]({issue['html_url']})")
            st.write(f"🧑 Author: [{issue['user']['login']}]({issue['user']['html_url']})")
            st.write(f"🏷️ Labels: {', '.join([label['name'] for label in issue['labels']]) if issue['labels'] else 'None'}")
            st.write(f"🔗 Assigned to: {', '.join([user['login'] for user in issue['assignees']]) if issue['assignees'] else 'Unassigned'}")
            st.write(f"📌 State: {issue['state'].capitalize()}")
            st.write(f"💬 Comments: {issue['comments']}")

    st.markdown("---")
    st.caption("All issues are displayed.")

