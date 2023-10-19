import mysql.connector
import streamlit as st

# Establish a connection to MySQL Server

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="Fest_Database"


)
mycursor=mydb.cursor()
print("Connection Established")

# create a streamlit instance to display the data
def streamlitUI():
    st.title("Fest Database")
    st.sidebar.title("options")
    option = st.sidebar.selectbox("Select the option", ["Home", "Add", "Search", "Delete", "Update"])
    if(option == "Home"):
        home()
    elif(option == "Add"):
        add()
    elif(option == "Search"):
        search()
    elif(option == "Delete"):
        delete()
    elif(option == "Update"):
        update()
    
def home():
    st.title("Home") 
    mycursor.execute("show tables")
    myresult = mycursor.fetchall()
    st.write("Tables in the database")
    for it in myresult:
        st.write(it)


def add():
    st.title("Add")

def search():
    st.title("Search")

def delete():
    st.title("Delete")

def update():
    st.title("Update")



def main():
    streamlitUI()

main()