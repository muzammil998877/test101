import streamlit as st

# Dictionary mapping names to a list of ages
name_age_dict = {
    "Muzammil": [29, 30, 31],
    "Krish": [40, 41, 42],
    "Ali": [25, 26, 27]
}

# Title of the app
st.title("User Information Form")

# Create a form to capture user's name and age
with st.form(key='user_form'):
    # First dropdown for Name
    name = st.selectbox("Select your name:", list(name_age_dict.keys()))
    
    # Second dropdown for Age (dependent on the selected name)
    age = st.selectbox("Select your age:", name_age_dict[name])

    # Submit button
    submit_button = st.form_submit_button(label='Submit')

# When the user submits the form
if submit_button:
    st.write(f"Hello {name}! You selected age {age}.")
