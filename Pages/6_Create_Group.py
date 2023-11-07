
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
    
def create_new_group(User1):
    st.title("Create Group")
    st.text("Create a group to hang out with your friends!")
    
    group_name = st.text_input("Group Name")
    group_description = st.text_input("Group Description")
    
    if st.button("Create Group"):
        if group_name and group_description:
            # Establish a connection to the database
            connection = connect_to_database()
            if connection:
                cursor = connection.cursor()
                
                # Fetch the latest group ID from the database and increment it by 1
                cursor.execute("SELECT MAX(CAST(SUBSTRING(ho_group_id, 2) AS SIGNED)) FROM ho_group")
                latest_group_id = cursor.fetchone()[0]
                print(latest_group_id)
                if latest_group_id is None:
                    latest_group_id = 0
                new_group_id = f'G{latest_group_id + 1:05d}'
                print(new_group_id)
                
                # Insert the new group into the database
                cursor.execute("INSERT INTO ho_group (ho_group_id, ho_group_name, ho_group_desc, admin_name, date_created) VALUES (%s, %s, %s, %s, CURDATE());", (new_group_id, group_name, group_description, User1))
                connection.commit()
                cursor.execute(f"INSERT INTO user_groups  VALUES ('{User1}', '{new_group_id}', CURDATE());")
                connection.commit()
                
                st.success(f"Group '{group_name}' (Group ID: {new_group_id}) has been created successfully.")
            else:
                st.error("Database connection error.")
        else:
            st.error("Please fill in all the required information.")


def delete_group(User1):
     # Display the user's groups here
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute(f"call get_admin_groups('{User1}')")
    result = cursor.fetchall()
    print(result)
    connection.close()
    #creating a dropdown menu for the user to select a group
    # Extract group names from the results
    group_names = [group[1] for group in result]
    
    if group_names:
        # Create a selectbox with group names
        selected_group_name = st.selectbox("Your Groups :", group_names)
        #st.text(f"You selected {selected_group_name}")
        
        # Find the corresponding group_id for the selected group name
        selected_group_id = [group[0] for group in result if group[1] == selected_group_name][0]

        if st.button("Delete Group"):
            connection = connect_to_database()
            cursor = connection.cursor()
            cursor.execute(f"DELETE FROM ho_group WHERE ho_group_id = '{selected_group_id}';")
            connection.commit()
            connection.close()
            st.success(f"Group '{selected_group_name}' (Group ID: {selected_group_id}) has been deleted successfully.")
    else:
        st.warning("You have no groups to select from.")


# Check if the user is logged in
if 'Username' not in st.session_state:
    st.session_state["Username"] = ""

if 'is_pro_member' not in st.session_state:
    st.session_state["is_pro_user"] = 0

User1 = st.session_state['Username']
is_pro_user = st.session_state['is_pro_member']



if User1 != "" and is_pro_user == 1:
    Choice = st.radio("Choose", ("Create Group", "Delete Group"))
    if Choice == "Create Group":
        create_new_group(User1)
    else:
        delete_group(User1)

else:
    st.error("👑Premium Membership is required to access this page.")

