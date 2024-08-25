
# Social News Analysis and Query App

This repository contains a Retrieval-Augmented Generation (RAG) pipeline for creating a social news analysis and query application. The app allows users to fetch, filter, and analyze articles, as well as query the data using a Streamlit-based interface.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Scripts](#scripts)
- [Streamlit App](#streamlit-app)
- [Contributing](#contributing)
- [License](#license)

## Introduction

The Social News Analysis and Query App is built to fetch articles from a remote API, filter them by date, and provide a user-friendly interface for querying the articles. The app utilizes Python scripts to process and filter articles and a Streamlit app to present the data in an interactive way.

## Features

- **Article Extraction**: Fetches articles from a remote API and stores them locally in JSON format.
- **Date Filtering**: Filters articles by specific date ranges.
- **Streamlit Interface**: Provides an interactive interface for querying and analyzing the articles.
- **Complex Query Handling**: Utilizes Large Language Models (LLMs) and LlamaIndex to handle complex queries that go beyond simple searches.

## Installation

### Prerequisites

- Python 3.8 or above
- pip (Python package installer)

### Clone the Repository

```bash
git clone https://github.com/yourusername/social-news-analysis-app.git
cd social-news-analysis-app
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

## Usage

### 1. Extract Articles

Run the script to fetch articles from the API and split them into smaller JSON files.

```bash
python 00-extract-articles.py
```

### 2. Filter Articles by Date

Use the date filtering script to filter the articles by a specific date range.

```bash
python 01-filter-articles-by-date.py
```

### 3. Run the Streamlit App

Start the Streamlit app to interact with the articles.

```bash
streamlit run app-streamlit.py
```

## Scripts

### `00-extract-articles.py`

This script fetches articles from a remote API and splits them into multiple JSON files.

### `01-filter-articles-by-date.py`

This script filters the articles by a specific date range.

### `02-write-articles-by-date.py`

This script writes the filtered articles to files for further processing.

### `app-streamlit.py`

The main script that runs the Streamlit app for querying and analyzing the articles.

## Streamlit App

The Streamlit app (`app-streamlit.py`) is the core of the social news analysis and query interface. It is designed to enable users to interact with the extracted and filtered articles through a user-friendly interface. The app offers the following key features:

- **Multi-Agent Document RAG**: This app uniquely integrates a multi-agent system that leverages both Large Language Models (LLMs) and LlamaIndex. This allows for more complex and nuanced queries, enabling users to analyze the content deeply.
  
- **Complex Query Handling**: Users can query complex questions, such as comparing different topics or providing in-depth analysis based on the content. This goes beyond simple keyword searches, making the app a powerful tool for social news analysis.

- **LlamaIndex Integration**: The app uses LlamaIndex to structure and retrieve data efficiently, allowing users to interact with the content in a meaningful way.

- **Custom User Interface**: The app includes custom CSS for a polished look and feel, making the user experience more engaging.

### Example Queries

Here are some examples of complex queries that the app can handle:

- "Compare the sentiment of articles published on climate change versus those on economic policies."
- "Provide an analysis of the most mentioned topics in the last month's articles."
- "Summarize the different perspectives on social justice issues across various articles."

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue if you find any bugs or have suggestions for improvements.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
