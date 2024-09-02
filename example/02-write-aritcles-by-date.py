import os
import json
from datetime import datetime, timedelta
from collections import defaultdict

# Define input and output directories
input_dir = r'D:\github-repo-tkhongsap\article-query-ai\tmp\docs-by-date'
output_dir = r'D:\github-repo-tkhongsap\article-query-ai\docs'

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Function to write dictionary content to file as Markdown
def write_dict_to_markdown(article, file):
    """Write the article content to a file in Markdown format."""
    # Write metadata at the top
    file.write(f"# {article['title']}\n\n")
    file.write(f"**ID:** {article['id']}\n")
    file.write(f"**Slug:** {article['slug']}\n")
    file.write(f"**Published At:** {article['publishedAt']}\n")
    file.write(f"**Locale:** {article['locale']}\n")
    file.write(f"**Excerpt:** {article['excerpt']}\n")
    file.write(f"**Category:** {article['category']}\n")
    file.write(f"**Tags:** {article['tags']}\n")
    file.write("\n")

    # Write highlights
    if article['highlights']:
        file.write(f"## Highlights\n")
        for highlight in article['highlights']:
            file.write(f"- {highlight}\n")
        file.write("\n")

    # Write content
    if article['content']:
        file.write(f"## Content\n\n")
        for paragraph in article['content']:
            file.write(f"{paragraph}\n\n")

    # Write credits
    if article['credit']:
        file.write(f"## Credit\n")
        for credit in article['credit']:
            file.write(f"- {credit}\n")
        file.write("\n")

    # Separator between articles
    file.write("\n" + "="*40 + "\n\n")

# Function to clean and flatten JSON data
def extract_metadata(json_data):
    result = []
    
    for item in json_data:
        attributes = item.get('attributes', {})
        
        # Extract and flatten categories
        categories = attributes.get('categories', {}).get('data', [])
        flattened_category = ', '.join(
            [f"{cat['attributes']['title']}, {cat['attributes']['slug']}" for cat in categories]
        )
        
        # Extract tags
        tags = attributes.get('tags', {}).get('data', [])
        tag_list = ', '.join([tag['attributes']['title'] for tag in tags])
        
        # Extract highlights
        highlights = attributes.get('highlights', [])
        highlight_list = [hl['content'] for hl in highlights]
        
        # Extract contents
        contents = attributes.get('contents', [])
        content_list = [cont['content'] for cont in contents]
        
        # Extract credit
        credits = attributes.get('credits', [])
        credit_list = [
            credit['credit']['data']['attributes']['collaborator']['data']['attributes']['name']
            for credit in credits if credit.get('credit') and credit['credit'].get('data')
        ]
        
        # Create the flattened dictionary
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

# Dictionary to hold articles grouped by their published date
articles_by_date = defaultdict(list)

# Convert JSON files to Markdown files and categorize articles by published date
for filename in os.listdir(input_dir):
    if filename.endswith('.json'):
        input_file = os.path.join(input_dir, filename)
        
        # Load JSON data
        with open(input_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        # Clean and flatten JSON data
        cleaned_data = extract_metadata(data)
        
        # Process each article in the cleaned JSON data
        for item in cleaned_data:
            # Extract the published date (assuming the format is '2024-08-28 17:27:00')
            published_at = item['publishedAt']
            published_date = published_at.split(' ')[0]  # Get only the date part (before the time)
            
            # Store the article in the dictionary under the correct date
            articles_by_date[published_date].append(item)

# Write each group of articles to a separate Markdown file named by the published date
for date, articles in articles_by_date.items():
    output_filename = f"article_{date}.md"
    output_path = os.path.join(output_dir, output_filename)
    
    with open(output_path, 'w', encoding='utf-8') as file:
        for article in articles:
            write_dict_to_markdown(article, file)

print(f"Articles have been successfully converted to Markdown files in {output_dir}, grouped by date.")
