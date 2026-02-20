import streamlit as st

st.title("AI WEBSITE CHATBOT")
st.write("Ask questions from any website")

url = st.text_input("Enter website URL: ")
import streamlit as st
from scraper import get_website_text

st.title("🌐 AI Website Chatbot")
st.write("Ask questions from any website")

url = st.text_input("Enter website URL")

if st.button("Extract Website Content"):
    if url:
        with st.spinner("Reading website..."):
            content = get_website_text(url)
            st.write(content[:2000])   # show first part only
    else:
        st.warning("Please enter URL")

question = st.text_input("Ask a question: ")

if st.button("Submit"):
    st.write("Processing...")
