import os
import requests
import json
import math
from datetime import datetime, timedelta
import pytz
from dotenv import load_dotenv
from collections import defaultdict

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI API client with API key from environment variables
openai_api_key = os.getenv('OPENAI_API_KEY')

# Constants
VECTOR_STORE_ID = "vs_I09vB9pr80qOUB7W5LIRBeIo"  # Replace with your actual vector store ID
UPLOAD_URL = "https://api.openai.com/v1/files"
BATCH_URL = f"https://api.openai.com/v1/vector_stores/{VECTOR_STORE_ID}/file_batches"
HEADERS = {
    "Authorization": f"Bearer {openai_api_key}",
    "Content-Type": "application/json",
    "OpenAI-Beta": "assistants=v2"
}

# Directory paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
tmp_dir = os.path.join(BASE_DIR, 'tmp')
docs_by_date_dir = os.path.join(tmp_dir, 'docs-by-date')
final_docs_dir = os.path.join(BASE_DIR, 'docs')

# Ensure directories exist
for dir_path in [tmp_dir, docs_by_date_dir, final_docs_dir]:
    os.makedirs(dir_path, exist_ok=True)

# Timezone definitions
utc_tz = pytz.utc
bangkok_tz = pytz.timezone('Asia/Bangkok')

def convert_to_bangkok_time(utc_datetime_str):
    utc_datetime = datetime.strptime(utc_datetime_str, "%Y-%m-%dT%H:%M:%S.%fZ")
    utc_datetime = utc_tz.localize(utc_datetime)
    bangkok_datetime = utc_datetime.astimezone(bangkok_tz)
    return bangkok_datetime.strftime("%Y-%m-%d %H:%M:%S")

def extract_articles():
    # API URL and headers
    url = "https://editors.spacebar.th/api/articles"
    headers = {
        "Authorization": "Bearer 57a66138938d7be50285f274c57d44266805285b0f4e25e2678c35e52df1a0c5628e9b7ab0440ce0de8d6a5ea2b5da5d21a64e077ec950439192eece3fee9b44482a2eb6ae4ebaefa3b1297aca2a54d79ab16c207a837a8415db0bb3d1bc1778ef5156568b442399a679b9ae03ac1fe245264d8e93425e637528abbfcbf3e9b5"
    }

    # Calculate the date 14 days ago from today
    date_14_days_ago = (datetime.utcnow() - timedelta(days=14)).isoformat()

    # Initialize parameters for the first request
    params = {
        "populate[categories]": "true",
        "populate[tags]": "true",
        "populate[highlights]": "true",
        "populate[contents][populate]": "*",
        "populate[contents][on][article.richtext]": "true",
        "populate[contents][on][article.quote]": "true",
        "populate[contents][on][article.html]": "true",
        "populate[credits][populate][credit][populate][collaborator]": "true",
        "populate[credits][populate][credit][populate][title]": "true",
        "populate[share][populate]": "*",
        "populate[references]": "true",
        "sort[publishedAt]": "desc",
        "pagination[page]": "1",
        "pagination[pageSize]": "50",
        "filters[publishedAt][$gte]": date_14_days_ago
    }

    # Fetch all articles
    all_articles = []
    has_more_data = True

    while has_more_data:
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        
        all_articles.extend(data.get('data', []))
        
        pagination = data.get('meta', {}).get('pagination', {})
        current_page = pagination.get('page', 1)
        total_pages = pagination.get('pageCount', 1)
        
        if current_page < total_pages:
            params["pagination[page]"] = current_page + 1
        else:
            has_more_data = False

    # Debug: Print the first and last published dates in Bangkok time
    if all_articles:
        first_date_utc = all_articles[-1]['attributes']['publishedAt']
        last_date_utc = all_articles[0]['attributes']['publishedAt']
        
        first_date_bangkok = convert_to_bangkok_time(first_date_utc)
        last_date_bangkok = convert_to_bangkok_time(last_date_utc)
        
        print(f"First publishedAt date in Bangkok time: {first_date_bangkok}")
        print(f"Last publishedAt date in Bangkok time: {last_date_bangkok}")
    else:
        print("No articles found within the last 14 days.")

    # Update each article's publishedAt field to Bangkok time
    for article in all_articles:
        article['attributes']['publishedAt'] = convert_to_bangkok_time(article['attributes']['publishedAt'])

    # Determine the number of articles
    num_articles = len(all_articles)

    # Calculate the number of articles per file to create around 100 files
    articles_per_file = math.ceil(num_articles / 100)

    # Split the articles and save to separate files
    for i in range(0, num_articles, articles_per_file):
        chunk = all_articles[i:i + articles_per_file]
        decoded_chunk = json.loads(json.dumps(chunk, ensure_ascii=False))
        output_file = os.path.join(tmp_dir, f'articles_part_{i//articles_per_file + 1}.json')

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(decoded_chunk, f, ensure_ascii=False, indent=4)

        print(f'Saved {len(chunk)} articles to {output_file}')

    print(f"Total articles saved: {num_articles}")

