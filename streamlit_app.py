Sure! To add a **logout button** on the second page, you can simply add a button at the top-right of the page and, when clicked, reset the session state (i.e., logging the user out).

Here’s how to integrate the **logout functionality**:

1. **Add a logout button** in the form page.
2. **On clicking the logout button**, clear the session state related to the login and redirect to the login page.

### Here's the updated code with the logout button:

```python
import streamlit as st
import pandas as pd

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

# Function to logout the user
def logout():
    # Clear session state
    st.session_state.logged_in = False
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
        # Display logout button on top-right
        logout_button = st.button("Logout", key="logout_button", help="Click to logout")
        
        if logout_button:
            logout()
            st.experimental_rerun()  # Refresh the page to go back to login
        
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
```

### Explanation of Changes:
1. **Logout Button**:
   - The `logout()` function clears the session state (`st.session_state.logged_in` and `st.session_state.username`).
   - The `st.button("Logout")` button is placed at the top right, and when clicked, it triggers the logout process and refreshes the page.

2. **Logout Process**:
   - When the user clicks on the **Logout** button, the session is cleared using `st.session_state.logged_in = False` and `st.session_state.username = ""`.
   - `st.experimental_rerun()` is used to refresh the page, effectively taking the user back to the login page.

3. **Form Page**:
   - The form page remains the same. The user can fill out the form, and once submitted, the form data is saved in the session state.
   - The CSV download is also available as before.

### User Flow:
1. The user enters the **Login Page**, inputs their username, and clicks **Login**.
2. After logging in, the user sees the **Form Page** where they can fill out the form.
3. If the user wishes to log out, they click the **Logout** button in the top-right corner. This will log them out and return to the login page.

### Next Steps:
- You can enhance this by adding more complex authentication mechanisms (such as password validation).
- The **logout button** provides a smooth way to exit the application and ensure that the session data is cleared.
