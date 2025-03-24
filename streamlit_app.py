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
if 'form_completed' not in st.session_state:
    st.session_state.form_completed = False

# Function to load user data
def load_user_data():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'rb') as f:
            return pickle.load(f)
    return {"admin": "admin123"}

# Function to save user data
def save_user_data(user_data):
    with open(USER_DATA_FILE, 'wb') as f:
        pickle.dump(user_data, f)

# Function to log in
def login(username, password):
    user_data = load_user_data()
    if username in user_data and user_data[username] == password:
        st.session_state.logged_in = True
        st.session_state.username = username
        return True
    return False

# Function to log out
def logout():
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.form_started = False
    st.session_state.start_form_time = None
    st.session_state.form_completed = False
    st.rerun()

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
        
        # ✅ View Submission Forms Data
        st.subheader("View Submission Forms Data")
        form_data = load_form_data()

        if form_data:
            df = pd.DataFrame(form_data)
            st.write(df)

            # ✅ Download CSV button
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="submission_data.csv",
                mime="text/csv",
            )
        else:
            st.info("No form data available.")

        # ✅ Logout button
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

        if not st.session_state.form_started:
            if st.button("Start Form"):
                st.session_state.form_started = True
                st.session_state.start_form_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                st.rerun()

        elif not st.session_state.form_completed:
            st.subheader("Form Section")

            question1 = st.text_input("Enter your response to Question 1:")
            question2 = st.text_input("Enter your response to Question 2:")

            if st.button("Submit Form"):
                form_entry = {
                    "Username": st.session_state.username,
                    "Start Time": st.session_state.start_form_time,
                    "End Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Question 1": question1,
                    "Question 2": question2,
                }

                form_data = load_form_data()
                form_data.append(form_entry)
                save_form_data(form_data)

                st.session_state.form_completed = True
                st.success("Form submitted successfully!")
                st.rerun()

        else:
            st.write("✅ You have already completed the form. Thank you!")

        # ✅ Logout button on Start Form Page
        if st.button("Logout", key="logout_start_page"):
            logout()

# Run the app
if __name__ == "__main__":
    app()
