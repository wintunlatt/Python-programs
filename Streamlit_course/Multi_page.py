import streamlit as st

st.title("Main Dashboard")

tab1, tab2, tab3 = st.tabs(["Home", "Analytics", "Settings"])

with tab1:
    st.header("Welcome to Home")
    st.write("This is the home tab.")

with tab2:
    st.header("Analytics View")
    st.write("Put your charts and data insights here.")

with tab3:
    st.header("Settings")
    st.write("User preferences or configurations go here.")
