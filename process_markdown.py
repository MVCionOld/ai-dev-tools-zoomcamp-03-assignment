import os
import json
from pathlib import Path

def traverse_and_prepare_data(source_dir="fastmcp-main", output_file="data/fastmcp-main-cache.json"):
    """
    Traverse the source directory, read .md and .mdx files, and save their content and filenames to a JSON file.

    Args:
        source_dir (str): Path to the source directory. Defaults to "fastmcp-main".
        output_file (str): Path to the output JSON file. Defaults to "data/fastmcp-main-cache.json".
    """
    data = []

    # Ensure the output directory exists
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Traverse the directory
    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.endswith(".md") or file.endswith(".mdx"):
                file_path = Path(root) / file
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    relative_path = file_path.relative_to(source_dir)  # Remove the first part of the path
                    data.append({"filename": str(relative_path), "content": content})
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")

    # Write the data to the output file
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Process markdown files and save their content to a JSON file.")
    parser.add_argument("--source", type=str, default="fastmcp-main", help="Path to the source directory.")
    parser.add_argument("--output", type=str, default="src/md_reader_tool/data/fastmcp-main-cache.json", help="Path to the output JSON file.")

    args = parser.parse_args()
    traverse_and_prepare_data(source_dir=args.source, output_file=args.output)