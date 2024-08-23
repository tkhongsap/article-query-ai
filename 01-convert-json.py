import json
import os

# Define input and output directories
input_dir = r'D:\github-repo-tkhongsap\editor-in-chief\docs'
output_dir = r'D:\github-repo-tkhongsap\editor-in-chief\docs'

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

# Loop through all files in the input directory
for filename in os.listdir(input_dir):
    if filename.endswith('.json'):
        # Construct full file paths
        input_file = os.path.join(input_dir, filename)
        output_file = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}.txt")

        # Load the JSON data from the current file
        with open(input_file, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Create a text file in the output directory with the same name as the JSON file
        with open(output_file, 'w', encoding='utf-8') as file:
            for item in data:
                # Write each top-level dictionary item
                write_dict_to_file(item, file)
                
                # Add a separator between items for clarity
                file.write("="*50 + "\n\n")

        print(f"Data has been successfully written to {output_file}")
