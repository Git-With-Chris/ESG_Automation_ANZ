# Install Dependencies
# You can install the required dependencies using pip with the following command:
# pip install PyPDF2 nltk pdf2image pytesseract

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
            text += page.extract_text()
            
    return text

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

        if len(sentence.split(" ")) < 4:
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
        text = parser_pypdf(pdf_file_path)
    elif parsing_method == "ocr":
        text = parser_ocr(pdf_file_path)
    else:
        print("Error: Invalid parsing method specified.")
        return
    
    # Get sentences
    sentences = get_sentences(text)

    # Formatting Sentences
    formatted_sentences = sentence_formatter(sentences)

    # Summary of the number of sentences
    num_total_sentences = len(formatted_sentences)
    print("Report located in specified directory")
    print("\nSummary:")
    print("Total number of sentences:", num_total_sentences)

    # Print the first n formatted sentences if required
    if print_sentences:
        if num_sentences > 0:
            for sentence in formatted_sentences[:num_sentences]:
                print('\n', sentence)
        else:
            for sentence in formatted_sentences:
                print('\n', sentence)

    return formatted_sentences


# Example usage (Ensure to navigate to working directory):
# pdf_file_path = "../SampleReports/2023_Coles_Report.pdf"
# sentence_parser(pdf_file_path, print_sentences=True, num_sentences=10, parsing_method='pypdf')
