import streamlit as st
import mysql.connector
from mysql.connector import Error

# # Create a connection to the MySQL database
# db_connection = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="1234",
#     database="hang_out"
# )

# # Create a cursor to execute SQL queries
# cursor = db_connection.cursor()
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
    

if 'Username' not in st.session_state:
    st.session_state["Username"] = ""

User1 = st.session_state['Username']
   
# Define a function to fetch location details from the database
def fetch_location_details():
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("SELECT location_name, location_type, street, city, state, location_contact, location_desc, location_rating, location_img FROM vis_locations")
    location_data = cursor.fetchall()
    return location_data

# Create the Streamlit web app
if User1 != "":
    st.title("Location Details")
    User1 = st.session_state['Username']
    st.text(f"Welcome, {User1}")
    
    # Display the user's groups here
    connection = connect_to_database()
    cursor = connection.cursor()
    # Fetch location details from the database
    location_data = fetch_location_details()

    # Display location details in a Streamlit table
    st.table(location_data)

# if __name__ == '__main__':
#     location_app()
else:
    st.warning("You need to log in to access this page.")