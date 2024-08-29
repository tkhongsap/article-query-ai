from utils.markdown_parser import parse_markdown
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, SummaryIndex
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.tools import FunctionTool, QueryEngineTool
from llama_index.core.vector_stores import MetadataFilters, FilterCondition
from typing import List, Optional, Tuple, Dict

def get_doc_tools(
    file_path: str,
    name: str,
) -> Tuple[FunctionTool, QueryEngineTool]:
    """Get vector query and summary query tools from a parsed markdown document.

    Args:
        file_path (str): Path to the markdown document file.
        name (str): A unique name identifier for the tools.

    Returns:
        Tuple[FunctionTool, QueryEngineTool]: A tuple containing the vector query tool and the summary tool.
    """
    
    # Use markdown_parser to load and parse the markdown file
    # documents = parse_markdown(file_path)
    documents = SimpleDirectoryReader(input_files=[file_path]).load_data()
    
    # Split the document into smaller chunks (nodes) for efficient querying and summarization
    splitter = SentenceSplitter(chunk_size=1024, chunk_overlap=100)  # Adjust chunk_size as needed
    nodes = splitter.get_nodes_from_documents(documents)

    # Create a VectorStoreIndex from the nodes for vector-based queries
    vector_index = VectorStoreIndex(nodes)
    
    # Define a function for querying the document using metadata filters
    def vector_query(
        query: str, 
        filters: Optional[Dict[str, Optional[List[str]]]] = None
    ) -> str:
        """Query the document with metadata filters to enhance RAG performance.

        Args:
            query (str): The query string.
            filters (Optional[Dict[str, Optional[List[str]]]]): A dictionary to filter documents by specific metadata fields, 
                such as 'category', 'tags', 'locale', 'publishedAt', 'slug', or 'id'. 
                Example: {"category": ["world", "nations"], "tags": ["politics"]}.

        Returns:
            str: The query response.
        """
        
        # Prepare metadata filters based on the provided dictionary
        metadata_dicts = []
        if filters:
            for key, values in filters.items():
                if isinstance(values, list):
                    metadata_dicts.extend([{"key": key, "value": v} for v in values])
                else:
                    metadata_dicts.append({"key": key, "value": values})
        
        # Create a query engine with the metadata filters and a similarity threshold
        query_engine = vector_index.as_query_engine(
            similarity_top_k=5,
            filters=MetadataFilters.from_dicts(
                metadata_dicts,
                condition=FilterCondition.OR  # OR logic can be changed to AND based on your needs
            )
        )
        
        # Execute the query and return the response
        response = query_engine.query(query)
        return response
    
    # Create a FunctionTool for the vector query and give it a unique name
    vector_query_tool = FunctionTool.from_defaults(
        name=f"vector_tool_{name}",
        fn=vector_query
    )
    
    # Create a SummaryIndex from the nodes for document summarization
    summary_index = SummaryIndex(nodes)

    # Create a query engine for generating holistic summaries of the document
    summary_query_engine = summary_index.as_query_engine(
        response_mode="tree_summarize",  # Use tree summarization method
        use_async=True,  # Enable asynchronous execution
    )

    # Create a QueryEngineTool for summarization with a description for when to use it
    summary_tool = QueryEngineTool.from_defaults(
        name=f"summary_tool_{name}",
        query_engine=summary_query_engine,
        description=(
            "Use ONLY IF you want to get a holistic summary of the document. "
            "Do NOT use if you have specific questions over the document."
        ),
    )

    # Return both the vector query tool and the summary tool
    return vector_query_tool, summary_tool
