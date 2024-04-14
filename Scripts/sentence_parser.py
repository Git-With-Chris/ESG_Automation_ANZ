# Import Dependencies
import PyPDF2
import nltk
import re

# PyPDF 2 Parser
def parser_pypdf(file_path):
    
    text = ""
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)
        
        for page_number in range(num_pages):
            page = reader.pages[page_number]
            text += page.extract_text()
            
    return text

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

