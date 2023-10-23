import streamlit as st

class SessionState:
    def __init__(self):
        self.username = ""
        self.is_logged_in = False

session_state = SessionState()