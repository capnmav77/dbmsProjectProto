import streamlit as st
from main import session_state

# Check if the user is logged in
if session_state.is_logged_in:
    st.title(f"Welcome, {session_state.username}")
    # Display the user's groups here
else:
    st.warning("You need to log in to access this page.")