import pandas as pd
import io

# Dictionary mapping names to ages
name_age_dict = {
    "Muzammil": 29,
    "Krish": 40,
    "Ali": 25
}

# Initialize form_data in session state if it doesn't exist
if "form_data" not in st.session_state:
    st.session_state.form_data = []

# Title of the app
st.title("User Information Form")

# Create a form to capture user's name and age
with st.form(key='user_form'):
    # First dropdown for Name
    name = st.selectbox("Select your name:", list(name_age_dict.keys()))
    
    # Second dropdown for Age (dependent on the selected name)
    # Only show the corresponding age for the selected name
    age = name_age_dict[name]  # Get the age directly based on the selected name

    # Display the age (as it's fixed based on the name)
    st.write(f"Your age is: {age}")

    # Submit button
    submit_button = st.form_submit_button(label='Submit')

    # When the user submits the form
    if submit_button:
        # Store the form data in session state
        st.session_state.form_data.append({"Name": name, "Age": age})
        
        # Display the selected information
        st.write(f"Hello {name}! You selected age {age}.")

# Export button to download form data as CSV
if st.button("Export Data to CSV"):
    if st.session_state.form_data:
        # Convert the list of form submissions into a DataFrame
        df = pd.DataFrame(st.session_state.form_data)

        # Convert DataFrame to CSV
        csv = df.to_csv(index=False)

        # Convert CSV to bytes so it can be downloaded
        buffer = io.StringIO(csv)
        st.download_button(
            label="Download CSV",
            data=buffer,
            file_name="user_data.csv",
            mime="text/csv",
        )
    else:
        st.write("No data to export.")                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
