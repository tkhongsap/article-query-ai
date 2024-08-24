import os
import json
from datetime import datetime, timedelta
from collections import defaultdict

# Define input and output directories
input_dir = r'D:\github-repo-tkhongsap\editor-in-chief\tmp\docs-by-date'
output_dir = r'D:\github-repo-tkhongsap\editor-in-chief\docs'

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Function to write dictionary content to file with proper indentation
def write_dict_to_file(d, file, indent=0):
    """Recursively write dictionary content to file with proper indentation."""
    for key, value in d.items():
        if isinstance(value, dict):
            file.write(f"{' ' * indent}{key}:\n")
            write_dict_to_file(value, file, indent + 4)
        elif isinstance(value, list):
            file.write(f"{' ' * indent}{key}:\n")
            for item in value:
                if isinstance(item, dict):
                    write_dict_to_file(item, file, indent + 4)
                else:
                    file.write(f"{' ' * (indent + 4)}- {item}\n")
        else:
            file.write(f"{' ' * indent}{key}: {value}\n")

# Dictionary to hold articles grouped by their published date
articles_by_date = defaultdict(list)

# Convert JSON files to text files and categorize articles by published date
for filename in os.listdir(input_dir):
    if filename.endswith('.json'):
        input_file = os.path.join(input_dir, filename)
        
        # Load JSON data
        with open(input_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        # Process each article in the JSON file
        for item in data:
            # Extract the published date (assuming the format is '2024-08-24T08:51:06.360Z')
            published_at = item['attributes']['publishedAt']
            published_date = published_at.split('T')[0]  # Get only the date part
            
            # Store the article in the dictionary under the correct date
            articles_by_date[published_date].append(item)

# Get the current date and the last 7 days' dates
current_date = datetime.utcnow()
last_7_days = [(current_date - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7)]

# Write articles to files, one file per date within the last 7 days
for date in last_7_days:
    if date in articles_by_date:
        output_file = os.path.join(output_dir, f"article_{date}.txt")
        
        with open(output_file, 'w', encoding='utf-8') as file:
            for article in articles_by_date[date]:
                # Write the article to the file
                write_dict_to_file(article, file)
                
                # Add a separator between articles for clarity
                file.write("="*50 + "\n\n")
        
        print(f"Articles from {date} have been successfully written to {output_file}")

print("Processing complete.")
