import streamlit as st
import pandas as pd
import pickle
import os
from datetime import datetime

# Define file to store user credentials and form data
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
    st.session_state.form_started = False  # Track if the user clicked "Start Form"

# Function to load user data from the pickle file
def load_user_data():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'rb') as f:
            return pickle.load(f)
    else:
        return {"admin": "admin123"}  # Default admin credentials

# Function to save user data to the pickle file
def save_user_data(user_data):
    with open(USER_DATA_FILE, 'wb') as f:
        pickle.dump(user_data, f)

# Function to load form data from the pickle file
def load_form_data():
    if os.path.exists(FORM_DATA_FILE):
        with open(FORM_DATA_FILE, 'rb') as f:
            return pickle.load(f)
    else:
        return []

# Function to save form data to the pickle file
def save_form_data(form_data):
    with open(FORM_DATA_FILE, 'wb') as f:
        pickle.dump(form_data, f)

# Function to simulate login and capture the username
def login(username, password):
    user_data = load_user_data()
    if username in user_data and user_data[username] == password:
        st.session_state.logged_in = True
        st.session_state.username = username
        return True
    return False

# Function to simulate creating a new user
def create_user(username, password):
    user_data = load_user_data()
    if username in user_data:
        st.error(f"User {username} already exists!")
    else:
        user_data[username] = password
        save_user_data(user_data)
        st.success(f"User {username} created successfully!")

# Function to logout the user
def logout():
    st.session_state.logged_in = False
    st.session_state.username = ""

# Data for the form (Cohort, LOB, Sub-LOB)
data = {
    'Exception Management': {
        'HHDC': ['A Flag - No', 'A Flag - Yes'],
        'NHHDC': ['Received D0002s - Daily: NHH Faults']
    },
    'Metering': {
        'Meter Serv BW': ['Aborts - SMETS Install', 'D0002: HH']
    }
}

# Streamlit app
def app():
    if st.session_state.logged_in and st.session_state.username == "admin":
        st.title("Admin Page")
        st.subheader("Create New User")

        new_username = st.text_input("Enter new username")
        new_password = st.text_input("Enter new password", type="password")

        if st.button("Create User"):
            if new_username and new_password:
                create_user(new_username, new_password)
            else:
                st.error("Please provide both a username and a password.")

        if st.button("View Existing Users"):
            st.write(load_user_data())

        if st.button("View Form Submissions"):
            st.write(load_form_data())

    elif not st.session_state.logged_in:
        st.title("Login Page")
        username = st.text_input("Enter your Username:")
        password = st.text_input("Enter your Password", type="password")

        if st.button("Login"):
            if login(username, password):
                st.success(f"Welcome, {username}!")
            else:
                st.error("Invalid username or password.")

    else:
        if st.session_state.form_started:
            if st.button("Logout", key="logout_button"):
                logout()

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
                        "Submission Time": submission_time
                    }

                    st.session_state.form_data.append(form_entry)
                    save_form_data(st.session_state.form_data)

                    st.session_state.form_started = False
                    st.success("Form submitted successfully!")

                    df = pd.DataFrame(st.session_state.form_data)
                    csv = df.to_csv(index=False)

                    st.download_button(
                        label="Download CSV",
                        data=csv,
                        file_name="form_data_with_submission_time.csv",
                        mime="text/csv"
                    )

        # Fixed Start Form Button
        if not st.session_state.form_started:
            if st.button("Start Form"):
                st.session_state.form_started = True

if __name__ == "__main__":
    app()
