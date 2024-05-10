# Import Dependencies
import os
import PyPDF2
import nltk
import re
from pdf2image import convert_from_path
import pytesseract


# PyPDF 2 Parser
def parser_pypdf(file_path):
    """
    Extract text from a PDF file using PyPDF2.

    Args:
    file_path (str): Path to the PDF file.

    Returns:
    str: Extracted text from the PDF.
    """
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

    # return text


# OCR PDF Reader.
def parser_ocr(pdf_path):
    """
    Extract text from a PDF file using OCR (Optical Character Recognition).

    Args:
    pdf_path (str): Path to the PDF file.

    Returns:
    str: Extracted text from the PDF.
    """
    images = convert_from_path(pdf_path)
    extracted_text = ""

    for image in images:
        text = pytesseract.image_to_string(image, lang='eng')
        extracted_text += text

    return extracted_text


# Function to split document into sentences
def get_sentences(text):
    """
    Tokenize text into sentences using nltk.

    Args:
    text (str): Input text.

    Returns:
    list: List of sentences.
    """
    sentences = nltk.sent_tokenize(text)
    return sentences


# Function to perform text formatting operations on a list of sentences
def sentence_formatter(sentences):
    """
    Format sentences.

    Args:
    sentences (list): List of sentences.

    Returns:
    list: Formatted sentences.
    """
    formatted_sentences = []

    for sentence in sentences:
        sentence = sentence.replace('\n', ' ')
        sentence = sentence.strip()
        sentence = re.sub(r'\s+', ' ', sentence)

        # Skip sentences with more than 85 words
        if len(sentence.split(" ")) > 85:
            continue

        # Join fragmented sentences
        if len(formatted_sentences) > 0 and not sentence[0].isupper():
            formatted_sentences[-1] += ' ' + sentence
        else:
            formatted_sentences.append(sentence)

    return formatted_sentences


def sentence_parser(pdf_file_path, print_sentences=False, num_sentences=5, parsing_method="pypdf"):
    """
    Parse sentences from a PDF file.

    Args:
    pdf_file_path (str): Path to the PDF file.
    print_sentences (bool, optional): Whether to print the extracted sentences. Defaults to False.
    num_sentences (int, optional): Number of sentences to print. Defaults to 5.
    parsing_method (str, optional): Parsing method to use ('pypdf' or 'ocr'). Defaults to "pypdf".

    Returns:
    list: List of formatted sentences.
    """
    # Check if file exists
    if not os.path.exists(pdf_file_path):
        print("Error: PDF file not found.")
        return

    # Extract text from the PDF based on the parsing method chosen
    if parsing_method == "pypdf":
        parsed_sentences = list(parser_pypdf(pdf_file_path))  # Convert generator to list
    elif parsing_method == "ocr":
        parsed_sentences = [(1, parser_ocr(pdf_file_path))]  # For OCR, assume all text belongs to the first page
    else:
        print("Error: Invalid parsing method specified.")
        return

    sentences_with_metadata = []
    for page_number, page_text in parsed_sentences:
        sentences = get_sentences(page_text)
        for sentence in sentences:
            sentences_with_metadata.append({
                'Page': page_number,
                'Filename': os.path.basename(pdf_file_path),
                'Sentence': sentence
            })

    # Summary of the number of sentences
    num_total_sentences = len(sentences_with_metadata)
    print("\nSummary:")
    print("Total number of sentences:", num_total_sentences)

    # Print the first n formatted sentences if required
    if print_sentences:
        if num_sentences > 0:
            for idx, item in enumerate(sentences_with_metadata[:num_sentences]):
                print('\n', f"Page: {item['Page']}, Filename: {item['Filename']}", item['Sentence'])
        else:
            for idx, item in enumerate(sentences_with_metadata):
                print('\n', f"Page: {item['Page']}, Filename: {item['Filename']}", item['Sentence'])

    return sentences_with_metadata
