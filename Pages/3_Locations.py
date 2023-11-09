import streamlit as st
import mysql.connector
from mysql.connector import Error

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

def fetch_location_details():
    with connect_to_database() as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT location_name, location_type, street, city, state, location_contact, location_desc, location_rating, location_img FROM vis_locations")
            location_data = cursor.fetchall()
    st.table(location_data)

def add_new_location():
    with connect_to_database() as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT interest_name , interest_desc FROM interests ")
            interests = cursor.fetchall()
            interest_names = [interest[0] for interest in interests]
            interest_descs = [interest[1] for interest in interests]

        location_name = st.text_input("Location Name")
        if location_name:
            #check for ' in the location name
            if "'" in location_name:
                st.error("Location name cannot contain '")
                return
            #check if location already exists
            with connect_to_database() as connection:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT location_name FROM vis_locations")
                    location_names = [row[0] for row in cursor.fetchall()]
            if location_name in location_names:
                st.error("Location already exists")
                return
            
        
        location_type = st.selectbox("Location Type", interest_names)
        street = st.text_input("Street")
        city = st.text_input("City")
        state = st.text_input("State")
        location_contact = st.text_input("Contact")
        location_desc = st.text_area("Description")
        location_rating = st.number_input("Rating", min_value=1, max_value=5)

        if st.button("Add Location"):
            selected_interest = interests[interest_names.index(location_type)]
            with connect_to_database() as connection:
                with connection.cursor() as cursor:
                    try:
                        cursor.execute("INSERT INTO vis_locations (location_name, location_type, street, city, state, location_contact, location_desc, location_rating) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                                       (location_name, selected_interest[0], street, city, state, location_contact, location_desc, location_rating))
                        connection.commit()
                        st.success("Location added successfully!")
                    except Error as e:
                        st.error(f"Error adding location: {e}")

def delete_location():
    with connect_to_database() as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT location_name FROM vis_locations")
            location_names = [row[0] for row in cursor.fetchall()]
    
        selected_location_name = st.selectbox("Select a Location to Delete:", location_names)
    
        if st.button("Delete Location"):
            with connect_to_database() as connection:
                with connection.cursor() as cursor:
                    try:
                        cursor.execute("DELETE FROM vis_locations WHERE location_name = %s", (selected_location_name,))
                        connection.commit()
                        st.success(f"Location '{selected_location_name}' has been deleted.")
                    except Error as e:
                        st.error(f"Error: {e}")



def update_location():
    st.warning("Select a location to update from the list below.")
    
    with connect_to_database() as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT location_name FROM vis_locations")
            location_names = [row[0] for row in cursor.fetchall()]

    selected_location = st.selectbox("Select a location to update:", location_names)

    if selected_location:
        with connect_to_database() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT location_type, street, city, state, location_contact, location_desc, location_rating, location_img FROM vis_locations WHERE location_name = %s", (selected_location,))
                location_data = cursor.fetchone()
            with connection.cursor() as cursor:
                cursor.execute("SELECT interest_name FROM interests")
                interests = cursor.fetchall()
                interest_names = [interest[0] for interest in interests]
        
        st.subheader(f"Current Details for {selected_location}")
        st.write(f"Location Type: {location_data[0]}")
        st.write(f"Street: {location_data[1]}")
        st.write(f"City: {location_data[2]}")
        st.write(f"State: {location_data[3]}")
        st.write(f"Location Contact: {location_data[4]}")
        st.write(f"Location Description: {location_data[5]}")
        st.write(f"Location Rating: {location_data[6]}")
        
        st.subheader(f"Update Details for {selected_location}")
        new_location_type = st.selectbox("Location Type", interest_names)
        new_street = st.text_input("Street", value=location_data[1])
        new_city = st.text_input("City", value=location_data[2])
        new_state = st.text_input("State", value=location_data[3])
        new_location_contact = st.text_input("Location Contact", value=location_data[4])
        new_location_desc = st.text_area("Location Description", value=location_data[5])
        new_location_rating = st.number_input("Location Rating", value=location_data[6])

        if st.button("Update Location"):
            with connect_to_database() as connection:
                with connection.cursor() as cursor:
                    cursor.execute("UPDATE vis_locations SET location_type=%s, street=%s, city=%s, state=%s, location_contact=%s, location_desc=%s, location_rating=%s WHERE location_name=%s",
                                   (new_location_type, new_street, new_city, new_state, new_location_contact, new_location_desc, new_location_rating, selected_location))
                    connection.commit()
                    st.success(f"{selected_location} has been updated successfully!")



def LocationPage(User1):
    st.title("Location Page")
    st.text(f"Welcome, {User1}")
    
    Choice  = st.radio("Select an option", ("View Location Details", "Add a new Location", "Delete a Location", "Update a Location"))
    
    if Choice == "View Location Details":
        st.subheader("Location Details")
        fetch_location_details()
    elif Choice == "Add a new Location":
        st.subheader("Add a new Location")
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

if User1 != "":
    LocationPage(User1)
else:
    st.warning("You need to log in to access this page.")
