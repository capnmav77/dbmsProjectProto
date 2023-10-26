import streamlit as st
import mysql.connector
from mysql.connector import Error


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
    
def get_group_events(group):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute(f"call get_group_events('{group}')")
    result = cursor.fetchall()
    print(result)
    return result

# Check if the user is logged in

if 'Username' not in st.session_state:
    st.session_state["Username"] = ""

User1 = st.session_state['Username']

if User1 != "":
    User1 = st.session_state['Username']
    st.text(f"Welcome, {User1}")
    
    # Display the user's groups here
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute(f"call get_user_groups('{User1}')")
    result = cursor.fetchall()
    print(result)
    #creating a dropdown menu for the user to select a group
    group_list = []
    for i in result:
        group_list.append(i[1])
    group_list = tuple(group_list)
    group = st.selectbox("Select a group", group_list)
    st.text(f"You selected {group}")
    get_group_events(group)

    #creating a button to display the group members
else:
    st.warning("You need to log in to access this page.")
