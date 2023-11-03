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
def display_requests(requests):
    st.text("pending requests")
    #the dataframe with the column names as the column names of the table
    df = pd.DataFrame(requests,columns=['Group ID','Group Name','Admin Name','Member Count'])
    st.dataframe(df)
    
def get_pending_requests(User1):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute(f"select  group_id as dId ,ho_group_name as gName , admin_name as adName , member_count as MC from  group_requests as gr join ho_group as jg where gr.group_id = jg.ho_group_id and gr.username = '{User1}';")
    result = cursor.fetchall()
    # print(result)
    if(len(result)==0):
        st.text("No pending requests")
    else:
        display_requests(result)
    
def check_group_exists(groupName):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute(f"select check_group_exists('{groupName}')")
    result = cursor.fetchone()
    cursor.close()
    if result[0] == 1:
        return 1
    else :
        return 0



#Check if the user is logged in
if 'Username' not in st.session_state:
    st.session_state["Username"] = ""

User1 = st.session_state['Username']

if User1 != "":
    #get user's group req
    st.title("Join Groups")
    userGroupId = st.text_input("Enter the Group ID")
    if st.button("search and request"):
        if check_group_exists(userGroupId) :
            connection = connect_to_database()
            cursor = connection.cursor()
            cursor.execute(f"call add_group_requests('{userGroupId}','{User1}');")
            response = cursor.fetchall()
            
            st.text(response[0][0])

        else:
            st.text("The group doesn't exists check your group-id")
    get_pending_requests(User1)
    

else:
    st.warning("You need to log in to access this page.")
