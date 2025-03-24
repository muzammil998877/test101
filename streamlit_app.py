import streamlit as st
import pandas as pd
import getpass

# Function to simulate login and capture the username
def login(username):
    # For simplicity, we're not checking passwords; just capturing the username.
    # You could add password validation if needed.
    st.session_state.logged_in = True
    st.session_state.username = username

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

# Initialize session state variables
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""

# Streamlit app
def app():
    # If the user is not logged in, show the login form
    if not st.session_state.logged_in:
        st.title("Login Page")
        username = st.text_input("Enter your Username:")
        
        if st.button("Login"):
            if username:
                login(username)
                st.success(f"Welcome, {username}!")
            else:
                st.error("Please enter a valid username.")
    
    # After login, show the form page
    else:
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
                # Collect form data along with username
                form_entry = {
                    "Cohort": cohort,
                    "LOB": lob,
                    "Sub-LOB": sub_lob,
                    "MPAN": mpan,
                    "Account": account,
                    "Status": status,
                    "Username": st.session_state.username
                }

                # Store the form entry
                if 'form_data' not in st.session_state:
                    st.session_state.form_data = []
                st.session_state.form_data.append(form_entry)

                # Reset the form after submission
                st.session_state.cohort = ""
                st.session_state.lob = ""
                st.session_state.sub_lob = ""
                st.session_state.mpan = ""
                st.session_state.account = ""
                st.session_state.status = ""

                st.success("Form submitted successfully!")

                # Offer to download CSV
                if len(st.session_state.form_data) > 0:
                    df = pd.DataFrame(st.session_state.form_data)
                    csv = df.to_csv(index=False)

                    # Create a download link for the CSV
                    st.download_button(
                        label="Download CSV",
                        data=csv,
                        file_name="form_data_with_username.csv",
                        mime="text/csv"
                    )

if __name__ == "__main__":
    app()
