import os
import json
from pathlib import Path
from minsearch import Index


def gather_and_index_cache_files(data_dir="data") -> dict[str, Index]:
    """
    Gather all files ending with `-cache.json` in the data directory and create an index for each file.

    Args:
        data_dir (str): Path to the data directory. Defaults to "data".

    Returns:
        dict: A dictionary where the key is the first part of the JSON file before `-cache.json`
              and the value is the precomputed MinSearch index.
    """
    indices = {}

    # Traverse the data directory
    for root, _, files in os.walk(data_dir):
        for file in files:
            if file.endswith("-cache.json"):
                file_path = Path(root) / file
                key = file.replace("-cache.json", "")

                # Load the JSON cache
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)

                # Create a MinSearch index
                index = Index(text_fields=["content"], keyword_fields=["filename"])

                index.fit(data)

                # Store the index in the dictionary
                indices[key] = index

    return indices