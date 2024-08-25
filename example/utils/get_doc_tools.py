from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, SummaryIndex
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.tools import FunctionTool, QueryEngineTool
from llama_index.core.vector_stores import MetadataFilters, FilterCondition
from typing import List, Optional, Dict

def get_doc_tools(
    file_path: str,
    name: str,
) -> str:
    """Get vector query and summary query tools from a document."""

    # Load documents
    documents = SimpleDirectoryReader(input_files=[file_path]).load_data()
    splitter = SentenceSplitter(chunk_size=1024)
    nodes = splitter.get_nodes_from_documents(documents)
    vector_index = VectorStoreIndex(nodes)
    
    def vector_query(
        query: str, 
        categories: Optional[List[str]] = None,
        tags: Optional[List[str]] = None,
        locale: Optional[str] = None,
        created_at: Optional[str] = None,
        slug: Optional[str] = None
    ) -> str:
        """Query with metadata filters to enhance RAG performance."""
    
        metadata_filters = []
        
        # Add metadata filters based on provided options
        if categories:
            metadata_filters.extend([{"key": "category", "value": category} for category in categories])
        
        if tags:
            metadata_filters.extend([{"key": "tags", "value": tag} for tag in tags])
        
        if locale:
            metadata_filters.append({"key": "locale", "value": locale})
        
        if created_at:
            metadata_filters.append({"key": "created_at", "value": created_at})
        
        if slug:
            metadata_filters.append({"key": "slug", "value": slug})
        
        query_engine = vector_index.as_query_engine(
            similarity_top_k=5,
            filters=MetadataFilters.from_dicts(
                metadata_filters,
                condition=FilterCondition.AND  # Use AND to combine filters
            )
        )
        
        response = query_engine.query(query)
        return response
        
    
    vector_query_tool = FunctionTool.from_defaults(
        name=f"vector_tool_{name}",
        fn=vector_query
    )
    
    summary_index = SummaryIndex(nodes)
    summary_query_engine = summary_index.as_query_engine(
        response_mode="tree_summarize",
        use_async=True,
    )
    summary_tool = QueryEngineTool.from_defaults(
        name=f"summary_tool_{name}",
        query_engine=summary_query_engine,
        description=(
            "Use ONLY IF you want to get a holistic summary of the document. "
            "Do NOT use if you have specific questions over the document."
        ),
    )
    return vector_query_tool, summary_tool


# from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, SummaryIndex
# from llama_index.core.node_parser import SentenceSplitter
# from llama_index.core.tools import FunctionTool, QueryEngineTool
# from llama_index.core.vector_stores import MetadataFilters, FilterCondition
# from typing import List, Optional

# def get_doc_tools(
#     file_path: str,
#     name: str,
# ) -> str:
#     """Get vector query and summary query tools from a document."""

#     # load documents
#     documents = SimpleDirectoryReader(input_files=[file_path]).load_data()
#     splitter = SentenceSplitter(chunk_size=1024)
#     nodes = splitter.get_nodes_from_documents(documents)
#     vector_index = VectorStoreIndex(nodes)
    
#     def vector_query(
#         query: str, 
#         page_numbers: Optional[List[str]] = None
#     ) -> str:
#         """Use to answer questions over the MetaGPT paper.
    
#         Useful if you have specific questions over the MetaGPT paper.
#         Always leave page_numbers as None UNLESS there is a specific page you want to search for.
    
#         Args:
#             query (str): the string query to be embedded.
#             page_numbers (Optional[List[str]]): Filter by set of pages. Leave as NONE 
#                 if we want to perform a vector search
#                 over all pages. Otherwise, filter by the set of specified pages.
        
#         """
    
#         page_numbers = page_numbers or []
#         metadata_dicts = [
#             {"key": "page_label", "value": p} for p in page_numbers
#         ]
        
#         query_engine = vector_index.as_query_engine(
#             similarity_top_k=5,
#             filters=MetadataFilters.from_dicts(
#                 metadata_dicts,
#                 condition=FilterCondition.OR
#             )
#         )
#         response = query_engine.query(query)
#         return response
        
    
#     vector_query_tool = FunctionTool.from_defaults(
#         name=f"vector_tool_{name}",
#         fn=vector_query
#     )
    
#     summary_index = SummaryIndex(nodes)
#     summary_query_engine = summary_index.as_query_engine(
#         response_mode="tree_summarize",
#         use_async=True,
#     )
#     summary_tool = QueryEngineTool.from_defaults(
#         name=f"summary_tool_{name}",
#         query_engine=summary_query_engine,
#         description=(
#             "Use ONLY IF you want to get a holistic summary of MetaGPT. "
#             "Do NOT use if you have specific questions over MetaGPT."
#         ),
#     )
#     return vector_query_tool, summary_tool