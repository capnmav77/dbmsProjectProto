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
    
def update_user_info(email,street,city,state,gender,password,about,new_password_updation = False):
    if(new_password_updation == True):
        st.text("updated password with user info")
        #code for changing user information
    else:
        st.text("Updated user_info")
        #code for changing user information with password


def display_user_prof(user_info):

    email =  st.text_input('Email',user_info[1])
    Street = st.text_input('Street',user_info[2])
    City = st.text_input('City',user_info[3])
    State = st.text_input('State',user_info[4])
    st.text(f"Gender: {user_info[5]}")
    Gender = st.radio(f'Gender:{user_info[5]}',options=["Male","Female","Prefer not to say"],horizontal=True,)
    st.text(f"selected:{Gender}")
    Password = st.text_input('Password',user_info[6])
    Password2 = st.text_input('Password Confirmation',user_info[6])
    About = st.text_input('About',user_info[7])
    if(user_info[9]==1):
        st.text("✅ Pro membership activated.")
    else: 
        st.text("try out the Pro membership")

        
    if(st.button('make changes')):
        if(Password != user_info[6]):
            if(Password != Password2):
                st.warning("New Passwords don't match try again")
            else:
                update_user_info(email,Street,City,State,Gender,Password,About,new_password_updation=True)
        else:
            update_user_info(email,Street,City,State,Gender,Password,About,new_password_updation=False)
                        
            


# Check if the user is logged in
if 'Username' not in st.session_state:
    st.session_state["Username"] = ""

User1 = st.session_state['Username']

if User1 != "":
    User1 = st.session_state['Username']
    st.subheader(f"Hey, {User1}, feel like changing your profile?")
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM users WHERE username = '{User1}'")
    result = cursor.fetchall()
    connection.close()
    display_user_prof(result[0])
    
else:
    st.warning("You need to log in to access this page.")
