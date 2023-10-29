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
    


def display_group_details(group_details):
    st.subheader("Group Details")
    st.table(pd.DataFrame([group_details], columns=["Group ID", "Group Name", "Group Description","Group Owner","date created","member count","previously_visited_location","pending Requests"]))
    # st.text("Group Name: " + group_details[1])
    # st.text("Group ID: " + str(group_details[0]))
    # st.text("Group Description: " + group_details[2])

def get_group_details(group_id):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute(f"call get_group_details('{group_id}')")
    result = cursor.fetchall()
    #print(result)
    display_group_details(result[0]) #result is a list of lists, so we need to pass in the first element of the list


def display_event_details(event_details):
    event_container = st.container()
    
    with event_container:
        st.title(event_details[1])
        st.text("Event Location: " + event_details[2])
        
        # Format the date and time
        event_date = event_details[3].strftime("%Y-%m-%d")
        event_time = event_details[4].total_seconds() / 3600  # Convert timedelta to hours
        
        st.text(f"Event Date: {event_date}")
        st.text(f"Event Time: {event_time} hours")
        
        st.text("Event Description: " + event_details[5])


def get_group_events(group_id):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute(f"call get_group_events('{group_id}')")
    result = cursor.fetchall()
    st.subheader("Group Events")
    print(result)
    if result == []:
        st.warning("There are no events in this group.")
    else:
        display_event_details(result[0])



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
        st.warning("You have no groups to select from.")

    #creating a button to display the group members
else:
    st.warning("You need to log in to access this page.")
