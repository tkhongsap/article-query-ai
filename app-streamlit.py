import streamlit as st
import os
import openai
import nest_asyncio
import warnings
from openai import OpenAI

from dotenv import load_dotenv
from pprint import pprint
from pathlib import Path
from utils.get_doc_tools import get_doc_tools
from utils.custom_css_banner import get_social_news_banner
from llama_index.llms.openai import OpenAI as LlamaOpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import VectorStoreIndex
from llama_index.core.objects import ObjectIndex
from llama_index.core.agent import FunctionCallingAgentWorker, AgentRunner

# Set page config
st.set_page_config(page_title="💬 Intelligence Social News Analytics", page_icon="📺", layout="wide")

# Apply custom CSS
@st.cache_data
def load_social_news_banner():
    return get_social_news_banner()

st.markdown(load_social_news_banner(), unsafe_allow_html=True)

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

@st.cache_resource
def load_and_process_documents():
    docs_directory = Path("docs")
    articles = [file for file in docs_directory.iterdir() if file.is_file() and file.suffix == '.txt']
    articles.sort()

    paper_to_tools_dict = {}
    for article in articles:
        vector_query_tool, summary_tool = get_doc_tools(str(article), article.stem)
        paper_to_tools_dict[article] = [vector_query_tool, summary_tool]

    llm = LlamaOpenAI(model="gpt-4o", api_key=openai_api_key)
    embed_model = OpenAIEmbedding(model="text-embedding-3-large", api_key=openai_api_key)

    all_tools = [tool for tools in paper_to_tools_dict.values() for tool in tools]
    obj_index = ObjectIndex.from_objects(all_tools, index_cls=VectorStoreIndex)
    obj_retriever = obj_index.as_retriever(similarity_top_k=7)

    agent_worker = FunctionCallingAgentWorker.from_tools(
        tool_retriever=obj_retriever,
        llm=llm,
        system_prompt="""You are an AI journalist specializing in generating concise, accurate, and objective news reports. 
        Your primary task is to answer user queries by summarizing and analyzing information from the provided news articles or documents.

        Follow these guidelines:
        1. Utilize the tools provided to extract information directly from the given sources.
        2. Prioritize clarity, accuracy, and brevity in your responses, adhering to journalistic standards.
        3. Summarize key points and highlight relevant facts without introducing personal opinions or external information.
        4. Ensure your language and tone remain professional, unbiased, and appropriate for news reporting.
        5. Respond in the same language as the user's query and format your summaries to be easily understood by a broad audience.

        Remember, your goal is to inform users efficiently and accurately based on the provided materials.""",
        verbose=False
    )

    return AgentRunner(agent_worker)

# Load the agent
agent = load_and_process_documents()
st.sidebar.success("Agent loaded successfully.")

# Streamlit app layout
st.title("AI Journalist Query System")

# Display some information about the loaded documents
# st.sidebar.header("Document Information")
# docs_directory = Path("docs")
# num_docs = len([f for f in docs_directory.iterdir() if f.is_file() and f.suffix == '.txt'])
# st.sidebar.write(f"Number of loaded documents: {num_docs}")

# Chat input and response
user_query = st.chat_input("Ask a question about the articles")

if user_query:
    with st.spinner("Generating response..."):
        try:
            response = agent.query(user_query)
            
            # Display the main response text
            st.write("Agent response:", response.response)
            
            # Optionally, display the sources if available
            # if response.source_nodes:
            #     st.write("Source Nodes:", response.source_nodes)
            
            # Optionally, display formatted sources
            # formatted_sources = response.get_formatted_sources()
            # if formatted_sources:
            #     st.write("Formatted Sources:", formatted_sources)
                
        except Exception as e:
            st.error(f"An error occurred while processing your query: {str(e)}")
            st.exception(e)  # This will display the full traceback for debugging


# Footer
st.markdown("---")
st.markdown("AI Journalist Query System powered by OpenAI and LlamaIndex")