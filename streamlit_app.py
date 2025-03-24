import streamlit as st

st.title("Streamlit Button Example")
if st.button('Say Hello'):
    st.write("Hello, Streamlit!")
else:
    st.write("Click the button!")
