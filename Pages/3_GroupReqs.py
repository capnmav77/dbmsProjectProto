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
    st.table(pd.DataFrame([group_details], columns=["Group ID", "Group Name", "Group Description","Group Owner","date created","member count","previously_visited_location","Pending Requests"]))
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
    if result:
        for it in result:
            print(it)
            display_group_requests(it)  
    else :
        st.warning("There are No requests pending")
    


#Check if the user is logged in
if 'Username' not in st.session_state:
    st.session_state["Username"] = ""

User1 = st.session_state['Username']

if User1 != "":
    User1 = st.session_state['Username']
    st.text(f"Welcome, {User1}")
    
    # Display the user's groups here
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute(f"call get_admin_groups('{User1}')")
    result = cursor.fetchall()
    cursor.close()
    #creating a dropdown menu for the user to select a group
    group_names = [group[1] for group in result]
    
    if group_names:
        # Create a selectbox with group names
        selected_group_name = st.selectbox("Your Groups :", group_names)
        # Find the corresponding group_id for the selected group name
        selected_group_id = [group[0] for group in result if group[1] == selected_group_name][0]
        
        # Call the get_group_events function with the selected group_id
        choice = st.radio('Select an option',('View Group Details','View Group Requests'))
        if choice == 'View Group Details':
            get_group_details(selected_group_id)
        elif choice == 'View Group Requests':
            get_group_requests(selected_group_id)
        else:
            st.text("choose an option")

    else:
        st.warning("You have no groups")

else:
    st.warning("You need to log in to access this page.")
