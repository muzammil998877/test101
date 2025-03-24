import streamlit as st
import pandas as pd
import pickle
import os
from datetime import datetime

USER_DATA_FILE = 'user_data.pkl'
FORM_DATA_FILE = 'form_data.pkl'

# Session State Variables
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'form_data' not in st.session_state:
    st.session_state.form_data = []
if 'form_started' not in st.session_state:
    st.session_state.form_started = False
if 'start_form_time' not in st.session_state:
    st.session_state.start_form_time = None  # ✅ Stores Start Form Time

# Load User Data
def load_user_data():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'rb') as f:
            return pickle.load(f)
    return {"admin": "admin123"}

# Save User Data
def save_user_data(user_data):
    with open(USER_DATA_FILE, 'wb') as f:
        pickle.dump(user_data, f)

# Load Form Data
def load_form_data():
    if os.path.exists(FORM_DATA_FILE):
        with open(FORM_DATA_FILE, 'rb') as f:
            return pickle.load(f)
    return []

# Save Form Data
def save_form_data(form_data):
    with open(FORM_DATA_FILE, 'wb') as f:
        pickle.dump(form_data, f)

# Login Function
def login(username, password):
    user_data = load_user_data()
    if username in user_data and user_data[username] == password:
        st.session_state.logged_in = True
        st.session_state.username = username
        return True
    return False

# Logout Function
def logout():
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.form_started = False
    st.session_state.start_form_time = None  # ✅ Reset start form time
    st.rerun()  # ✅ Redirects back to login page

data = {
    'Exception Management': {
        'HHDC': ['A Flag - No', 'A Flag - Yes'],
        'NHHDC': ['Received D0002s - Daily: NHH Faults']
    },
    'Metering': {
        'Meter Serv BW': ['Aborts - SMETS Install', 'D0002: HH']
    }
}

# Main App
def app():
    if not st.session_state.logged_in:
        # Login Page
        st.title("Login Page")
        username = st.text_input("Enter your Username:")
        password = st.text_input("Enter your Password", type="password")

        if st.button("Login"):
            if login(username, password):
                st.success(f"Welcome, {username}!")
                st.rerun()  # ✅ Redirects to Start Form Page
            else:
                st.error("Invalid username or password.")

    elif st.session_state.logged_in and st.session_state.username == "admin":
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

        if st.button("View Existing Users"):
            st.write(load_user_data())

        # ✅ View and Download Form Submissions
        st.subheader("View Form Submissions")
        form_data = load_form_data()

        if form_data:
            df = pd.DataFrame(form_data)
            st.dataframe(df)

            # Download Button
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Form Submissions as CSV",
                data=csv,
                file_name="form_submissions.csv",
                mime="text/csv"
            )
        else:
            st.info("No form submissions available.")

        # ✅ Logout Button
        if st.button("Logout"):
            logout()

    else:
        # ✅ Start Form Page
        st.title("Start Form Page")

        # ✅ Start Form Button
        if not st.session_state.form_started:
            if st.button("Start Form"):
                st.session_state.start_form_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # ✅ Capture Start Form Time
                st.session_state.form_started = True
                st.rerun()

        # ✅ Logout Button on Start Form Page (Before Form Starts)
        st.write("")
        if st.button("Logout"):
            logout()

        # ✅ Form Submission Page
        if st.session_state.form_started:
            st.title("Form Submission Page")
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
                        "Start Form Time": st.session_state.start_form_time,  # ✅ Added to CSV
                        "Submission Time": submission_time
                    }

                    st.session_state.form_data.append(form_entry)
                    save_form_data(st.session_state.form_data)

                    st.success("Form submitted successfully!")

                    # ✅ Download Form Data as CSV
                    df = pd.DataFrame(st.session_state.form_data)
                    csv = df.to_csv(index=False).encode('utf-8')

                    st.download_button(
                        label="Download CSV",
                        data=csv,
                        file_name="form_data_with_submission_time.csv",
                        mime="text/csv"
                    )

                    # ✅ Reset Form State
                    st.session_state.form_started = False
                    st.session_state.start_form_time = None
                    st.rerun()

            # ✅ Logout Button on Form Page
            if st.button("Logout"):
                logout()

if __name__ == "__main__":
    app()
