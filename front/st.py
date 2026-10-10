import time
import streamlit as st
from langchain.messages import HumanMessage, SystemMessage
from langchain_ollama import ChatOllama

# Page Configuration
st.set_page_config(page_title="LLM Playground", layout="wide")

# Sidebar: Model Parameters
with st.sidebar:
    st.header("Model Settings")
    
    temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.3, step=0.1)
    top_p = st.slider("Top P", min_value=0.0, max_value=1.0, value=0.9, step=0.1)
    top_k = st.slider("Top K", min_value=0, max_value=100, value=40, step=1)
    seed = st.number_input("Seed", value=42, step=1)

st.subheader("Enter text")
user_input = st.text_area(
    label="Text",
    placeholder="Insert text here...",
    height=200,
    label_visibility="collapsed"
)

submit_button = st.button("Submit")

if submit_button and user_input.strip():
    llm = ChatOllama(
        model="llama3.2",
        temperature=temperature,
        top_k=top_k,
        top_p=top_p,
        num_predict=1000,
        seed=seed
    )

    messages = [
        SystemMessage(content=''),
        HumanMessage(content=user_input)
    ]

    st.markdown("---")
    st.header("Result")

    response_placeholder = st.empty()
    full_response = ""
    finish_reason = "stop"
    
    start_time = time.time()
    
    try:
        # Standard streaming without un-supported keyword arguments
        for chunk in llm.stream(messages):
            full_response += chunk.content
            response_placeholder.markdown(full_response + "▌")
            
            # Check for native metadata if passed by Ollama's final chunk
            if hasattr(chunk, "response_metadata") and chunk.response_metadata:
                if "done_reason" in chunk.response_metadata:
                    finish_reason = chunk.response_metadata["done_reason"]
                    
        response_placeholder.markdown(full_response)
        elapsed_time = round(time.time() - start_time, 2)

        # Calculate accurate token counts using ChatOllama's tokenizer
        prompt_tokens = llm.get_num_tokens(user_input)
        completion_tokens = llm.get_num_tokens(full_response)
        total_tokens = prompt_tokens + completion_tokens

        # Display performance metrics
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.caption("Input tokens")
            st.subheader(prompt_tokens)
        with col2:
            st.caption("Output tokens")
            st.subheader(completion_tokens)
        with col3:
            st.caption("Total tokens")
            st.subheader(total_tokens)
        with col4:
            st.caption("Time")
            st.subheader(f"{elapsed_time} sec.")

        st.caption(f"Model: llama3.2:latest · Finish reason: {finish_reason}")

    except Exception as e:
        st.error(f"Ollama Error: {str(e)}")