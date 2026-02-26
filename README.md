# RAG Website Chatbot

### Context-Aware Web Intelligence Assistant

An AI-powered Retrieval-Augmented Generation (RAG) system that dynamically processes website content and enables intelligent, context-grounded question answering.


## Problem Statement

Websites contain large amounts of information, but users often struggle to quickly extract precise answers from lengthy content. Traditional chatbots generate responses without grounding them in actual website data, leading to hallucinations.

This project solves that problem by building a **context-aware AI assistant** that answers questions strictly based on the processed website content.



## Solution Overview

This system uses **Retrieval-Augmented Generation (RAG)** to:

1. Scrape website content dynamically
2. Split content into semantic chunks
3. Convert chunks into vector embeddings
4. Store embeddings in a FAISS vector database
5. Retrieve the most relevant chunks for a user query
6. Generate grounded answers using an instruction-tuned LLM (FLAN-T5)

The model only answers using retrieved context, reducing hallucinations and increasing reliability.


## Architecture
User Question
↓
SentenceTransformer Embedding
↓
FAISS Vector Search (Top-3 Retrieval)
↓
Context Aggregation
↓
FLAN-T5 (Instruction-Tuned Model)
↓
Grounded Answer + Source Display



## Key Features

- Semantic search using FAISS
- Instruction-tuned LLM (FLAN-T5-base)
- Source transparency (view retrieved chunks)
- Relevance validation (prevents off-topic answers)
- Chat-style interface using Streamlit
- Robust error handling for scraping & embedding
- Fully local inference (no external API required)



## Tech Stack

- **Python**
- **Streamlit** – UI
- **SentenceTransformers (all-MiniLM-L6-v2)** – Embeddings
- **FAISS** – Vector similarity search
- **Transformers (FLAN-T5-base)** – Language model
- **NumPy**
- **BeautifulSoup (Scraper module)**



## Installation

### Clone the repository
git clone <your-repo-url>
cd <repo-folder>


### Run the application
streamlit run app.py

### How to Use

1.Enter a website URL in the sidebar

2.Click Process Website

3.Ask questions in the chat interface

4.View retrieved source chunks for transparency

### Future Improvements

- Multi-website comparison

- Streaming token generation

- Improved chunk overlap strategy

- Deployment on cloud platform

- PDF and document support