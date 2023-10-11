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


mycursor.execute("select * from customers")
myresult=mycursor.fetchall()

print(myresult)

for x in myresult:
    print(x)