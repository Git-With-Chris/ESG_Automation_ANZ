# THIS IS VERSION 1 of the MVP - Use only for experimental purposes

import torch
import pandas as pd

def mvp_sentence_similarity(pdf_sentences, tokenizer, model, query_sentence):
    """
    Calculate the similarity scores between a list of sentences and a query sentence using a pre-trained model.

    Args:
        pdf_sentences (list): List of sentences to compare.
        tokenizer: A tokenizer object compatible with the pre-trained model.
        model: A pre-trained model (e.g., T5) for computing sentence embeddings.
        query_sentence (str): The query sentence to compare against.

    Returns:
        pandas.DataFrame: DataFrame containing the similarity scores and sentences.
    """
    
    # Initialize an empty list to store dictionaries
    sentence_data = []

    # Tokenize Query Sentence
    query_ids = tokenizer(query_sentence, return_tensors='pt').input_ids
    
    # Generate Encodings for Query
    query = model(input_ids=query_ids)

    # Retrieve encodings for Query
    last_hidden_states_query = query.last_hidden_state
    
    # Apply mean pooling along the token dimension (dim=1)
    pooled_last_hidden_states_query = torch.mean(last_hidden_states_query, dim=1).unsqueeze(0)
    
    # Reshape pooled_last_hidden_states_query to match the shape of pooled_last_hidden_states
    pooled_last_hidden_states_query = pooled_last_hidden_states_query.view(1, -1)

    # Iterate over the sentences
    for idx, sentence in enumerate(pdf_sentences, start=1):
        # Tokenize Input sentence
        input_ids = tokenizer(sentence, return_tensors='pt').input_ids

        # Generate Encodings for Sentence
        outputs = model(input_ids=input_ids)

        # Retrieve encodings for sentence.
        last_hidden_states = outputs.last_hidden_state

        # Apply mean pooling along the token dimension (dim=1)
        pooled_last_hidden_states = torch.mean(last_hidden_states, dim=1).unsqueeze(0)
        
        # Compute dot product between the pooled representations
        similarity = torch.matmul(pooled_last_hidden_states, pooled_last_hidden_states_query.T)

        # Append a dictionary with score and sentence to the list
        sentence_data.append({'Sentence_ID': idx, 'Score': similarity.item(), 'Sentence': sentence})

    # Create DataFrame from the list of dictionaries
    df = pd.DataFrame(sentence_data)

    # Sort the DataFrame by the "Score" column in descending order
    df_sorted = df.sort_values(by='Score', ascending=False)

    return df_sorted
