# Interactive Query Agent with OpenAI and LlamaIndex

This project is an interactive query system that utilizes OpenAI's GPT model and LlamaIndex to analyze and respond to user queries based on a set of provided news articles.

## Features

- **Query System:** Users can input queries and receive answers generated from the provided news articles.
- **Document Tools Integration:** The system processes and utilizes document tools like vector queries and summaries for better information retrieval.
- **Customizable:** The LLM (Language Learning Model) and embeddings can be adjusted to different OpenAI models.
- **Real-time Interaction:** The system supports real-time interaction with nested asyncio loops and an interactive query loop.

## Prerequisites

- Python 3.x
- An OpenAI API key
- Necessary Python packages (see below)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/editor-in-chief.git
    cd editor-in-chief
    ```

2. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

3. Create a `.env` file in the project root directory and add your OpenAI API key:

    ```bash
    OPENAI_API_KEY=your_openai_api_key
    ```

## Usage

1. Ensure you have your news articles saved as `.txt` files in the `docs` directory.
2. Run the main script:

    ```bash
    python 03-multi-agent-rag.py
    ```

3. Interact with the query loop by asking questions. To exit the loop, type `exit`.

## Customization

### Modify Agent Behavior

You can modify the behavior and response style of the agent by adjusting the `system_prompt` in the script:

```python
system_prompt="""
You are an AI journalist specializing in generating concise, accurate, and objective news reports. 
...
"""
```

### Adjust the Language Model

The LLM and embeddings can be customized by changing the model names in the script:

```python
llm = LlamaOpenAI(model="gpt-4o")
embed_model = OpenAIEmbedding(model="text-embedding-3-large")
```

## Color-coded Output

The system outputs the user's input in **bold black** and the agent's response in **dark blue** using ANSI escape codes. Note that not all terminals support colored output.

## Contributing

Feel free to open issues or submit pull requests if you find bugs or have improvements.

## License

This project is licensed under the MIT License.
