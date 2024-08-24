import os
import openai
import nest_asyncio
import warnings

from dotenv import load_dotenv
from pprint import pprint
from pathlib import Path
from utils.get_doc_tools import get_doc_tools
from llama_index.llms.openai import OpenAI as LlamaOpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import VectorStoreIndex
from llama_index.core.objects import ObjectIndex
from llama_index.core.agent import FunctionCallingAgentWorker, AgentRunner

# Ignore all deprecation warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Load environment variables from .env file
load_dotenv()

# Allow for nested asyncio event loops
nest_asyncio.apply()

# Initialize OpenAI API client with API key from environment variables
openai_client = LlamaOpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Define the directory containing the articles
docs_directory = Path(r"D:\github-repo-tkhongsap\editor-in-chief\docs")

# Collect all .txt files in the directory
articles = [file for file in docs_directory.iterdir() if file.is_file() and file.suffix == '.txt']

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
llm = LlamaOpenAI(model="gpt-4o")
embed_model = OpenAIEmbedding(model="text-embedding-3-large")

# Collect all tools generated for the articles
all_tools = [tool for tools in paper_to_tools_dict.values() for tool in tools]

# Create an object index using the collected tools and VectorStoreIndex for retrieval
obj_index = ObjectIndex.from_objects(all_tools, index_cls=VectorStoreIndex)

# Create a retriever with the top 7 similar tools based on the query
obj_retriever = obj_index.as_retriever(similarity_top_k=7)

# Initialize the agent worker and runner with the retriever and LLM
agent_worker = FunctionCallingAgentWorker.from_tools(
    tool_retriever=obj_retriever,
    llm=llm, 
    system_prompt=""" \
You are an AI journalist specializing in generating concise, accurate, and objective news reports. 
Your primary task is to answer user queries by summarizing and analyzing information from the provided news articles or documents.

Follow these guidelines:
1. Utilize the tools provided to extract information directly from the given sources.
2. Prioritize clarity, accuracy, and brevity in your responses, adhering to journalistic standards.
3. Summarize key points and highlight relevant facts without introducing personal opinions or external information.
4. Ensure your language and tone remain professional, unbiased, and appropriate for news reporting.
5. Respond in the same language as the user's query and format your summaries to be easily understood by a broad audience.

Remember, your goal is to inform users efficiently and accurately based on the provided materials.

""",
    verbose=False
)

# Initialize the agent runner
agent = AgentRunner(agent_worker)

# Define ANSI color codes for styling
BOLD_BLACK = "\033[1;30m"  # Bold black color for user input
DARK_BLUE = "\033[34m"     # Dark blue color for agent response
RESET = "\033[0m"          # Reset color to default

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
        
        # Print the user input in bold black (simulated markdown) and the response in dark blue
        print(f"{BOLD_BLACK}\n **User Input:** {user_input}{RESET}")
        print(f"{DARK_BLUE}\n **Agent response:** {response}{RESET}")

# Start the query loopc
interactive_query_loop()
