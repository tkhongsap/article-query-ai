# import json

# output_dir =r'D:\github-repo-tkhongsap\editor-in-chief\docs'

# # Load the JSON file
# with open('articles.json', 'r', encoding='utf-8') as f:
#     data = json.load(f)

# # Save the decoded JSON content into a new file
# with open('articles_decoded.json', 'w', encoding='utf-8') as f:
#     json.dump(data, f, ensure_ascii=False, indent=4)

import os
import requests
import json
import math

# API URL and headers
url = "https://editors.spacebar.th/api/articles"
headers = {
    "Authorization": "Bearer 57a66138938d7be50285f274c57d44266805285b0f4e25e2678c35e52df1a0c5628e9b7ab0440ce0de8d6a5ea2b5da5d21a64e077ec950439192eece3fee9b44482a2eb6ae4ebaefa3b1297aca2a54d79ab16c207a837a8415db0bb3d1bc1778ef5156568b442399a679b9ae03ac1fe245264d8e93425e637528abbfcbf3e9b5"
}

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
    "pagination[pageSize]": "50"
}

# Directory to save the split files
output_dir = r'D:\github-repo-tkhongsap\editor-in-chief\docs'

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Fetch all articles
all_articles = []
has_more_data = True

while has_more_data:
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    
    # Append the data from this page to the all_articles list
    all_articles.extend(data.get('data', []))
    
    # Get pagination information
    pagination = data.get('meta', {}).get('pagination', {})
    current_page = pagination.get('page', 1)
    total_pages = pagination.get('pageCount', 1)
    
    # Check if there are more pages to fetch
    if current_page < total_pages:
        params["pagination[page]"] = current_page + 1
    else:
        has_more_data = False

# Decode JSON (if needed) and split the articles into smaller files

# Determine the number of articles
num_articles = len(all_articles)

# Calculate the number of articles per file to create around 100 files
articles_per_file = math.ceil(num_articles / 100)

# Split the articles and save to separate files
for i in range(0, num_articles, articles_per_file):
    # Get the chunk of articles
    chunk = all_articles[i:i + articles_per_file]

    # Decode the chunk if needed (this step is a placeholder, you can adjust it based on your specific decoding needs)
    decoded_chunk = json.loads(json.dumps(chunk, ensure_ascii=False))  # Handles decoding in case of special characters

    # Create the output file path
    output_file = os.path.join(output_dir, f'articles_part_{i//articles_per_file + 1}.json')

    # Save the decoded chunk to a new JSON file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(decoded_chunk, f, ensure_ascii=False, indent=4)

    print(f'Saved {len(chunk)} articles to {output_file}')

print(f"Total articles saved: {num_articles}")

