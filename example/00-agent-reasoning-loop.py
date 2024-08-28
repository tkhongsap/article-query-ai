"""
Script: LlamaIndex-based Document Analysis with OpenAI Embeddings

Description:
This script is designed to perform document analysis on selected PDFs using the LlamaIndex framework. 
It allows users to choose a PDF from the 'docs' folder, query the document using a pre-configured 
embedding model from OpenAI, and receive a summarized response. The script currently operates 
in high-level mode only, providing straightforward query execution.

Features:
1. **Document Selection**: Users can select a PDF from the 'docs' folder for analysis.
2. **Query Execution**: Users can input queries, and the agent will provide summarized responses.
3. **Embedding Model**: The script uses the "text-embedding-ada-002" model to convert text into embeddings.

Usage:
1. Ensure the 'docs' folder contains the PDF files you wish to analyze.
2. Run the script, select the desired PDF, and enter your queries.
3. The script will return summarized responses based on your input.

Note:
The debugging functionality has been commented out but can be re-enabled if needed.
"""

import os
from dotenv import load_dotenv
import nest_asyncio
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.agent import FunctionCallingAgentWorker, AgentRunner
from utils.get_doc_tools import get_doc_tools

# ANSI escape codes for colors
BOLD_BLACK = "\033[1;30m"
BOLD_RED = "\033[1;31m"
BOLD_BLUE = "\033[1;34m"
RESET = "\033[0m"

# Load environment variables
load_dotenv()

# Initialize OpenAI API client with API key from environment variables
openai_api_key = os.getenv('OPENAI_API_KEY')
embed_model = OpenAIEmbedding(model="text-embedding-3-large")

# Apply nest_asyncio to avoid event loop conflicts
nest_asyncio.apply()

# Path to the docs folder
docs_folder = "docs"

# List all PDF files in the docs folder
pdf_files = [f for f in os.listdir(docs_folder) if f.endswith('.pdf')]

# Display the available PDF files to the user
print("\n======")
print("\nAvailable PDF files for analysis:")
for i, file in enumerate(pdf_files):
    print(f"{i + 1}. {file}")
print("\n======")

# Prompt the user to select a PDF file by number
file_index = int(input(f"\n{BOLD_BLUE}Select a PDF file by number (1-{len(pdf_files)}): {RESET}")) - 1

# Get the selected PDF file
selected_pdf = pdf_files[file_index]
pdf_path = os.path.join(docs_folder, selected_pdf)

# Get document tools for vector querying and summarization for the selected PDF, passing the embedding model
vector_query_tool, summary_tool = get_doc_tools(pdf_path, selected_pdf, embed_model)

# Configure the LLM service
llm = OpenAI(model="gpt-4o", temperature=0.2, max_tokens=2000)

# Initialize the agent worker and agent runner with verbose=False for high-level mode
agent_worker = FunctionCallingAgentWorker.from_tools(
    [vector_query_tool, summary_tool],
    llm=llm,
    verbose=False
)
agent = AgentRunner(agent_worker)

# Function to execute a task in high-level mode
def execute_task(query):
    response = agent.query(query)
    
    # Display the response
    print("\n======")
    print(f"{BOLD_RED}{response}{RESET}")
    print("\n======")

# Commenting out the debug function for now
"""
# Function to handle debugging and control with verbose=True for lower-level mode
def debug_task(query):
    # Initialize the agent worker and agent runner with verbose=True for lower-level mode
    agent_worker = FunctionCallingAgentWorker.from_tools(
        [vector_query_tool, summary_tool],
        llm=llm,
        verbose=False
    )
    agent = AgentRunner(agent_worker)

    # Create and run the task with detailed debug info printed
    task = agent.create_task(query)

    while True:
        step_output = agent.run_step(task.task_id)
        
        # Print details about the completed and upcoming steps
        completed_steps = agent.get_completed_steps(task.task_id)
        print(f"Num completed for task {task.task_id}: {len(completed_steps)}")
        if completed_steps:
            print("\n======")
            print(f"{BOLD_BLUE}{completed_steps[0].output.sources[0].raw_output}{RESET}")
        
        upcoming_steps = agent.get_upcoming_steps(task.task_id)
        print(f"Num upcoming steps for task {task.task_id}: {len(upcoming_steps)}")

        # Break loop if the last step is completed
        if step_output.is_last:
            break
        
        # Optionally, get further input if desired in the loop
        user_input = input("Input for next step (or press Enter to continue): ")
        if user_input:
            step_output = agent.run_step(task.task_id, input=user_input)
    
    # Finalize and print the complete response
    response = agent.finalize_response(task.task_id)
    
    if response.source_nodes:
        print("\n======")
        print(f"{BOLD_BLUE}{str(response)}{RESET}")
        print("\n======")

    else:
        print("\n======")
        print(f"{BOLD_BLUE}No relevant content found for the query.{RESET}")
        print("\n======")
"""

# Main loop for user interaction
while True:
    user_query = input(f"{BOLD_BLACK}Enter your query (or type 'exit' to quit): {RESET}")
    if user_query.lower() == 'exit':
        break
    
    # For now, just using the execute_task function
    execute_task(user_query)

print("Exiting...")
