from minsearch import Index


def search_index(query: str, index: Index, top_k: int = 5):
    """
    Search the index for the most relevant documents.

    Args:
        query (str): The search query.
        index (Index): The Index index.
        top_k (int): Number of top results to retrieve. Defaults to 5.

    Returns:
        list: List of top-k relevant documents.
    """
    return list(map(lambda data: data["filename"], index.search(query, {}, {}, num_results=top_k)))
