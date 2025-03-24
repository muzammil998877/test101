import streamlit as st

# Dictionary for name and age mapping
name_age_dict = {
    "Muzammil": 29,
    "Krish": 40
}

# Title of the app
st.title("User Information Form")

# Create a form to capture user's name
with st.form(key='user_form'):
    name = st.text_input("Enter your name:")
    submit_button = st.form_submit_button(label='Submit')

# When the user submits the form
if submit_button:
    # Check if the name exists in the dictionary
    if name in name_age_dict:
        age = name_age_dict[name]
        st.write(f"Hello {name}! Your age is {age}.")
    else:
        st.write("Sorry, we don't have information for this name.")
