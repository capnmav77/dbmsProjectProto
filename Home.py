import streamlit as st

# Set page title and background color
st.set_page_config(
    page_title="Welcome to Hangout",
    page_icon="✌️",
    layout="wide",
)

# Define the main title
st.title("Welcome to Hangout")
st.markdown("🚀 *A Social Media App for Friends to Hang Out* 🌴")

# Create a two-column layout for information and action
col1, col2 = st.columns([2, 1])

# Left column: App information and visuals
with col1:
    st.write(
        "Hangout is a fun and interactive social media app designed for you and your friends "
        "to connect, share moments, and hang out together, no matter where you are!"
    )

    st.write(
        "Here's what you can do on Hangout:\n"
        "- Create and join groups\n"
        "- Plan events and gatherings\n"
        "- Stay connected and have fun!"
    )

# Right column: Action buttons and sign-up prompt

# Add some additional styling
st.markdown(
    """
    <style>
    .st-title {
        font-size: 36px;
        color: #FFA500;
    }
    .stText {
        font-size: 18px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
