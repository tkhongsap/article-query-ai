"""
This script sets up a system for loading documents from a directory, processing them into nodes,
and then using OpenAI's GPT-4o model to provide summarization and context-based queries. 

The program performs the following steps:
1. Initializes the environment by loading environment variables and allowing nested asyncio loops.
2. Sets up the OpenAI API client.
3. Loads documents from a specified directory.
4. Processes the documents into nodes using a sentence splitter.
5. Configures models for summarization and embedding.
6. Creates summary and vector indexes from the nodes.
7. Sets up query engines for summarization and vector-based searches.
8. Allows for continuous querying by the user, with the option to exit the loop.

The program is designed to be run in a terminal, and it uses colorized output to indicate progress
through various stages of execution.

Dependencies:
- OpenAI API
- LlamaIndex for document processing and indexing
- dotenv for environment variable management
- colorama for colorized terminal output
"""

import os
import openai
import nest_asyncio
from dotenv import load_dotenv
from llama_index.core import SimpleDirectoryReader, SummaryIndex, VectorStoreIndex, Settings
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.core.tools import QueryEngineTool
from llama_index.core.query_engine.router_query_engine import RouterQueryEngine
from llama_index.core.selectors import LLMSingleSelector
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

def print_markdown(message):
    """Print a message with markdown-style formatting."""
    print(f"{Fore.CYAN}### {message}{Style.RESET_ALL}\n")

def print_step(message):
    """Print a step with emphasis."""
    print(f"{Fore.GREEN}{message}{Style.RESET_ALL}\n")

def initialize_environment():
    """Load environment variables and allow nested asyncio loops."""
    print_markdown("Initializing environment...")
    load_dotenv()
    nest_asyncio.apply()
    print_step("Environment initialized.")

def setup_openai_client():
    """Set up OpenAI API client."""
    print_markdown("Setting up OpenAI API client...")
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    print_step("OpenAI API client setup completed.")
    return client

def get_input_files(base_dir):
    """Get the list of files from the base directory."""
    print_markdown(f"Getting list of files from directory: {base_dir}...")
    input_files = [os.path.join(base_dir, f) for f in os.listdir(base_dir) if os.path.isfile(os.path.join(base_dir, f))]
    print_step(f"Found {len(input_files)} file(s).")
    return input_files

def load_documents(input_files):
    """Load documents from the specified files."""
    print_markdown("Loading documents from files...")
    try:
        documents = SimpleDirectoryReader(input_files=input_files).load_data()
        if documents:
            print_step(f"Successfully loaded {len(documents)} document(s).")
            print_markdown("First document content preview:")
            print(f"{documents[0]}\n" if len(documents) > 0 else "No documents found.\n")
        else:
            print_step("No documents were loaded.")
        return documents
    except Exception as e:
        print(f"{Fore.RED}An error occurred while loading documents: {e}{Style.RESET_ALL}\n")
        return []

def split_documents_into_nodes(documents):
    """Split the documents into nodes for further processing."""
    print_markdown("Splitting documents into nodes...")
    splitter = SentenceSplitter(chunk_size=1024)
    nodes = splitter.get_nodes_from_documents(documents)
    print_step(f"Document splitting completed. Generated {len(nodes)} node(s).")
    return nodes

def setup_models():
    """Set up models for summarization and embedding."""
    print_markdown("Setting up models for summarization and embedding...")
    Settings.llm = OpenAI(model="gpt-4o")
    Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-large")
    print_step("Model setup completed.")

def create_indexes(nodes):
    """Create summary and vector indexes from nodes."""
    print_markdown("Creating summary and vector indexes...")
    summary_index = SummaryIndex(nodes)
    vector_index = VectorStoreIndex(nodes)
    print_step("Indexes created successfully.")
    return summary_index, vector_index

def create_query_engines(summary_index, vector_index):
    """Create query engines for summarization and vector search."""
    print_markdown("Creating query engines...")
    summary_query_engine = summary_index.as_query_engine(response_mode="tree_summarize", use_async=True)
    vector_query_engine = vector_index.as_query_engine()
    print_step("Query engines created.")
    return summary_query_engine, vector_query_engine

def setup_query_tools(summary_query_engine, vector_query_engine):
    """Set up query tools with descriptions."""
    print_markdown("Setting up query tools...")
    summary_tool = QueryEngineTool.from_defaults(
        query_engine=summary_query_engine,
        description="Useful for summarization questions",
    )
    vector_tool = QueryEngineTool.from_defaults(
        query_engine=vector_query_engine,
        description="Useful for retrieving specific context",
    )
    print_step("Query tools set up.")
    return summary_tool, vector_tool

def setup_router_query_engine(summary_tool, vector_tool):
    """Set up the Router Query Engine with a selector and query tools."""
    print_markdown("Setting up Router Query Engine...")
    query_engine = RouterQueryEngine(
        selector=LLMSingleSelector.from_defaults(),
        query_engine_tools=[summary_tool, vector_tool],
        verbose=True
    )
    print_step("Router Query Engine setup completed.")
    return query_engine

def main():
    """Main function to orchestrate the processing and query engine."""
    # Initialize environment and setup
    initialize_environment()
    client = setup_openai_client()
    
    # Define the base directory for documents
    base_dir = os.path.join(os.getcwd(), 'docs')
    
    # Load and process documents
    input_files = get_input_files(base_dir)
    print(f"Files to be loaded: {input_files}\n")
    
    documents = load_documents(input_files)
    if not documents:
        print_step("No documents to process. Exiting...")
        return  # Exit if no documents were loaded
    
    nodes = split_documents_into_nodes(documents)
    
    # Set up models and indexes
    setup_models()
    summary_index, vector_index = create_indexes(nodes)
    
    # Set up query engines and tools
    summary_query_engine, vector_query_engine = create_query_engines(summary_index, vector_index)
    summary_tool, vector_tool = setup_query_tools(summary_query_engine, vector_query_engine)
    
    query_engine = setup_router_query_engine(summary_tool, vector_tool)
    
    # Continuous loop to get user input and query the engine
    while True:
        user_input = input("Enter your query (or type 'exit' to quit): ")
        
        if user_input.lower() == 'exit':
            break
        
        # Perform the query
        print_markdown("Processing query...")
        response = query_engine.query(user_input)
        
        # Print the response in markdown format
        print(f"### Response:\n{str(response)}\n")

# Run the main function
if __name__ == "__main__":
    main()