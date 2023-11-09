
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
    

def get_latest_id():
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("SELECT MAX(CAST(SUBSTRING(event_id, 2) AS SIGNED)) FROM planned_event")
    latest_group_id = cursor.fetchone()[0]
    #print(latest_group_id)
    if latest_group_id is None:
        latest_group_id = 0
    new_group_id = f'E{latest_group_id + 1:05d}'
    #print(new_group_id)
    cursor.close()
    connection.close()
    return new_group_id


def check_for_duplicates(event_name , group_id , event_date , event_time):
    print(event_name , group_id)
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute(f"select count(*) from planned_event where event_name = '{event_name}' and group_id = '{group_id}' and event_date = '{event_date}' and event_time = '{event_time}' ")
    result = cursor.fetchone()
    #print(result)
    cursor.close()
    connection.close()
    return result[0]



def DeleteEvent(User1):
    st.subheader("Delete Events")

    # Get the list of events for the user to select for deletion
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute(f"SELECT event_name, event_date, event_time , group_id , event_id FROM planned_event WHERE group_id IN (SELECT group_id FROM user_groups WHERE username = '{User1}')")
    events_data = cursor.fetchall() 
    #print(events_data)
    cursor.close()
    connection.close()

    if not events_data:
        st.warning("No events found for deletion.")
        return

    event_options = [f"{event[0]} - {event[3]} - {event[1]} - {event[2]} - {event[4]} " for event in events_data]

    selected_event = st.selectbox("Select an event to delete:", event_options)

    if st.button("Delete Selected Event"):

        #process the input
        selected_event_name = selected_event.split(' - ')[0]
        selected_event_date = selected_event.split(' - ')[2].split(' ')[0]
        selected_event_time = selected_event.split(' - ')[3]
        selected_event_id = selected_event.split(' - ')[-1].strip()  # Use strip() to remove spaces
        #print(selected_event_id)

        #connection to database and deletion
        connection = connect_to_database()
        cursor = connection.cursor()
        cursor.execute(f"DELETE FROM planned_event WHERE event_id = '{selected_event_id}';")
        connection.commit()
        cursor.close()
        connection.close()
        st.success(f"Event '{selected_event_name}' on {selected_event_date} at {selected_event_time} has been deleted.")

def AddEvents(User1):
    st.title("Add Events")

    #connection for getting the groups of the user
    connection = connect_to_database()
    cursor = connection.cursor()

    cursor.execute(f"SELECT ho_group_id , ho_group_name FROM ho_group join user_groups on user_groups.group_id = ho_group.ho_group_id WHERE username = '{User1}'")
    groups_data = cursor.fetchall()
    cursor.close()

    #fetch the locations from the database
    cursor = connection.cursor()
    cursor.execute(f"SELECT location_name FROM vis_locations")
    locations_data = cursor.fetchall()

    cursor.close()
    connection.close()
    
    if not groups_data:
        st.warning("You are not a member of any groups.")
    
    group_options = [group[0] for group in groups_data]
    location_options = [location[0] for location in locations_data] 

    # Get user input for event details
    event_name = st.text_input("Event Name:")
    selected_group = st.selectbox("Select a group to add an event to:", group_options)
    group_id = selected_group
    location_name = st.selectbox("Select a location for the event:", location_options)
    event_date = st.date_input("Event Date / YYYY-MM-DD")
    event_time = st.time_input("Event Time / HH-MM-SS")
    event_description = st.text_area("Event Description")

    if st.button("Add Event"):
        connection = connect_to_database()
        cursor = connection.cursor()
        cursor.execute(f"SELECT ug.group_id FROM user_groups ug WHERE ug.username = '{User1}' AND ug.group_id =  '{group_id}';")
        group_id = cursor.fetchone()
        cursor.close()
        print(group_id)

        if group_id:
            #connection = connect_to_database()
            cursor = connection.cursor()
            # Check if the location exists
            cursor.execute("SELECT location_name FROM vis_locations WHERE location_name = %s", (location_name,))
            existing_location = cursor.fetchone()
            cursor.close()


            if not existing_location:
                st.error(f"Location '{location_name}' does not exist in the database.")
            else:
                # Insert the event into the database
                group_id = group_id[0]
                event_id = get_latest_id()
                #print(event_date , event_time , event_id , group_id)

                #null constraint
                if (event_description == "") :
                    event_description = "a random fun event"


                #check for pre existing event : 
                result = check_for_duplicates(event_name, group_id, event_date, event_time)
                #print(result)

                if result == 0:
                    #push to database 
                    cursor = connection.cursor()
                    cursor.execute(f"INSERT INTO planned_event values ('{event_id}','{event_name}', '{group_id}','{location_name}', '{event_date}','{event_time}','{event_description}', 0)")
                    connection.commit()
                    cursor.close()
                    connection.close()
                    st.success("Event added successfully!")

                else:
                    st.warning("Event already exists.")
                    connection.close()
        else:
            st.error(f"Group '{group_id}' does not exist or you are still in the process of joining group.") 
            connection.close()   


def update_event(User1):
    st.subheader("Update Event")

    #connection to database
    connection = connect_to_database()
    cursor = connection.cursor()

    # Get the list of events that the user can update
    cursor.execute(f"SELECT event_name, group_id, event_date, event_time FROM planned_event WHERE group_id IN (SELECT group_id FROM user_groups WHERE username = '{User1}')")
    events_data = cursor.fetchall()

    if not events_data:
        st.warning("No events found that can be updated.")
        cursor.close()
        return

    selected_event = st.selectbox("Select an event to update:", [f"{event[0]} - {event[1]} - {event[2]} - {event[3]}" for event in events_data])

    # Extract event details
    selected_event = selected_event.split(" - ")
    event_name, group_id, event_date, event_time = selected_event

    new_event_name = st.text_input("New Event Name:", event_name)
    new_event_date = st.date_input("New Event Date:", pd.to_datetime(event_date).date())
    new_event_time = st.time_input("New Event Time:", pd.to_datetime(event_time).time())
    new_event_description = st.text_area("New Event Description")

    if st.button("Update Event"):
        cursor.execute(f"UPDATE planned_event SET event_name = '{new_event_name}', event_date = '{new_event_date}', event_time = '{new_event_time}', event_desc = '{new_event_description}' WHERE event_name = '{event_name}' AND group_id = '{group_id}' AND event_date = '{event_date}' AND event_time = '{event_time}'")
        connection.commit()
        st.success("Event updated successfully!")

    cursor.close()
    connection.close()

# Check if the user is logged in
if 'Username' not in st.session_state:
    st.session_state["Username"] = ""

User1 = st.session_state['Username']

if User1 != "":
    st.title("Event-Page")
    Choice = st.radio("Select an option", ("Create Event", "Update Event", "Delete Event"))

    if Choice == 'Create Event':
        AddEvents(User1)
    elif Choice == 'Delete Event':
        DeleteEvent(User1)
    elif Choice == 'Update Event':
        update_event(User1)

else:
    st.warning("You need to log in to access this page.")


