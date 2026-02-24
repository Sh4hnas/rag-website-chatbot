# RAG Website Chatbot

## Overview
This project is an AI-powered chatbot that can read any website and answer questions based on its content using Retrieval-Augmented Generation (RAG).

## Features
- Extracts text from any website URL
- Converts website content into embeddings
- Stores embeddings using FAISS
- Prepares data for AI-based question answering

## Tech Stack
- Python
- Streamlit
- LangChain
- OpenAI API
- FAISS
- BeautifulSoup

## How to Run

1. Install dependencies:
   pip install -r requirements.txt

2. Set OpenAI API key:
   setx OPENAI_API_KEY "your_api_key"

3. Run app:
   streamlit run app.py

## Project Status
Currently implementing core RAG pipeline.
