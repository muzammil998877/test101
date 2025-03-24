import streamlit as st
import pandas as pd
import io

# Dictionary mapping names to a list of ages
name_age_dict = {
    "Muzammil": [29, 30, 31],
    "Krish": [40, 41, 42],
    "Ali": [25, 26, 27]
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
    # Set the default age based on the selected name
    default_age = name_age_dict[name][0]  # Set the first age as the default value
    age = st.selectbox("Select your age:", name_age_dict[name], index=name_age_dict[name].index(default_age))

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
