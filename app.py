
from scraper import get_website_text
from embeddings import create_vector_store
import numpy as np
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
import streamlit as st

st.title("AI Website Chatbot ")

# Load local LLM once

@st.cache_resource
def load_llm():
    model_name = "google/flan-t5-base"

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    return tokenizer, model

tokenizer, model = load_llm()


def generate_answer(prompt):
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=200,
            temperature=0.3
        )

    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return answer.strip()

# Initialize session
if "index" not in st.session_state:
    st.session_state.index = None
    st.session_state.chunks = None
    st.session_state.model = None

# URL input
url = st.text_input("Enter website URL")

if st.button("Process Website"):
    if url:
        with st.spinner("Reading website..."):
            content = get_website_text(url)

        with st.spinner("Creating knowledge base..."):
            index, chunks, model = create_vector_store(content)

        st.session_state.index = index
        st.session_state.chunks = chunks
        st.session_state.model = model

        st.success("Website processed successfully!")
    else:
        st.warning("Please enter a URL.")

# Question input
question = st.text_input("Ask a question")

if st.button("Get Answer"):
    if st.session_state.index is not None and question:

        question_embedding = st.session_state.model.encode([question])
        question_embedding = np.array(question_embedding)

        D, I = st.session_state.index.search(question_embedding, k=3)

        retrieved_text = " ".join(
            [st.session_state.chunks[i] for i in I[0]]
        )
        
        prompt = f"""
Answer the question using only the information in the context.

Context:
{retrieved_text}

Question:
{question}

Answer:
"""

        with st.spinner("Generating answer..."):
            answer = generate_answer(prompt)

        st.write("### Answer:")
        st.write(answer)

    else:
        st.warning("Please process a website first.")