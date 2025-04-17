import streamlit as st
from langchain_groq import ChatGroq

# Load the API key from .streamlit/secrets.toml
groq_api_key = st.secrets["GROQ_API_KEY"]

# Initialize LLM
llm = ChatGroq(groq_api_key=groq_api_key, model_name="llama-3.3-70b-versatile")

# Run the query
if __name__ == "__main__":
    response = llm.invoke(
        "Give me all the unique tags for LinkedIn posts. Give me all the current topic tags in the world."
    )
    st.write(response.content)
