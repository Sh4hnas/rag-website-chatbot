import streamlit as st

st.title("AI WEBSITE CHATBOT")
st.write("Ask questions from any website")

url = st.text_input("Enter website URL: ")

question = st.text_input("Ask a question: ")

if st.button("Submit"):
    st.write("Processing...")
