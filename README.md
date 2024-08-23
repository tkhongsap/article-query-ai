
# DocQuery AI

**DocQuery AI** is a Python-based tool designed for loading documents, summarizing content, and querying information using OpenAI's GPT models. The program processes documents into nodes and provides summarization and context-based retrieval via a user-friendly query interface.

## Features

- **Document Loading**: Automatically load documents from a specified directory.
- **Document Processing**: Split documents into nodes for efficient processing.
- **Summarization**: Use OpenAI's GPT models to summarize content.
- **Context-based Querying**: Retrieve specific information from documents based on user queries.
- **User-friendly Interface**: Continuous loop to interactively query the system with color-coded output for better readability.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/DocQuery-AI.git
   cd DocQuery-AI
   ```

2. **Install the required dependencies**:
   You can install the required dependencies using `pip`:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   - Create a `.env` file in the root directory of your project.
   - Add your OpenAI API key to the `.env` file:
     ```plaintext
     OPENAI_API_KEY=your-openai-api-key
     ```

## Usage

1. **Prepare your documents**:
   - Place the documents you want to process in the `docs` directory within the root of your project.

2. **Run the program**:
   - Execute the main Python script:
     ```bash
     python main.py
     ```

3. **Interact with the system**:
   - After starting the program, you can enter queries related to the loaded documents.
   - Type `exit` to quit the program.

## Example Queries

- "Summarize the content of document X."
- "What is the key point discussed in section Y?"

## Contributing

If you'd like to contribute to this project, feel free to fork the repository and submit a pull request. You can also open issues for any bugs or feature requests.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
