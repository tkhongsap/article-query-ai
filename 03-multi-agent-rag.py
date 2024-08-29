import os
import warnings
import openai

from dotenv import load_dotenv
from pathlib import Path
from pprint import pprint

from utils.rag_tools import get_doc_tools  # Updated import path
from utils.role_description_prompts import JOURNALIST_ROLE_PROMPT  # Updated import path
from llama_index.llms.openai import OpenAI as LlamaOpenAI
from llama_index.llms.anthropic import Anthropic

from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import VectorStoreIndex
from llama_index.core.objects import ObjectIndex
from llama_index.core.agent import FunctionCallingAgentWorker, AgentRunner

# Ignore all deprecation warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI API client with API key from environment variables
openai_api_key = os.getenv('OPENAI_API_KEY')
anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')

# Initialize OpenAI API client with API key from environment variables
openai_client = LlamaOpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Define the directory containing the articles relative to the script location
docs_directory = Path(__file__).parent / 'docs'

# Collect all markdown (.md) files in the directory
articles = [file for file in docs_directory.iterdir() if file.is_file() and file.suffix == '.md']

# Sort the articles list to ensure the dates are in order (optional)
articles.sort()

# Print the sorted list of articles
pprint([article.name for article in articles])

# Dictionary to map each article to its tools
paper_to_tools_dict = {}

# Iterate over articles and generate tools for each article
for article in articles:
    print(f"Processing tools for article: {article.name}")
    
    # Get document tools (e.g., vector query tool, summary tool) for the article
    vector_query_tool, summary_tool = get_doc_tools(str(article), article.stem)
    
    # Store the tools in the dictionary
    paper_to_tools_dict[article] = [vector_query_tool, summary_tool]

# Initialize LLM and embedding model for querying and indexing
llm = LlamaOpenAI(temperature=0.2, model="gpt-4o", api_key=openai_api_key, max_tokens=3000)

# # Initialize LLM and embedding model for querying and indexing
# llm = Anthropic(api_key=anthropic_api_key, model="claude-3-5-sonnet-20240620", temperature=0.2, max_tokens=2000)

# set an embedding model for the ObjectIndex
embed_model = OpenAIEmbedding(model="text-embedding-3-large")

# Collect all tools generated for the articles
all_tools = [tool for tools in paper_to_tools_dict.values() for tool in tools]
print(f"Total number of tools collected: {len(all_tools)}")

# Create an object index using the collected tools and VectorStoreIndex for retrieval
obj_index = ObjectIndex.from_objects(all_tools, index_cls=VectorStoreIndex)

# Create a retriever with the top k similar tools based on the query
obj_retriever = obj_index.as_retriever(similarity_top_k=7, embedding_model=embed_model)

# Initialize the agent worker and runner with the retriever and LLM
agent_worker = FunctionCallingAgentWorker.from_tools(
    tool_retriever=obj_retriever,
    llm=llm, 
    system_prompt= JOURNALIST_ROLE_PROMPT,
    verbose=False
)

# Initialize the agent runner
agent = AgentRunner(agent_worker)

# Define ANSI color codes for styling
BOLD_RED = "\033[1;31m"  # Bold red color for user input
DARK_BLUE = "\033[34m"   # Dark blue color for agent response
RESET = "\033[0m"        # Reset color to default

# Start the interactive query loop
def interactive_query_loop():
    while True:
        # Get the user query
        user_input = input("Ask a question (or type 'exit' to quit): ")
        
        # Break the loop if the user wants to exit
        if user_input.lower() == "exit":
            print("Exiting the query loop.")
            break
        
        # Get the agent's response based on the user query
        response = agent.query(user_input)
        
        # Print the user input in bold red and the response in dark blue, separated by a break line
        print("\n=======\n")
        print(f"{BOLD_RED}\n **User Input:** {user_input}{RESET}")
        print("\n=======\n")
        print(f"{DARK_BLUE}\n **Agent response:** {response}{RESET}")
        print("\n=======\n")

# Start the query loop
interactive_query_loop()
