
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
    

def add_group_event(UserGroupId):
    st.text("add events")
    #code for adding events
    #get event details
    #call add_event
    #display event details


def AddEvents(User1):
    st.title("Add Events")
    userGroupId = st.text_input("Enter the Group ID")
    if st.button("search and request"):
        connection = connect_to_database()
        cursor = connection.cursor()
        cursor.execute(f"select check_group_exists('{userGroupId}')")
        result = cursor.fetchone()
        cursor.close()
        if result[0] == 1:
            st.text("Group exists")
            #code for adding events
            add_group_event(userGroupId)
        else :
            st.text("Group doesn't exist")

# Check if the user is logged in
if 'Username' not in st.session_state:
    st.session_state["Username"] = ""

User1 = st.session_state['Username']

if User1 != "":
    AddEvents(User1)
    
    
else:
    st.warning("You need to log in to access this page.")