def filter_articles_by_date():
    current_date = datetime.now()
    fourteen_days_ago = current_date - timedelta(days=14)

    def is_within_last_14_days(published_at_str):
        published_at = datetime.strptime(published_at_str, "%Y-%m-%d %H:%M:%S")
        return published_at >= fourteen_days_ago

    for file_name in os.listdir(tmp_dir):
        if file_name.endswith(".json"):
            file_path = os.path.join(tmp_dir, file_name)
            
            with open(file_path, "r", encoding="utf-8") as file:
                articles = json.load(file)
            
            filtered_articles = []
            for article in articles:
                published_at = article["attributes"]["publishedAt"]
                
                if is_within_last_14_days(published_at):
                    filtered_articles.append(article)
                else:
                    break
            
            if filtered_articles:
                output_file_name = f"article_date_{file_name.replace('.json', '')}.json"
                output_file_path = os.path.join(docs_by_date_dir, output_file_name)
                
                with open(output_file_path, "w", encoding="utf-8") as output_file:
                    json.dump(filtered_articles, output_file, ensure_ascii=False, indent=4)
                
                print(f"Saved {len(filtered_articles)} articles to {output_file_path}")
            else:
                print(f"No recent articles found in {file_name}, skipping...")

    print("Filtering complete.")

def write_dict_to_markdown(article, file):
    file.write(f"# {article['title']}\n\n")
    file.write(f"**ID:** {article['id']}\n")
    file.write(f"**Slug:** {article['slug']}\n")
    file.write(f"**Published At:** {article['publishedAt']}\n")
    file.write(f"**Locale:** {article['locale']}\n")
    file.write(f"**Excerpt:** {article['excerpt']}\n")
    file.write(f"**Category:** {article['category']}\n")
    file.write(f"**Tags:** {article['tags']}\n")
    file.write("\n")

    if article['highlights']:
        file.write(f"## Highlights\n")
        for highlight in article['highlights']:
            file.write(f"- {highlight}\n")
        file.write("\n")

    if article['content']:
        file.write(f"## Content\n\n")
        for paragraph in article['content']:
            file.write(f"{paragraph}\n\n")

    if article['credit']:
        file.write(f"## Credit\n")
        for credit in article['credit']:
            file.write(f"- {credit}\n")
        file.write("\n")

    file.write("\n" + "="*40 + "\n\n")

def extract_metadata(json_data):
    result = []
    
    for item in json_data:
        attributes = item.get('attributes', {})
        
        categories = attributes.get('categories', {}).get('data', [])
        flattened_category = ', '.join(
            [f"{cat['attributes']['title']}, {cat['attributes']['slug']}" for cat in categories]
        )
        
        tags = attributes.get('tags', {}).get('data', [])
        tag_list = ', '.join([tag['attributes']['title'] for tag in tags])
        
        highlights = attributes.get('highlights', [])
        highlight_list = [hl['content'] for hl in highlights]
        
        contents = attributes.get('contents', [])
        content_list = [cont['content'] for cont in contents]
        
        credits = attributes.get('credits', [])
        credit_list = [
            credit['credit']['data']['attributes']['collaborator']['data']['attributes']['name']
            for credit in credits if credit.get('credit') and credit['credit'].get('data')
        ]
        
        metadata = {
            "id": item.get('id'),
            "title": attributes.get('title'),
            "slug": attributes.get('slug'),
            "publishedAt": attributes.get('publishedAt'),
            "locale": attributes.get('locale'),
            "excerpt": attributes.get('excerpt'),
            "category": flattened_category,
            "tags": tag_list,
            "highlights": highlight_list,
            "content": content_list,
            "credit": credit_list
        }
        
        result.append(metadata)
    
    return result

