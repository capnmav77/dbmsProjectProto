import streamlit as st
import mysql.connector
from mysql.connector import Error
import pandas as pd


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
    
def check_group_exists(groupName):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute(f"select check_group_exists('{groupName}')")
    result = cursor.fetchone()
    cursor.close()
    if result == 1:
        return 1
    else :
        return 0



#Check if the user is logged in
if 'Username' not in st.session_state:
    st.session_state["Username"] = ""

User1 = st.session_state['Username']

if User1 != "":
    #get user's group req
    userGroupId = st.text_input("Group ID")
    if check_group_exists(userGroupId) :
        connection = connect_to_database()
        cursor = connection.cursor()
        cursor.execute(f"call add_group_requests('{userGroupId}','{User1}');")
        response = cursor.fetchall()
        connection.commit()
        st.text(response)
    else:
        st.text("The group doesn't exists check your group-id")
    

else:
    st.warning("You need to log in to access this page.")
