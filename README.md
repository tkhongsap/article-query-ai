
# Article Query AI Pipeline

This project automates the process of extracting articles, filtering and converting them to markdown files, uploading them to OpenAI's vector store, and interacting with the data through a Streamlit application.

## Table of Contents

- [Project Overview](#project-overview)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Step-by-Step Guide](#step-by-step-guide)
  - [1. Extract Articles](#1-extract-articles)
  - [2. Filter Articles by Date](#2-filter-articles-by-date)
  - [3. Convert Articles to Markdown](#3-convert-articles-to-markdown)
  - [4. Upload Articles to OpenAI Vector Store](#4-upload-articles-to-openai-vector-store)
  - [5. Streamlit Application](#5-streamlit-application)
- [Running the Full Pipeline](#running-the-full-pipeline)
- [Contributing](#contributing)
- [License](#license)

## Project Overview

This project automates the handling of articles through a pipeline that:

1. Extracts articles from an external API.
2. Filters them by date (within the last 14 days).
3. Converts the filtered articles to markdown files.
4. Uploads the markdown files to OpenAI's vector store.
5. Uses a Streamlit application to query and interact with the data through OpenAI's API.

## Prerequisites

- Python 3.x
- pip (Python package installer)
- [Streamlit](https://streamlit.io/)
- [OpenAI API Key](https://platform.openai.com/signup) (stored in a `.env` file)

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/article-query-ai.git
   cd article-query-ai
   ```

2. Install the required Python packages:
   ```sh
   pip install -r requirements.txt
   ```

3. Set up your `.env` file with your OpenAI API key:
   ```sh
   echo "OPENAI_API_KEY=your-openai-api-key" > .env
   ```

## Step-by-Step Guide

### 1. Extract Articles

The first step involves extracting articles from an external API. This is done using the `00-extract-articles.py` script.

- **Script:** `00-extract-articles.py`
- **Functionality:** This script fetches articles from the specified API endpoint, converts the publication times to Bangkok time, and saves the articles into JSON files.
- **Output:** JSON files containing articles, split into smaller chunks for easier processing.

```sh
python 00-extract-articles.py
```

### 2. Filter Articles by Date

The next step is to filter the articles to include only those published within the last 14 days.

- **Script:** `01-filter-articles-by-date.py`
- **Functionality:** This script filters the extracted articles to include only those published within the last 14 days. It saves the filtered articles into a separate directory.
- **Output:** Filtered JSON files.

```sh
python 01-filter-articles-by-date.py
```

### 3. Convert Articles to Markdown

After filtering, the articles are converted to markdown format for easier readability and processing.

- **Script:** `02-write-aritcles-by-date.py`
- **Functionality:** This script converts the JSON files containing filtered articles into markdown files, grouped by their publication date.
- **Output:** Markdown files saved in the `docs` directory.

```sh
python 02-write-aritcles-by-date.py
```

### 4. Upload Articles to OpenAI Vector Store

The markdown files are then uploaded to OpenAI's vector store for querying and analysis.

- **Script:** `03-upload-articles-to-vector-store.py`
- **Functionality:** This script uploads the markdown files to OpenAI's vector store. It first deletes any existing files in the vector store before uploading the new ones.
- **Output:** Files uploaded to the vector store, ready for querying.

```sh
python 03-upload-articles-to-vector-store.py
```

### 5. Streamlit Application

Finally, a Streamlit application allows users to interact with the articles through OpenAI's assistant.

- **Script:** `app-streamlit.py`
- **Functionality:** This Streamlit application provides an interface to query the articles uploaded to the OpenAI vector store. It uses a custom assistant to provide responses based on the uploaded data.
- **Output:** A web application running on `localhost`, where users can interact with the data.

You can access the live Streamlit application at: [News Article Query AI](https://news-article-query-ai-fxfxmrwbqfhf3hnzyappf3s.streamlit.app/).

```sh
streamlit run app-streamlit.py
```

## Running the Full Pipeline

To run the entire pipeline sequentially, follow these steps:

1. Extract articles:
   ```sh
   python 00-extract-articles.py
   ```

2. Filter articles by date:
   ```sh
   python 01-filter-articles-by-date.py
   ```

3. Convert filtered articles to markdown:
   ```sh
   python 02-write-aritcles-by-date.py
   ```

4. Upload markdown files to the OpenAI vector store:
   ```sh
   python 03-upload-articles-to-vector-store.py
   ```

5. Run the Streamlit application:
   ```sh
   streamlit run app-streamlit.py
   ```

## Contributing

If you'd like to contribute to this project, feel free to fork the repository and submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
