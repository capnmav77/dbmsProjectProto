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
    

# Check if the user is logged in
if 'Username' not in st.session_state:
    st.session_state["Username"] = ""

User1 = st.session_state['Username']

if User1 != "":
    User1 = st.session_state['Username']
    st.text(f"Hey, {User1}, feel like changing your profile")
    
    # Display the user's groups here
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute(f"call get_user_groups('{User1}')")
    result = cursor.fetchall()
    print(result)
    #creating a dropdown menu for the user to select a group
    # Extract group names from the results
    group_names = [group[1] for group in result]
    
    if group_names:
        # Create a selectbox with group names
        selected_group_name = st.selectbox("Your Groups :", group_names)
        #st.text(f"You selected {selected_group_name}")
        
        # Find the corresponding group_id for the selected group name
        selected_group_id = [group[0] for group in result if group[1] == selected_group_name][0]
        
        # Call the get_group_events function with the selected group_id
        get_group_details(selected_group_id)
        st.write("---")
        get_group_events(selected_group_id)

else:
    st.warning("You need to log in to access this page.")
