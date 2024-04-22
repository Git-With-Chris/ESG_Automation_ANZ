import PyPDF2
import nltk
import re
import pandas as pd
import pytesseract
import torch
from pdf2image import convert_from_path
import streamlit as st
from transformers import AutoTokenizer, T5EncoderModel


# Function to parse regular PDF files
def parse_regular_pdf(file_path):
    text = ""
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)

        for page_number in range(num_pages):
            page = reader.pages[page_number]
            page_text = page.extract_text()
            text += page_text
            # Yielding page number and text of each page
            yield page_number + 1, page_text

# Function to parse OCR-based PDF files
def parse_ocr_pdf(pdf_path):
    images = convert_from_path(pdf_path)
    extracted_text = ""

    for image in images:
        text = pytesseract.image_to_string(image, lang='eng')
        extracted_text += text

    return extracted_text

# Function to split document into sentences
def get_sentences(text):
    sentences = nltk.sent_tokenize(text)
    return sentences

# Function to perform text formatting operations on a list of sentences
def sentence_formatter(sentences):
    formatted_sentences = []

    for sentence in sentences:
        sentence = sentence.replace('\n', ' ')
        sentence = sentence.strip()
        sentence = re.sub(r'\s+', ' ', sentence)

        # Skip sentences with more than 80 words
        if len(sentence.split(" ")) > 85:
            continue

        # Join fragmented sentences
        if len(formatted_sentences) > 0 and not sentence[0].isupper():
            formatted_sentences[-1] += ' ' + sentence
        else:
            formatted_sentences.append(sentence)

    return formatted_sentences


# Function to parse PDF files based on type
def parse_pdf(file_paths, use_ocr):
    all_sentences = []
    all_page_numbers = []
    all_filenames = []

    for file_path in file_paths:
        sentences = []
        page_numbers = []
        if file_path.lower().endswith('.pdf'):
            if use_ocr:
                parsed_data = parse_ocr_pdf(file_path)
                sentences.extend(get_sentences(parsed_data))
                page_numbers.extend(
                    [-1] * len(get_sentences(parsed_data)))  # Assigning -1 for page numbers when using OCR
            else:
                for page_number, page_text in parse_regular_pdf(file_path):
                    sentences.extend(get_sentences(page_text))
                    page_numbers.extend([page_number] * len(get_sentences(page_text)))

        all_sentences.extend(sentences)
        all_page_numbers.extend(page_numbers)
        all_filenames.extend([file_path.split('/')[-1]] * len(sentences))

    return all_sentences, all_page_numbers, all_filenames

# Streamlit UI
def main():
    st.title("PDF Parser")
    st.write("Upload PDF files and choose parsing options")

    uploaded_files = st.file_uploader("Upload PDF files", accept_multiple_files=True)

    # Checkbox for parsing method
    use_ocr = st.checkbox("Use OCR")

    if uploaded_files:
        # Check file size
        for file in uploaded_files:
            if file.size > 100 * 1024 * 1024:  # Limit to 100 MB
                st.error(f"File '{file.name}' exceeds maximum allowed size (100 MB). Please upload a smaller file.")
                return

        # Get user input for query
        query_input = st.text_input("Enter your query:")

        # Validate query input
        if query_input:
            if not re.match(r'^[a-zA-Z\s?]+$', query_input):
                st.error("Query should only contain letters, spaces, and '?'")
                return

        parsed_sentences, page_numbers, filenames = parse_pdf([file.name for file in uploaded_files], use_ocr)
        st.write("Parsed Sentences:")
        for sentence, page_number, filename in zip(parsed_sentences, page_numbers, filenames):
            st.write(f"Sentence: {sentence}, Page Number: {page_number}, Filename: {filename}")

        # Initialize tokenizer and model
        tokenizer = AutoTokenizer.from_pretrained("t5-large", suppress_warnings=True)
        model = T5EncoderModel.from_pretrained("t5-large")

        # Initialize an empty list to store dictionaries
        sentence_data = []

        # Iterate over the sentences
        for idx, (sentence, page_number, filename) in enumerate(zip(parsed_sentences, page_numbers, filenames), start=1):
            # Tokenize Input sentence and query
            input_ids = tokenizer(sentence, return_tensors='pt').input_ids
            query_ids = tokenizer(query_input, return_tensors='pt').input_ids  # Use user input as query

            # Generate Encodings
            outputs = model(input_ids=input_ids)
            query = model(input_ids=query_ids)

            # Retrieve encodings for sentence and query.
            last_hidden_states = outputs.last_hidden_state
            last_hidden_states_query = query.last_hidden_state

            # Apply mean pooling along the token dimension (dim=1)
            pooled_last_hidden_states = torch.mean(last_hidden_states, dim=1).unsqueeze(0)
            pooled_last_hidden_states_query = torch.mean(last_hidden_states_query, dim=1).unsqueeze(0)

            # Reshape pooled_last_hidden_states_query to match the shape of pooled_last_hidden_states
            pooled_last_hidden_states_query = pooled_last_hidden_states_query.view(1, -1)

            # Compute dot product between the pooled representations
            similarity = torch.matmul(pooled_last_hidden_states, pooled_last_hidden_states_query.T)

            # Append a dictionary with score, sentence, page number, and filename to the list
            sentence_data.append({'Sentence_ID': idx, 'Score': similarity.item(), 'Sentence': sentence, 'Page_Number': page_number, 'Filename': filename})

        # Create DataFrame from the list of dictionaries
        df = pd.DataFrame(sentence_data)
        st.write(df)

        # Offer download link for the DataFrame in CSV format
        csv = df.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="parsed_sentences.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main()
