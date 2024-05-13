import pandas as pd
import os
from sentence_transformers import SentenceTransformer, util

def compute_similarity_v2(model, query, pdf_sentences):
    """
    Computes similarity scores between a query and sentences retrieved from a PDF document.

    Args:
    - model: The model used for encoding embeddings.
    - query: The query for which similarity scores are computed.
    - pdf_sentences: List of sentences retrieved from a PDF document.

    Returns:
    - sorted_df: DataFrame containing sorted similarity scores.
    """
    # Create Embeddings for query
    query_embedding = model.encode(query)

    # Create Embeddings for retrieved sentences
    sentence_embedding = model.encode(pdf_sentences)

    # Compute similarity scores
    scores = util.cos_sim(query_embedding, sentence_embedding)[0]

    # Create a DataFrame
    df = pd.DataFrame({
        'Sentence_ID': range(1, len(pdf_sentences) + 1),
        'Sentence': pdf_sentences,
        'Score': scores.tolist()
    })

    # Sort DataFrame by similarity scores in descending order
    sorted_df = df.sort_values(by='Score', ascending=False)

    return sorted_df


def save_similarity_results(sorted_df, file_name='sorted_results.csv'):
    """
    Saves the sorted DataFrame to a CSV file in the user's downloads folder.

    Args:
    - sorted_df: DataFrame containing sorted similarity scores.
    - file_name: Name of the CSV file to be saved.
    """
    # Get the user's home directory
    home_directory = os.path.expanduser("~")

    # Depending on the operating system, navigate to the downloads folder
    if os.name == 'posix':  # Unix-based systems including macOS
        downloads_folder = os.path.join(home_directory, 'Downloads')
    elif os.name == 'nt':  # Windows
        downloads_folder = os.path.join(home_directory, 'Downloads')
    else:
        # Handle other operating systems if necessary
        raise NotImplementedError("Operating system not supported")

    # Specify the file path for the CSV file
    csv_file_path = os.path.join(downloads_folder, file_name)

    # Save the sorted DataFrame to the CSV file in the downloads folder
    sorted_df.to_csv(csv_file_path, index=False)
