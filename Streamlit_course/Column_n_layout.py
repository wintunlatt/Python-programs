import streamlit as st

st.title("Two Column Layout")

col1, col2 = st.columns(2)

with col1:
    st.header("Column 1")
    st.write("This is the left column.")

with col2:
    st.header("Column 2")
    st.write("This is the right column.")
