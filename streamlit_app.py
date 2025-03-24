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
    # Load user data from the pickle file
    user_data = load_user_data()

    # Check if username exists and password matches
    if username in user_data and user_data[username] == password:
        st.session_state.logged_in = True
        st.session_state.username = username
        return True
    else:
        return False

# Function to simulate creating a new user
def create_user(username, password):
    # Load existing user data
    user_data = load_user_data()
    
    # Add new user to the user_data session state (as an in-memory dictionary)
    if username in user_data:
        st.error(f"User {username} already exists!")
    else:
        user_data[username] = password
        save_user_data(user_data)  # Save updated user data to the pickle file
        st.success(f"User {username} created successfully!")

# Function to logout the user
def logout():
    # Clear session state
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
    # Admin Page: Only accessible if logged in as an admin
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

        # View existing users (for admin purposes)
        if st.button("View Existing Users"):
            user_data = load_user_data()
            st.write(user_data)

        # View form data (for admin purposes)
        if st.button("View Form Submissions"):
            form_data = load_form_data()
            st.write(form_data)

    # If the user is not logged in, show the login form
    elif not st.session_state.logged_in:
        st.title("Login Page")
        username = st.text_input("Enter your Username:")
        password = st.text_input("Enter your Password", type="password")

        if st.button("Login"):
            if login(username, password):
                st.success(f"Welcome, {username}!")
            else:
                st.error("Invalid username or password.")
    
    # After login, show the form page
    else:
        if st.session_state.form_started:
            # Display logout button on top-right
            logout_button = st.button("Logout", key="logout_button", help="Click to logout")
            
            if logout_button:
                logout()

            st.title("Form Submission Page")
            st.write(f"Hello, {st.session_state.username}! Please fill in the form below.")
        
            # Dropdown 1 (Cohort)
            cohort = st.selectbox("Select Cohort", options=[""] + list(data.keys()), index=0)

            if cohort:
                # Dropdown 2 (LOB)
                lob_options = list(data[cohort].keys())
                lob = st.selectbox("Select LOB", options=[""] + lob_options, index=0)

                if lob:
                    # Dropdown 3 (Sub-LOB)
                    sub_lob_options = data[cohort][lob]
                    sub_lob = st.selectbox("Select Sub-LOB", options=[""] + sub_lob_options, index=0)

            # Additional Input Fields
            mpan = st.text_input("MPAN#", placeholder="Enter MPAN number")
            account = st.text_input("Account#", placeholder="Enter Account number")
            status = st.selectbox("Status", options=["", "Ongoing", "Completed"], index=0)

            # Submit Button
            submit_button = st.button("Submit")

            # Handling form submission
            if submit_button:
                if not cohort or not lob or not sub_lob or not mpan or not account or not status:
                    st.error("Please fill the form completely before submitting.")
                else:
                    # Capture the current date and time
                    submission_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    # Collect form data along with username and timestamp
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

                    # Store the form entry
                    st.session_state.form_data.append(form_entry)
                    save_form_data(st.session_state.form_data)  # Save updated form data

                    # Reset the form after submission
                    st.session_state.cohort = ""
                    st.session_state.lob = ""
                    st.session_state.sub_lob = ""
                    st.session_state.mpan = ""
                    st.session_state.account = ""
                    st.session_state.status = ""

                    st.success("Form submitted successfully!")

                    # Offer to download CSV with Submission Time
                    if len(st.session_state.form_data) > 0:
                        df = pd.DataFrame(st.session_state.form_data)
                        csv = df.to_csv(index=False)

                        # Create a download link for the CSV
                        st.download_button(
                            label="Download CSV",
                            data=csv,
                            file_name="form_data_with_submission_time.csv",
                            mime="text/csv"
                        )

                    # After submission, reset the form state and redirect to "Start Form"
                    st.session_state.form_started = False
                    st.experimental_rerun()

        # "Start Form" button
        if not st.session_state.form_started:
            start_form_button = st.button("Start Form")
            if start_form_button:
                st.session_state.form_started = True
                st.experimental_rerun()  # Re-run the app to show the form
        else:
            # Show the form submission page if the user has clicked "Start Form"
            st.title("Form Submission Page")
            st.write(f"Hello, {st.session_state.username}! Please fill in the form below.")

if __name__ == "__main__":
    app()
