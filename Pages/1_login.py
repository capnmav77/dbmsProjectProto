import mysql.connector
import streamlit as st
from mysql.connector import Error

st.sidebar.isExpanded = False

# Establish a connection to the MySQL Server
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
    
def login_page():
    st.title("User Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("User_Login"):
        connection = connect_to_database()
        cursor = connection.cursor()
        cursor.execute("SELECT check_password(%s,%s)", (username, password)) 
        result = cursor.fetchone()
        if result[0] == 1:
            #check for pro user 
            # cursor.execute ("SELECT check_isprouser(%s)", (username))
            # result = cursor.fetchone()
            # if result[0] == 1:
            #     st.session_state['isProUser'] = True
            # else:
            #     st.session_state['isProUser'] = False

            #for displaying proper login message 
            st.success("Login successful.")
            st.session_state['Username'] = username
            st.title(f"Welcome, {st.session_state['Username']}")
            st.text("you can now access your groups ") 

        else:
            st.error("Invalid username or password.")
    
    

def sign_up():
    st.title("Sign Up")
    username = st.text_input("Your name")
    password = st.text_input("Your Password", type="password")
    
    if st.button("Sign_Up"):
        connection = connect_to_database()
        cursor = connection.cursor()
        cursor.execute("SELECT check_username(%s)", (username,))
        result = cursor.fetchone()
        if result[0] == 1:
            st.error("Username already exists.")
        else:
            cursor.execute("SELECT add_user(%s,%s)", (username, password))
            connection.commit()
            st.success("Sign up successful. Please log in.")
            #redirect to login page
    

def Login_and_signup():
    st.title("Login and Signup")
    if 'Username' not in st.session_state :
        st.session_state['Username'] = ""

    User1 = st.session_state['Username']

    if (st.session_state['Username']):
        st.text('you have already logged in as ' + User1 + ' you can go back to your groups')
        # Display the user's groups here
    else:
        choice = st.radio("Choose an option:", ("Login", "Signup"))
        if choice == "Login":
            login_page()
        elif choice == "Signup":
            sign_up()
       #radiobutton for login or signup


 

Login_and_signup()