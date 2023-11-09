import streamlit as st
import mysql.connector
from mysql.connector import Error
import pandas as pd
from datetime import datetime


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
    


def current_date():
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("SELECT CURDATE()")
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result[0]



def display_group_requests(request):
    reqUser = request[1]
    reqGroup = request[0]
    
    if reqUser and reqGroup:
        key = f'{reqUser}-{reqGroup}'
        st.text("User name: " + reqUser + " is requesting to join this group")

        #making the accept and reject buttons in the same row
        column1 , column2 = st.columns(2)
        response = None

        with column1:
            if st.button(f"Accept", key=f'A-{key}'):
                connection = connect_to_database()
                cursor = connection.cursor()
                cursor.execute(f"CALL accept_group_request('{reqGroup}','{reqUser}');")
                response  = cursor.fetchall()
                cursor.close()
                connection.close()
                response = "Request accepted"
                # st.text(response)
                # # Mark the request as processed
                reqUser = None
                reqGroup = None
            
        with column2:
            if st.button(f"Reject", key=f'R-{key}'):
                connection = connect_to_database()
                cursor = connection.cursor()
                cursor.execute(f"DELETE FROM group_requests WHERE group_id = '{reqGroup}' AND username = '{reqUser}';")
                cursor.close()
                connection.commit()
                connection.close()
                response = "Request rejected"
                # st.text('Request rejected')
                # # Mark the request as processed
                reqUser = None
                reqGroup = None
        if(response != None):
            st.text(response)
    else:
        st.warning("There are no requests to display")



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
        st.markdown(
            """
            <style>
            .event-container {
                background-color: #ffffff;
                padding: 10px;
                border-radius: 5px;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        st.title(event_details[1])
        
        # Format the date and time
        event_date = event_details[3].strftime("%Y-%m-%d")
        event_time = event_details[4].total_seconds() / 3600  # Convert timedelta to hours

        curr_date = current_date().strftime("%Y-%m-%d")
        curr_datetime = datetime.strptime(curr_date, "%Y-%m-%d")
        event_datetime = datetime.strptime(event_date, "%Y-%m-%d")
        
        if curr_datetime > event_datetime:
            st.warning("This event has already passed, deleting event... ")
            connection = connect_to_database()
            cursor = connection.cursor()
            cursor.execute(f"DELETE FROM planned_event WHERE event_id = '{event_details[0]}'")
            connection.commit()
            cursor.close()
            connection.close()
        
        st.text("Event Location: " + event_details[2])
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
    print(result)
    if result == []:
        st.warning("There are no events in this group.")
    else:
        for event in result:
            display_event_details(event)


def leave_group_user(username,group_id):
    st.subheader("Leave Group")
    st.warning("you are about to exit the group")
    if(st.button("Leave Group")):
        connection = connect_to_database()
        cursor = connection.cursor()
        cursor.execute(f"delete from user_groups where username = '{username}' and group_id = '{group_id}';")
        connection.commit()
        cursor.close()
        connection.close()
        st.text("You have left the group")


def leave_group_admin(username,group_id):
    st.subheader("Leave Group")
    st.warning("Since you are the admin, select the next user for the group")
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute(f"select * from user_groups where group_id = '{group_id}';")
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    members = [member[0] for member in result]
    print(username)
    members.remove(username)
    next_group_admin = st.selectbox("Select the next admin",members)
    print(members)
    if(len(members) == 0):
        st.warning("Since there are no members in the group , directly delete the group")
    else:
        if(st.button("Change Admin")):
            connection = connect_to_database()
            cursor = connection.cursor()
            cursor.execute(f"update ho_group set admin_name = '{next_group_admin}' where ho_group_id = '{group_id}';")
            connection.commit()
            cursor.close()
            st.text("Admin changed successfully")
    
        if(st.button("Change Admin and Leave Group")):
            connection = connect_to_database()
            cursor = connection.cursor()
            cursor.execute(f"update ho_group set admin_name = '{next_group_admin}' where ho_group_id = '{group_id}';")
            connection.commit()
            cursor.close()
            cursor = connection.cursor()
            cursor.execute(f"delete from user_groups where username = '{username}' and group_id = '{group_id}';")
            connection.commit()
            cursor.close()
            connection.close()
            st.text("You have left the group")



def GroupsPage(User1):
    st.text(f"Welcome, {User1}")
    
    # Display the user's groups here
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute(f"call get_user_groups('{User1}')")
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    
    #print(result)
    #creating a dropdown menu for the user to select a group and Extract group names from the results

    group_names = [group[1] for group in result]

    
    if group_names:
        # Create a selectbox with group names
        selected_group_name = st.selectbox("Your Groups :", group_names)

        selected_group_id = [group[0] for group in result if group[1] == selected_group_name][0]
        selected_group_admin = [group[2] for group in result if group[1] == selected_group_name][0]
        
        # Display the group details
        get_group_details(selected_group_id)
        if(selected_group_admin == User1):
            Choice = st.radio("Choose", ("View Group Events","View Group Requests","Leave Group" ))
            if Choice == "View Group Events":
                get_group_events(selected_group_id)
            elif (Choice == "Leave Group") :
                leave_group_admin(User1,selected_group_id)
            else:
                get_group_requests(selected_group_id)
        else:
            choice = st.radio("Choose", ("View Group Events","Leave Group" ))
            if choice == "View Group Events":
                get_group_events(selected_group_id)
            else :
                leave_group_user(User1,selected_group_id)

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
