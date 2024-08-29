import streamlit as st
import os
import openai
import nest_asyncio
import warnings
from openai import OpenAI
from datetime import datetime, timedelta
from dotenv import load_dotenv
from pprint import pprint
from pathlib import Path
from utils.rag_tools import get_doc_tools

from utils.custom_css_main_page import get_main_custom_css
from utils.custom_css_banner import get_social_news_banner
from utils.role_description_prompts import JOURNALIST_ROLE_PROMPT  # Updated import path

from llama_index.llms.openai import OpenAI as LlamaOpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import VectorStoreIndex
from llama_index.core.objects import ObjectIndex
from llama_index.core.agent import FunctionCallingAgentWorker, AgentRunner

# Ignore all deprecation warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Set page config
st.set_page_config(page_title="💬 Intelligence Social News Analytics", page_icon="📺", layout="wide")

# Apply custom CSS
@st.cache_data
def load_social_news_banner():
    return get_social_news_banner()

st.markdown(load_social_news_banner(), unsafe_allow_html=True)

# Apply custom CSS
@st.cache_data
def load_main_custom_css():
    return get_main_custom_css()

st.markdown(load_main_custom_css(), unsafe_allow_html=True)


# Function to get the OpenAI API key from Streamlit secrets
def get_openai_api_key():
    if "OPENAI_API_KEY" not in st.secrets:
        st.error("OpenAI API key not found in Streamlit secrets.")
        st.stop()
    return st.secrets["OPENAI_API_KEY"]

# Initialize OpenAI API client with API key from Streamlit secrets
openai_api_key = get_openai_api_key()
openai_client = LlamaOpenAI(api_key=openai_api_key)
st.sidebar.success("OpenAI client initialized successfully.")

def display_sidebar_info():
    st.sidebar.markdown("---")
    st.sidebar.markdown(
        """
        <div style="background-color: #f0f2f6; padding: 10px; border-radius: 5px; border-left: 5px solid #4b9ff2;">
            <h4 style="color: #4b9ff2; margin-top: 0;">📅 Data Coverage</h4>
            <p style="margin-bottom: 0;">This news analytics system contains data from the <strong>last 7 days</strong>. Stay up-to-date with the most recent events and trends!</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
# Display sidebar info
display_sidebar_info()
    
@st.cache_resource
def load_and_process_documents():
    docs_directory = Path("docs")
    articles = [file for file in docs_directory.iterdir() if file.is_file() and file.suffix == '.txt']
    articles.sort()

    paper_to_tools_dict = {}
    for article in articles:
        vector_query_tool, summary_tool = get_doc_tools(str(article), article.stem)
        paper_to_tools_dict[article] = [vector_query_tool, summary_tool]

    llm = LlamaOpenAI(model="gpt-4o", api_key=openai_api_key, max_tokens=3000)
    embed_model = OpenAIEmbedding(model="text-embedding-3-large", api_key=openai_api_key)

    all_tools = [tool for tools in paper_to_tools_dict.values() for tool in tools]
    obj_index = ObjectIndex.from_objects(all_tools, index_cls=VectorStoreIndex)
    obj_retriever = obj_index.as_retriever(similarity_top_k=7)

    agent_worker = FunctionCallingAgentWorker.from_tools(
        tool_retriever=obj_retriever,
        llm=llm,
        system_prompt=JOURNALIST_ROLE_PROMPT,
        verbose=False
    )

    return AgentRunner(agent_worker)

# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Function to display chat messages
def display_chat_messages():
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar="🧑‍💻" if message["role"] == "user" else "🤖"):
            st.markdown(message["content"])

# Load the agent
agent = load_and_process_documents()
st.sidebar.success("Agent loaded successfully.")

# Display chat messages
display_chat_messages()

# Chat input and response
user_query = st.chat_input("Ask a question about the articles")

if user_query:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_query})
    
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(user_query)
    
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Generating response..."):
            try:
                response = agent.query(user_query)
                
                # Display the main response text
                st.markdown(response.response)
                
                # Add assistant message to chat history
                st.session_state.messages.append({"role": "assistant", "content": response.response})
                    
            except Exception as e:
                st.error(f"An error occurred while processing your query: {str(e)}")
                st.exception(e)  # This will display the full traceback for debugging
