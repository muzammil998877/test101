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

# Function to load form data
def load_form_data():
    if os.path.exists(FORM_DATA_FILE):
        with open(FORM_DATA_FILE, 'rb') as f:
            return pickle.load(f)
    else:
        return []

# Function to save form data
def save_form_data(form_data):
    with open(FORM_DATA_FILE, 'wb') as f:
        pickle.dump(form_data, f)

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

# Function to delete a user
def delete_user(username):
    user_data = load_user_data()
    if username in user_data:
        if username == "admin":
            st.error("Cannot delete the admin account!")
        else:
            del user_data[username]
            save_user_data(user_data)
            st.success(f"User {username} deleted successfully!")
            st.rerun()
    else:
        st.error("User not found!")

# Function to log out
def logout():
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.form_started = False
    st.session_state.start_form_time = None
    st.rerun()

# Sample data structure for form options
data = {
    'Exception Management': {
        'HHDC': ['A Flag - No', 'A Flag - Yes'],
        'NHHDC': ['Received D0002s - Daily: NHH Faults']
    },
    'Metering': {
        'Meter Serv BW': ['Aborts - SMETS Install', 'D0002: HH']
    }
}

# Main app function
def app():
    if st.session_state.logged_in and st.session_state.username == "admin":
        # Admin Page
        st.title("Admin Page")
        st.subheader("Create New User")

        new_username = st.text_input("Enter new username")
        new_password = st.text_input("Enter new password", type="password")

        if st.button("Create User"):
            if new_username and new_password:
                create_user(new_username, new_password)
            else:
                st.error("Please provide both a username and a password.")

        # ✅ View & Delete Users Feature
        st.subheader("Manage Users")

        user_data = load_user_data()
        if user_data:
            st.write("### Existing Users:")
            for user in user_data.keys():
                if user != "admin":  # Prevent admin deletion
                    col1, col2 = st.columns([3, 1])
                    col1.write(user)
                    if col2.button(f"Delete {user}", key=f"delete_{user}"):
                        delete_user(user)
        else:
            st.info("No users available.")

        # ✅ View Form Submissions in a Table Format & Download CSV
        st.subheader("View Form Submissions")

        form_data = load_form_data()
        if form_data:
            df = pd.DataFrame(form_data)
            st.dataframe(df)

            # Allow admin to download form submissions as CSV
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Form Submissions as CSV",
                data=csv,
                file_name="form_submissions.csv",
                mime="text/csv"
            )
        else:
            st.info("No form submissions available.")

        # ✅ Logout button for admin
        if st.button("Logout", key="logout_admin"):
            logout()

    elif not st.session_state.logged_in:
        # Login Page
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
        # ✅ Start Form Page (Landing Page)
        st.title("Start Form Page")
        st.write(f"Hello, {st.session_state.username}! Click below to start the form.")

        if not st.session_state.form_started:
            if st.button("Start Form"):
                st.session_state.form_started = True
                st.session_state.start_form_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                st.rerun()

        if st.button("Logout", key="logout_start_page"):
            logout()

        if st.session_state.form_started:
            st.title("Form Submission Page")
            st.write(f"Hello, {st.session_state.username}! Please fill in the form below.")

            cohort = st.selectbox("Select Cohort", options=[""] + list(data.keys()), index=0)

            if cohort:
                lob = st.selectbox("Select LOB", options=[""] + list(data[cohort].keys()), index=0)
                if lob:
                    sub_lob = st.selectbox("Select Sub-LOB", options=[""] + data[cohort][lob], index=0)

            mpan = st.text_input("MPAN#", placeholder="Enter MPAN number")
            account = st.text_input("Account#", placeholder="Enter Account number")
            status = st.selectbox("Status", options=["", "Ongoing", "Completed"], index=0)

            if st.button("Submit"):
                if not cohort or not lob or not sub_lob or not mpan or not account or not status:
                    st.error("Please fill the form completely before submitting.")
                else:
                    submission_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    form_entry = {
                        "Cohort": cohort,
                        "LOB": lob,
                        "Sub-LOB": sub_lob,
                        "MPAN": mpan,
                        "Account": account,
                        "Status": status,
                        "Username": st.session_state.username,
                        "Start Form Time": st.session_state.start_form_time,
                        "Submission Time": submission_time
                    }

                    st.session_state.form_data.append(form_entry)
                    save_form_data(st.session_state.form_data)

                    st.success("Form submitted successfully!")

                    st.session_state.form_started = False
                    st.session_state.start_form_time = None
                    st.rerun()

            if st.button("Logout", key="logout_form_page"):
                logout()

# Run the app
if __name__ == "__main__":
    app()
