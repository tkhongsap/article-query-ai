from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, SummaryIndex
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.tools import FunctionTool, QueryEngineTool
from llama_index.core.vector_stores import MetadataFilters, FilterCondition
from typing import List, Optional, Dict

def get_doc_tools(
    file_path: str,
    name: str,
) -> str:
    """Get vector query and summary query tools from a document.

    Args:
        file_path (str): Path to the document file.
        name (str): A unique name identifier for the tools.

    Returns:
        Tuple[str, str]: A tuple containing the vector query tool and the summary tool.
    """

    # Load the document from the specified file path
    documents = SimpleDirectoryReader(input_files=[file_path]).load_data()

    # Split the document into smaller chunks (nodes) for efficient querying and summarization
    splitter = SentenceSplitter(chunk_size=1024)
    nodes = splitter.get_nodes_from_documents(documents)

    # Create a VectorStoreIndex from the nodes, which will be used for vector-based queries
    vector_index = VectorStoreIndex(nodes)
    
    # Define a function for querying the document using metadata filters
    def vector_query(
        query: str, 
        categories: Optional[List[str]] = None,
        tags: Optional[List[str]] = None,
        locale: Optional[str] = None,
        created_at: Optional[str] = None,
        slug: Optional[str] = None
    ) -> str:
        """Query the document with metadata filters to enhance RAG performance.

        Args:
            query (str): The query string.
            categories (Optional[List[str]]): List of categories to filter by.
            tags (Optional[List[str]]): List of tags to filter by.
            locale (Optional[str]): Locale to filter by.
            created_at (Optional[str]): Creation date to filter by.
            slug (Optional[str]): Slug to filter by.

        Returns:
            str: The query response.
        """
    
        # Initialize an empty list for metadata filters
        metadata_filters = []
        
        # Add filters for categories, if provided
        if categories:
            metadata_filters.extend([{"key": "category", "value": category} for category in categories])
        
        # Add filters for tags, if provided
        if tags:
            metadata_filters.extend([{"key": "tags", "value": tag} for tag in tags])
        
        # Add filter for locale, if provided
        if locale:
            metadata_filters.append({"key": "locale", "value": locale})
        
        # Add filter for creation date, if provided
        if created_at:
            metadata_filters.append({"key": "created_at", "value": created_at})
        
        # Add filter for slug, if provided
        if slug:
            metadata_filters.append({"key": "slug", "value": slug})
        
        # Create a query engine with the metadata filters and a similarity threshold (top 5 similar results)
        query_engine = vector_index.as_query_engine(
            similarity_top_k=5,
            filters=MetadataFilters.from_dicts(
                metadata_filters,
                condition=FilterCondition.AND  # Combine filters using AND logic
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
