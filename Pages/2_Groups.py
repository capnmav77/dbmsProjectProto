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
    

def display_group_requests(request):
    reqUser = request[1]
    reqGroup = request[0]
    
    if reqUser and reqGroup:
        key = f'{reqUser}-{reqGroup}'
        st.text("User name: " + reqUser + " is requesting to join this group")

        if st.button(f"Accept", key=f'A-{key}'):
            connection = connect_to_database()
            cursor = connection.cursor()
            cursor.execute(f"CALL accept_group_request('{reqGroup}','{reqUser}');")
            response  = cursor.fetchall()
            cursor.close()
            connection.close()
            st.text(response)
            # Mark the request as processed
            reqUser = None
            reqGroup = None

        if st.button(f"Reject", key=f'R-{key}'):
            connection = connect_to_database()
            cursor = connection.cursor()
            cursor.execute(f"DELETE FROM group_requests WHERE group_id = '{reqGroup}' AND username = '{reqUser}';")
            cursor.close()
            connection.commit()
            connection.close()
            st.text('Request rejected')
            # Mark the request as processed
            reqUser = None
            reqGroup = None
           


def get_group_requests(group_id):
    st.subheader("Join Requests:")
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute(f"call get_group_requests('{group_id}')")
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    if result:
        for it in result:
            print(it)
            display_group_requests(it)  
    else :
        st.warning("There are No requests pending")
 

def display_group_details(group_details):
    st.subheader("Group Details")
    st.table(pd.DataFrame([group_details], columns=["Group ID", "Group Name", "Group Description","Group Owner","date created","member count","previously_visited_location","pending Requests"]))


def get_group_details(group_id):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute(f"call get_group_details('{group_id}')")
    result = cursor.fetchall()
    cursor.close()
    connection.close()
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
    cursor.close()
    connection.close()
    st.subheader("Group Events")
    #print(result)
    if result == []:
        st.warning("There are no events in this group.")
    else:
        for event in result:
            display_event_details(event)


def GroupsPage(User1):
    st.text(f"Welcome, {User1}")
    
    # Display the user's groups here
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute(f"call get_user_groups('{User1}')")
    result = cursor.fetchall()
    #print(result)
    #creating a dropdown menu for the user to select a group
    # Extract group names from the results
    group_names = [group[1] for group in result]
    
    if group_names:
        # Create a selectbox with group names
        selected_group_name = st.selectbox("Your Groups :", group_names)

        selected_group_id = [group[0] for group in result if group[1] == selected_group_name][0]

        get_group_details(selected_group_id)
        Choice = st.radio("Choose", ("View Group Events","View Group Requests" ))
        if Choice == "View Group Events":
            get_group_events(selected_group_id)
        else:
            get_group_requests(selected_group_id)

    else:
        st.warning("You have no groups to select from.")


# Check if the user is logged in
if 'Username' not in st.session_state:
    st.session_state["Username"] = ""

User1 = st.session_state['Username']

if User1 != "":
    GroupsPage(User1)

else:
    st.warning("You need to log in to access this page.")
