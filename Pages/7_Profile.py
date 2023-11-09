import streamlit as st
import mysql.connector
from mysql.connector import Error
import pandas as pd
import random

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
    
# Function to update user information in the database
def update_user_info(username, email, Street, City, State, Gender, Password, About, new_password_updation=False):
    connection = connect_to_database()
    cursor = connection.cursor()

    # Call the stored procedure with the provided parameters
    cursor.callproc("UpdateUserInfo", (username, email, Street, City, State, Gender, Password, About))  
    cursor.close()
    connection.close()
    st.success("User information updated successfully.")


def check_hash():
    hashkey = st.text_input("Enter your Hashkey")
    if st.button("Become a Pro Member!"):

        User1 = st.session_state["Username"]
        connection = connect_to_database()
        cursor = connection.cursor()
        cursor.execute("call checkHash(%s,%s)",(User1, hashkey) )
        result= cursor.fetchone()
        cursor.close()
        connection.close()
        print(result[0])
        if(result[0]):
            st.text("You are now a Pro user!")
            st.session_state['is_pro_member'] = 1
        else:
            st.warning("Wrong Hashkey")

def display_user_prof(User1,user_info):

    email =  st.text_input('Email',user_info[1])
    Street = st.text_input('Street',user_info[2])
    City = st.text_input('City',user_info[3])
    State = st.text_input('State',user_info[4])
    st.text(f"Gender: {user_info[5]}")
    Gender = st.radio(f'Gender:{user_info[5]}',options=["Male","Female","Prefer not to say"],horizontal=True,)
    st.text(f"selected:{Gender}")
    Password = st.text_input('Password',user_info[6],type="password")
    Password2 = st.text_input('Password Confirmation',user_info[6], type="password")
    About = st.text_input('About',user_info[7])
    if(user_info[9]):
        st.text("✅ Pro membership active.")
    else: 
        check_hash()
        

        
    if(st.button('Make Changes')):
        if(Password != user_info[6]):
            if(Password != Password2):
                st.warning("New Passwords do not match")
            else:
                update_user_info(User1 ,email,Street,City,State,Gender,Password,About,new_password_updation=True)
        else:
            update_user_info(User1,email,Street,City,State,Gender,Password,About,new_password_updation=False)



def deleteUser(User1):
    st.warning("Are you sure you want to delete your profile? This action cannot be undone.")
    confirmation = st.text_input("Type 'DELETE' to confirm")
    if(st.button("Confirm")):
        if(confirmation == "DELETE"):
            # connection = connect_to_database()
            # cursor = connection.cursor()
            # cursor.execute(f"call UpdateGroupAdminAndDeleteGroup('{User1}')")
            # cursor.execute(f"DELETE FROM users WHERE username = '{User1}'")
            # connection.commit()
            # cursor.close()
            # connection.close()
            st.success("Your profile has been deleted.")
            st.session_state["Username"] = ""
            st.session_state["is_pro_member"] = 0
        else:
            st.text("couldn't delete profile")

def ProfilePage(User1):
    st.subheader(f"Hey, {User1}, feel like changing your profile?")
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM users WHERE username = '{User1}'")
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    display_user_prof(User1,result[0])
            


# Check if the user is logged in
if 'Username' not in st.session_state:
    st.session_state["Username"] = ""

User1 = st.session_state['Username']

if User1 != "":
    ProfilePage(User1)

else:
    st.warning("You need to log in to access this page.")
