import mysql.connector
import streamlit as st
from mysql.connector import Error



class SessionState:
    def __init__(self):
        self.username = ""
        self.is_logged_in = False

session_state = SessionState()


# Establish a connection to MySQL Server
def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1234",
            database="hang_out"
        )
        return connection
    except Error as e:
        st.error(f"Error: {e}")
        return None



# create a streamlit instance to display the data
def streamlitUI():
    login_option = st.radio("Choose an option:", ["Login", "Signup"])

    if login_option == "Login":
        username = st.text_input("Username:")
        password = st.text_input("Password:", type="password")
        
        if st.button("Login"):
            connection = connect_to_database()
            if connection:
                st.write("connection established")
                cursor = connection.cursor()
                cursor.callproc("check_password", (username, password))
                result = cursor.fetchone()
                cursor.close()
                connection.close()
                
                if result[0] == True:
                    st.success("Login successful")
                    session_state.username = username
                    session_state.is_logged_in = True
                    st.write("Redirecting to your groups...")
                    # Implement a redirection to the user's groups page
                else:
                    st.error("Login failed. Please check your credentials.")
    elif login_option == "Signup":
        # Add the code for user registration here
        pass

    # You can add more Streamlit components to handle user registration and group navigation.

    # Example redirection:
    # If login is successful, you can use Streamlit's built-in Session State to redirect to the user's groups.
    # See https://docs.streamlit.io/1.0.0/library/api-reference/util/session_state
    # You would store the user's information in session state after successful login and use it to navigate to their groups.

    # Sample code for a page with user groups
    # import streamlit.report_thread as ReportThread
    # from streamlit.server.server import Server
    # session_state = SessionState.get(username="", is_logged_in=False)
    # if session_state.is_logged_in:
    #     st.title(f"Welcome, {session_state.username}")
    #     # Display the user's groups here

    # To run the Streamlit app, use the following command in your terminal:
    # streamlit run your_app_name.py

streamlitUI()