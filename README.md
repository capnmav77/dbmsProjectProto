# HangOut

Welcome to Hang_out! This is a web application built with streamlit and mysql.

## Getting Started

To get started with Hang_out, follow these steps:

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/capnmav77/dbmsProjectProto.git
   ```

2. Start the development server:

   ```bash
   open mysql workbench or use mysql command line
   in order to create a database the sql file in ./database files
   ```

3. change the necessary user credentials in order to login to the database:
   ```bash
   def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="Your User Name here",
            password="Your Password Here",
            database="hang_out"
        )
        return connection
    except Error as e:
        st.error(f"Error: {e}")
        return None
   ```

4. Run the streamlit app:

   ```bash
   streamlit run home.py
   ```

5. Open your web browser and navigate to http://localhost:3000 to view the application.

That's it! You should now be able to view and interact with Hang_out in your web browser. If you have any issues or questions, please refer to the project documentation or reach out to the project maintainers.
