

# 💬 Intelligence Social News Analytics

This project is a web application built using [Streamlit](https://streamlit.io/), designed to provide intelligent social news analytics. The application integrates with OpenAI's API to generate insights and responses based on user inputs, and it features a customized UI for displaying messages.

## Features

- **AI-Powered Chatbot**: Interact with an AI-powered assistant using OpenAI's API.
- **Custom CSS Styling**: The application includes custom CSS for both the main page and social news banner.
- **Session Management**: The app manages chat history within the session to maintain context.
- **Interactive Sidebar**: Provides additional information and model selection options.
- **Image Handling**: Loads and displays user and assistant avatars using Base64 encoded images.

## Project Structure

- **`app.py`**: The main application script that initializes the Streamlit app, handles user input, and displays responses.
- **`utils/`**: Contains utility functions used across the application.
  - **`custom_css_main_page.py`**: Custom CSS for the main page.
  - **`custom_css_banner.py`**: Custom CSS for the social news banner.
  - **`openai_utils.py`**: Utility functions for interacting with OpenAI's API.
  - **`message_utils.py`**: Functions for formatting and displaying messages in the chatbot UI.

## Setup and Installation

### Prerequisites

- Python 3.7+
- Streamlit
- OpenAI API Key

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/intelligence-social-news-analytics.git
   cd intelligence-social-news-analytics
   ```

2. **Install the required packages**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your OpenAI API key**:
   - Add your OpenAI API key to your Streamlit secrets. You can do this by creating a `.streamlit/secrets.toml` file in the root directory with the following content:
     ```toml
     [secrets]
     OPENAI_API_KEY = "your-openai-api-key"
     ```

4. **Run the application**:
   ```bash
   streamlit run app.py
   ```

## Usage

1. **Model Selection**: Use the radio button in the sidebar to select your preferred AI model.
2. **Chat Input**: Enter your message in the chat input field at the bottom of the page.
3. **View Responses**: The AI assistant will respond to your messages in real-time, displayed with custom-styled messages.

## Utility Functions

- **`format_message(text)`**:
  - Formats the messages for display in the chatbot UI.
  - Escapes HTML in the text and properly formats code blocks.

- **`message_func(text, user_icon_base64, assistant_icon_base64, is_user=False, model="Claude-3 Haiku")`**:
  - Displays a message in the chatbot UI.
  - Handles both user and assistant messages with appropriate alignment and styling.

## Customization

You can customize the CSS styles or add additional functionalities by modifying the utility scripts under the `utils/` directory.

## Contributing

Contributions are welcome! Please fork this repository, make your changes, and submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any inquiries, please contact `ta.khongsap@gmail.com`.
