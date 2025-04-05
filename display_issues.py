import streamlit as st
import requests
import math
from gemini import find_github_issues
import html


# --- Function to Display Issues ---
def display_issues(issues):
    # --- Display Issues ---
    for issue in issues:
        with st.container():
            st.markdown("<hr style='border: 1px solid #ccc;'>", unsafe_allow_html=True)
            safe_title = html.escape(issue["title"])
            # Create a clickable link with the title as visible text
            st.markdown(
                f"<a href='{issue['html_url']}' style='color: white; text-decoration: none; font-size: 1.3em;'>{safe_title}</a>",
                unsafe_allow_html=True
            )
            st.write(f"🧑 Author: [{issue['user']['login']}]({issue['user']['html_url']})")
            st.write(f"🏷️ Labels: {', '.join([label['name'] for label in issue['labels']]) if issue['labels'] else 'None'}")
            st.write(f"🔗 Assigned to: {', '.join([user['login'] for user in issue['assignees']]) if issue['assignees'] else 'Unassigned'}")
            st.write(f"📌 State: {issue['state'].capitalize()}")
            st.write(f"💬 Comments: {issue['comments']}")

    st.markdown("---")
    st.caption("All issues are displayed.")

