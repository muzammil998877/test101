import streamlit as st
import pandas as pd
import pickle
import os
from datetime import datetime

USER_DATA_FILE = 'user_data.pkl'
FORM_DATA_FILE = 'form_data.pkl'

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'form_data' not in st.session_state:
    st.session_state.form_data = []
if 'form_started' not in st.session_state:
    st.session_state.form_started = False

def load_user_data():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'rb') as f:
            return pickle.load(f)
    else:
        return {"admin": "admin123"}

def save_user_data(user_data):
    with open(USER_DATA_FILE, 'wb') as f:
        pickle.dump(user_data, f)

def load_form_data():
    if os.path.exists(FORM_DATA_FILE):
        with open(FORM_DATA_FILE, 'rb') as f:
            return pickle.load(f)
    else:
        return []

def save_form_data(form_data):
    with open(FORM_DATA_FILE, 'wb') as f:
        pickle.dump(form_data, f)

def login(username, password):
    user_data = load_user_data()
    if username in user_data and user_data[username] == password:
        st.session_state.logged_in = True
        st.session_state.username = username
        return True
    return False

def create_user(username, password):
    user_data = load_user_data()
    if username in user_data:
        st.error(f"User {username} already exists!")
    else:
        user_data[username] = password
        save_user_data(user_data)
        st.success(f"User {username} created successfully!")

data = {
    'Exception Management': {
        'HHDC': ['A Flag - No', 'A Flag - Yes'],
        'NHHDC': ['Received D0002s - Daily: NHH Faults']
    },
    'Metering': {
        'Meter Serv BW': ['Aborts - SMETS Install', 'D0002: HH']
    }
}

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

        st.subheader("View Form Submissions")
        form_data = load_form_data()
        if form_data:
            df = pd.DataFrame(form_data)
            st.dataframe(df)

            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Form Submissions as CSV",
                data=csv,
                file_name="form_submissions.csv",
                mime="text/csv"
            )
        else:
            st.info("No form submissions available.")

    elif not st.session_state.logged_in:
        st.title("Login Page")
        username = st.text_input("Enter your Username:")
        password = st.text_input("Enter your Password", type="password")

        if st.button("Login"):
            if login(username, password):
                st.success(f"Welcome, {username}!")
                st.rerun()  # ✅ Ensures page refresh to show landing page
            else:
                st.error("Invalid username or password.")

    else:
        # ✅ Shows "Start Form" first after login instead of going directly to the form
        st.title("Welcome")
        st.write(f"Hello, {st.session_state.username}! Click below to start the form.")

        # ✅ Fixed Logout Button (No double click issue)
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.rerun()  # ✅ Refreshes the app immediately

        if not st.session_state.form_started:
            if st.button("Start Form"):
                st.session_state.form_started = True
                st.rerun()

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
                        "Submission Time": submission_time
                    }

                    st.session_state.form_data.append(form_entry)
                    save_form_data(st.session_state.form_data)

                    st.success("Form submitted successfully!")

                    df = pd.DataFrame(st.session_state.form_data)
                    csv = df.to_csv(index=False)

                    st.download_button(
                        label="Download CSV",
                        data=csv,
                        file_name="form_data_with_submission_time.csv",
                        mime="text/csv"
                    )

                    st.session_state.form_started = False
                    st.rerun()

if __name__ == "__main__":
    app()
