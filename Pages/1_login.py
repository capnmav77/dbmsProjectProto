import mysql.connector
import streamlit as st
from mysql.connector import Error
import random

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
    
def checkforPro(User1):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute(f"select is_pro_member from users where username = '{User1}'")
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result[0]

def login_page():
    st.title("User Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("User_Login"):
        connection = connect_to_database()
        cursor = connection.cursor(buffered=True)
        cursor.execute("SELECT check_password(%s,%s)", (username, password))    
        result = cursor.fetchall()
        cursor.close()
        connection.close()
        if result[0][0] == 1:
            pro_user = checkforPro(username)
            st.session_state['is_pro_member'] = pro_user
            st.success("Login successful.")
            st.session_state['Username'] = username
            st.title(f"Welcome, {st.session_state['Username']}")
            st.text("You can now access your groups.") 
            connection.close()
        else:
            st.error("Invalid username or password.")
            cursor.close()
            connection.close()
    
def sign_up():
    st.title("Sign Up")
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    verify_password = st.text_input("Verify Password", type="password")
    
    if st.button("Sign_Up"):
        if password != verify_password:
            st.error("Passwords do not match.")
        else:
            hashkey = ''.join(random.choices('0123456789', k=5))
            connection = connect_to_database()
            cursor = connection.cursor(buffered=True)

            cursor.execute("SELECT check_username(%s)", (username,))
            result = cursor.fetchone()
            if result[0] == 1:
                st.error("Username already exists.")
                cursor.close()
                connection.close()
            else:
                cursor.execute("SELECT add_user(%s, %s, %s, %s)", (username, email, password, hashkey))
                connection.commit()
                st.success("Sign up successful. Please log in.")
                cursor.close()
                connection.close()
    

def Login_and_signup():
    st.title("Login and Signup")
    if 'Username' not in st.session_state:
        st.session_state['Username'] = ""

    User1 = st.session_state['Username']

    if User1:
        st.text('You have already logged in as ' + User1 + ' you can go back to your groups')
        # Display the user's groups here
    else:
        choice = st.radio("Choose an option:", ("Login", "Signup"))
        if choice == "Login":
            login_page()
        elif choice == "Signup":
            sign_up()


Login_and_signup()
