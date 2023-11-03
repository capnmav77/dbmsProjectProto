import streamlit as st
import mysql.connector
from mysql.connector import Error


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
    

# Define a function to fetch location details from the database
def fetch_location_details():
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("SELECT location_name, location_type, street, city, state, location_contact, location_desc, location_rating, location_img FROM vis_locations")
    location_data = cursor.fetchall()
    st.table(location_data)

def add_new_location():
    #bharath do this
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("SELECT location_name, location_type, street, city, state, location_contact, location_desc, location_rating, location_img FROM vis_locations")
    location_data = cursor.fetchall()
    st.table(location_data)

def delete_location():
    #bharath do this
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("SELECT location_name, location_type, street, city, state, location_contact, location_desc, location_rating, location_img FROM vis_locations")
    location_data = cursor.fetchall()
    st.table(location_data)

def update_location():
    #bharath do this
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("SELECT location_name, location_type, street, city, state, location_contact, location_desc, location_rating, location_img FROM vis_locations")
    location_data = cursor.fetchall()
    st.table(location_data)


def LocationPage(User1):
    st.title("Location Page")
    st.text(f"Welcome, {User1}")
    
    Choice  = st.radio("Select an option", ("View Location Details", "Add a new Location", "Delete a Location", "Update a Location"))
    
    if Choice == "View Location Details":
        st.subheader("Location Details")
        fetch_location_details()
    elif Choice == "Add a new Location":
        st.subheader("add a new Location")
        add_new_location()
    elif Choice == "Delete a Location":
        st.subheader("Delete a Location")
        delete_location()
    elif Choice == "Update a Location":
        st.subheader("Update a Location")
        update_location()
    else:
        st.error("Invalid Choice")





if 'Username' not in st.session_state:
    st.session_state["Username"] = ""

User1 = st.session_state['Username']
# Create the Streamlit web app
if User1 != "":
    LocationPage(User1)
    
else:
    st.warning("You need to log in to access this page.")