def write_articles_by_date():
    articles_by_date = defaultdict(list)

    for filename in os.listdir(docs_by_date_dir):
        if filename.endswith('.json'):
            input_file = os.path.join(docs_by_date_dir, filename)
            
            with open(input_file, 'r', encoding='utf-8') as file:
                data = json.load(file)
            
            cleaned_data = extract_metadata(data)
            
            for item in cleaned_data:
                published_at = item['publishedAt']
                published_date = published_at.split(' ')[0]
                articles_by_date[published_date].append(item)

    for date, articles in articles_by_date.items():
        output_filename = f"article_{date}.md"
        output_path = os.path.join(final_docs_dir, output_filename)
        
        with open(output_path, 'w', encoding='utf-8') as file:
            for article in articles:
                write_dict_to_markdown(article, file)

    print(f"Articles have been successfully converted to Markdown files in {final_docs_dir}, grouped by date.")

def list_files(purpose=None):
    try:
        url = "https://api.openai.com/v1/files"
        if purpose:
            url += f"?purpose={purpose}"
        
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()

        files = response.json()["data"]
        return files

    except Exception as e:
        print(f"An error occurred while listing the files: {str(e)}")
        return []

def delete_file(file_id):
    try:
        url = f"https://api.openai.com/v1/files/{file_id}"
        response = requests.delete(url, headers=HEADERS)
        response.raise_for_status()

        if response.json().get("deleted", False):
            print(f"File with ID {file_id} was successfully deleted.")
        else:
            print(f"Failed to delete the file with ID {file_id}.")

    except Exception as e:
        print(f"An error occurred while trying to delete the file: {str(e)}")

def get_markdown_files_from_docs():
    return [os.path.join(final_docs_dir, f) for f in os.listdir(final_docs_dir) if f.endswith('.md')]

def upload_files_to_openai(file_paths):
    file_ids = []
    for file_path in file_paths:
        filename = os.path.basename(file_path)
        with open(file_path, 'rb') as f:
            response = requests.post(
                UPLOAD_URL,
                headers={
                    "Authorization": f"Bearer {openai_api_key}",
                },
                files={
                    'file': (filename, f, 'text/markdown')
                },
                data={
                    'purpose': 'user_data'
                }
            )
            if response.status_code == 200:
                file_id = response.json()['id']
                file_ids.append(file_id)
                print(f"Uploaded {filename} successfully, file_id: {file_id}")
            else:
                print(f"Failed to upload {filename}: {response.text}")
    return file_ids

def create_vector_store_file_batch(file_ids):
    data = {
        "file_ids": file_ids,
    }
    response = requests.post(
        BATCH_URL,
        headers=HEADERS,
        json=data
    )
    if response.status_code == 200:
        batch_id = response.json()['id']
        print(f"Vector store file batch created successfully, batch_id: {batch_id}")
    else:
        print(f"Failed to create vector store file batch: {response.text}")

def main():
    print("Step 1: Extracting articles...")
    extract_articles()

    print("\nStep 2: Filtering articles by date...")
    filter_articles_by_date()

    print("\nStep 3: Writing articles by date...")
    write_articles_by_date()

    print("\nStep 4: Uploading articles to vector store...")
    print("Listing and deleting existing files...")
    files = list_files(purpose='user_data')

    for file in files:
        print(f"Deleting file: {file['filename']} (ID: {file['id']})")
        delete_file(file['id'])

    print("Uploading new files to the vector store...")
    file_paths = get_markdown_files_from_docs()

    file_ids = upload_files_to_openai(file_paths)

    if file_ids:
        create_vector_store_file_batch(file_ids)

if __name__ == "__main__":
    main()