import re
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, SummaryIndex
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.tools import FunctionTool, QueryEngineTool
from llama_index.core.vector_stores import MetadataFilters, FilterCondition
from llama_index.embeddings.openai import OpenAIEmbedding
from typing import List, Optional

def get_doc_tools(
    file_path: str,
    name: str,
    embedding_model: OpenAIEmbedding  # Add the embedding model parameter here
) -> tuple:
    """Get vector query and summary query tools from a document."""

    # Sanitize the name to ensure it only contains valid characters
    sanitized_name = re.sub(r'[^a-zA-Z0-9_-]', '_', name)

    # Load documents
    documents = SimpleDirectoryReader(input_files=[file_path]).load_data()
    splitter = SentenceSplitter(chunk_size=1024)
    nodes = splitter.get_nodes_from_documents(documents)

    # Create the vector store index with the custom embedding model
    vector_index = VectorStoreIndex(nodes, embedding=embedding_model)

    def vector_query(
        query: str, 
        page_numbers: Optional[List[str]] = None
    ) -> str:
        """Use to answer questions over the document."""

        page_numbers = page_numbers or []
        metadata_dicts = [
            {"key": "page_label", "value": p} for p in page_numbers
        ]

        query_engine = vector_index.as_query_engine(
            similarity_top_k=2,
            filters=MetadataFilters.from_dicts(
                metadata_dicts,
                condition=FilterCondition.OR
            )
        )
        response = query_engine.query(query)
        return response

    # Create vector query tool
    vector_query_tool = FunctionTool.from_defaults(
        name=f"vector_tool_{sanitized_name}",
        fn=vector_query
    )

    # Create summary index and tool
    summary_index = SummaryIndex(nodes)
    summary_query_engine = summary_index.as_query_engine(
        response_mode="tree_summarize",
        use_async=True,
    )
    summary_tool = QueryEngineTool.from_defaults(
        name=f"summary_tool_{sanitized_name}",
        query_engine=summary_query_engine,
        description=(
            "Use ONLY IF you want to get a holistic summary of the document. "
            "Do NOT use if you have specific questions."
        ),
    )

    return vector_query_tool, summary_tool
