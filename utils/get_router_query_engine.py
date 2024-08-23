import os
from llama_index.core import SimpleDirectoryReader, Settings, SummaryIndex, VectorStoreIndex
from llama_index.core.node_parser import SentenceSplitter
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.tools import QueryEngineTool
from llama_index.core.query_engine.router_query_engine import RouterQueryEngine
from llama_index.core.selectors import LLMSingleSelector

def get_router_query_engine(pdf_file):
    """
    Initializes and returns a RouterQueryEngine for querying the given PDF file.
    
    Args:
        pdf_file (str): The path to the PDF file to be loaded.
    
    Returns:
        RouterQueryEngine: Configured router query engine.
    """
    # Load documents from the PDF file
    documents = SimpleDirectoryReader(input_files=[pdf_file]).load_data()

    # Split documents into nodes
    splitter = SentenceSplitter(chunk_size=1024)
    nodes = splitter.get_nodes_from_documents(documents)

    # Define LLM and embedding model settings
    Settings.llm = OpenAI(model="gpt-4o-mini")
    Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-large")

    # Create summary and vector indices
    summary_index = SummaryIndex(nodes)
    vector_index = VectorStoreIndex(nodes)

    # Define query engines for summary and vector indices
    summary_query_engine = summary_index.as_query_engine(
        response_mode="tree_summarize",
        use_async=True,
    )
    vector_query_engine = vector_index.as_query_engine()

    # Create QueryEngineTools for each query engine
    summary_tool = QueryEngineTool.from_defaults(
        query_engine=summary_query_engine,
        description="Useful for summarization questions",
    )
    vector_tool = QueryEngineTool.from_defaults(
        query_engine=vector_query_engine,
        description="Useful for retrieving specific context.",
    )

    # Create and return a RouterQueryEngine
    query_engine = RouterQueryEngine(
        selector=LLMSingleSelector.from_defaults(),
        query_engine_tools=[summary_tool, vector_tool],
        verbose=True,
    )

    return query_engine
