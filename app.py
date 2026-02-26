from scraper import get_website_text, NetworkError, ContentExtractionError
from embeddings import create_vector_store, ChunkingError, VectorStoreError, EmbeddingError
import numpy as np
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
import streamlit as st

# Page configuration
st.set_page_config(
    page_title="RAG Website Chatbot",
    page_icon="🤖",
    layout="wide"
)

# Load LLM model
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
        outputs = model.generate(**inputs, max_new_tokens=200, temperature=0.3)
    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return answer.strip()

# Initialize session state
if "index" not in st.session_state:
    st.session_state.index = None
    st.session_state.chunks = None
    st.session_state.model = None

if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar
with st.sidebar:
    st.header("Website Processing")
    
    url = st.text_input("Enter website URL", placeholder="https://example.com")
    
    if st.button("Process Website"):
        if url:
            try:
                with st.spinner("Reading website..."):
                    content = get_website_text(url)
                
                with st.spinner("Creating embeddings..."):
                    index, chunks, embedding_model = create_vector_store(content)
                
                st.session_state.index = index
                st.session_state.chunks = chunks
                st.session_state.model = embedding_model
                
                st.success(f"✅ Processed! {len(chunks)} chunks created.")
                
            except (NetworkError, ContentExtractionError, ChunkingError, VectorStoreError, EmbeddingError) as e:
                st.error(f"❌ Error: {str(e)}")
            except Exception as e:
                st.error(f"❌ Unexpected error: {str(e)}")
        else:
            st.warning("⚠️ Please enter a URL.")
    
    # Show info if processed
    if st.session_state.chunks is not None:
        st.divider()
        st.info(f"📊 Chunks: {len(st.session_state.chunks)}")
    
    # Clear chat button
    if len(st.session_state.messages) > 0:
        st.divider()
        if st.button("Clear Chat"):
            st.session_state.messages = []
            st.rerun()

# Main content
st.title("💬 Chat with Website")

# Display chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Chat input
if st.session_state.index is not None:
    if question := st.chat_input("Ask a question about the website"):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": question})
        
        # Display user message
        with st.chat_message("user"):
            st.write(question)
        
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    # Search for relevant chunks
                    question_embedding = st.session_state.model.encode([question])
                    question_embedding = np.array(question_embedding)
                    D, I = st.session_state.index.search(question_embedding, k=3)
                    
                    # Check relevance - if distance is too high, the question is likely off-topic
                    # Lower distance = more relevant. Typical good matches are < 1.0
                    min_distance = D[0][0]
                    
                    if min_distance > 1.5:
                        # Question is likely not related to the website content
                        answer = "I couldn't find relevant information in the website to answer your question. This question might be outside the scope of the processed website content. Please ask questions related to the website's content."
                        st.warning(answer)
                        st.session_state.messages.append({"role": "assistant", "content": answer})
                    else:
                        # Generate answer from relevant content
                        retrieved_text = " ".join([st.session_state.chunks[i] for i in I[0]])
                        prompt = f"""Answer the question using only the information in the context. If the context doesn't contain enough information to answer the question, say "I don't have enough information to answer this question based on the website content."

Context:
{retrieved_text}

Question:
{question}

Answer:"""
                        
                        answer = generate_answer(prompt)
                        st.write(answer)
                        
                        # Show sources
                        with st.expander("📚 View Sources"):
                            for idx, source_idx in enumerate(I[0]):
                                st.text_area(
                                    f"Source {idx + 1}",
                                    st.session_state.chunks[source_idx],
                                    height=100,
                                    disabled=True
                                )
                        
                        # Add assistant message
                        st.session_state.messages.append({"role": "assistant", "content": answer})
                    
                except Exception as e:
                    error_msg = f"Error generating answer: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
else:
    st.info("👈 Please process a website first using the sidebar.")
