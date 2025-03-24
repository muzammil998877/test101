import streamlit as st
import pandas as pd
import pickle
import os
from datetime import datetime

# File storage paths
USER_DATA_FILE = 'user_data.pkl'
FORM_DATA_FILE = 'form_data.pkl'

# Initialize session state variables
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'form_data' not in st.session_state:
    st.session_state.form_data = []
if 'form_started' not in st.session_state:
    st.session_state.form_started = False
if 'start_form_time' not in st.session_state:
    st.session_state.start_form_time = None

# Function to load user data
def load_user_data():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'rb') as f:
            return pickle.load(f)
    else:
        return {"admin": "admin123"}

# Function to save user data
def save_user_data(user_data):
    with open(USER_DATA_FILE, 'wb') as f:
        pickle.dump(user_data, f)

# Function to delete a user
def delete_user(username):
    user_data = load_user_data()
    if username in user_data:
        del user_data[username]  # Remove the user
        save_user_data(user_data)  # Save updated data
        st.success(f"User '{username}' has been deleted successfully.")
    else:
        st.error("User not found.")

# Function to log in a user
def login(username, password):
    user_data = load_user_data()
    if username in user_data and user_data[username] == password:
        st.session_state.logged_in = True
        st.session_state.username = username
        return True
    return False

# Function to create a new user
def create_user(username, password):
    user_data = load_user_data()
    if username in user_data:
        st.error(f"User {username} already exists!")
    else:
        user_data[username] = password
        save_user_data(user_data)
        st.success(f"User {username} created successfully!")

# Function to log out
def logout():
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.form_started = False
    st.session_state.start_form_time = None
    st.rerun()  # Force rerun to return to the login page

# Function to load form data
def load_form_data():
    if os.path.exists(FORM_DATA_FILE):
        with open(FORM_DATA_FILE, 'rb') as f:
            return pickle.load(f)
    return []

# Function to save form data
def save_form_data(form_data):
    with open(FORM_DATA_FILE, 'wb') as f:
        pickle.dump(form_data, f)

# Main app function
def app():
    if st.session_state.logged_in and st.session_state.username == "admin":
        # ✅ Admin Page
        st.title("Admin Page")
        
        # ✅ Create New User Section
        st.subheader("Create New User")
        new_username = st.text_input("Enter new username")
        new_password = st.text_input("Enter new password", type="password")
        
        if st.button("Create User"):
            if new_username and new_password:
                create_user(new_username, new_password)
            else:
                st.error("Please provide both a username and a password.")

        # ✅ Delete User Section
        st.subheader("Delete a User")
        user_data = load_user_data()
        users_list = list(user_data.keys())

        if "admin" in users_list:
            users_list.remove("admin")  # Prevent deleting admin

        if users_list:
            selected_user = st.selectbox("Select a user to delete", users_list)

            if st.button("Delete User"):
                delete_user(selected_user)
                st.rerun()  # Refresh the page after deletion
        else:
            st.info("No users available to delete.")

        # ✅ View Existing Users Section
        if st.button("View Existing Users"):
            st.write(load_user_data())

        # ✅ View Submission Form Data Section
        st.subheader("View Submission Forms Data")
        form_data = load_form_data()

        if form_data:
            df = pd.DataFrame(form_data)
            st.write(df)

            # ✅ Download as CSV button
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="submission_data.csv",
                mime="text/csv",
            )
        else:
            st.info("No form data available.")

        # ✅ Logout button for admin
        if st.button("Logout", key="logout_admin"):
            logout()

    elif not st.session_state.logged_in:
        # ✅ Login Page
        st.title("Login Page")
        username = st.text_input("Enter your Username:")
        password = st.text_input("Enter your Password", type="password")

        if st.button("Login"):
            if login(username, password):
                st.success(f"Welcome, {username}!")
                st.rerun()
            else:
                st.error("Invalid username or password.")

    else:
        # ✅ Start Form Page
        st.title("Start Form Page")
        st.write(f"Hello, {st.session_state.username}! Click below to start the form.")

        if st.button("Start Form"):
            st.session_state.form_started = True
            st.session_state.start_form_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Capture Start Form Time
            st.rerun()

        # ✅ Logout button on Start Form Page
        if st.button("Logout", key="logout_start_page"):
            logout()

# Run the app
if __name__ == "__main__":
    app()
