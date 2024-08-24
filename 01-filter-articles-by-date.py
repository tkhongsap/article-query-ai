import os
import json
from datetime import datetime, timedelta

# Directory containing the JSON files
input_dir = r'D:\github-repo-tkhongsap\editor-in-chief\tmp'
output_dir = r'D:\github-repo-tkhongsap\editor-in-chief\tmp\docs-by-date' 

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Get the current date and calculate the date 7 days ago
current_date = datetime.utcnow()
seven_days_ago = current_date - timedelta(days=7)

# Function to check if the article is within the last 7 days
def is_within_last_7_days(published_at_str):
    published_at = datetime.strptime(published_at_str, "%Y-%m-%dT%H:%M:%S.%fZ")
    return published_at >= seven_days_ago

# Iterate through all JSON files in the input directory
for file_name in os.listdir(input_dir):
    if file_name.endswith(".json"):
        file_path = os.path.join(input_dir, file_name)
        
        # Load the JSON data from the file
        with open(file_path, "r", encoding="utf-8") as file:
            articles = json.load(file)
        
        # Filter the articles
        filtered_articles = []
        for article in articles:
            published_at = article["attributes"]["publishedAt"]
            
            # If the article is within the last 7 days, add it to the filtered list
            if is_within_last_7_days(published_at):
                filtered_articles.append(article)
            else:
                # Since the articles are in descending order, we can stop once we find one that's older than 7 days
                break
        
        # If there are filtered articles, save them to a new file
        if filtered_articles:
            # Generate a new file name
            output_file_name = f"article_date_{file_name.replace('.json', '')}.json"
            output_file_path = os.path.join(output_dir, output_file_name)
            
            # Save the filtered articles to the new JSON file
            with open(output_file_path, "w", encoding="utf-8") as output_file:
                json.dump(filtered_articles, output_file, ensure_ascii=False, indent=4)
            
            print(f"Saved {len(filtered_articles)} articles to {output_file_path}")
        else:
            print(f"No recent articles found in {file_name}, skipping...")

print("Processing complete.")
