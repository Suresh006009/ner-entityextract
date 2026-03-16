import nltk
import csv
import PyPDF2
import os
from collections import Counter

# Download required NLTK data (run once)
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')

def extract_text_from_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def extract_text_from_csv(file_path, text_column=0):
    """
    Assumes the CSV has a header. Uses the first column as text by default.
    Aggregates text from all rows.
    """
    texts = []
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)  # skip header
        for row in reader:
            if len(row) > text_column:
                texts.append(row[text_column])
    return "\n".join(texts)

def get_entities(text):
    """
    Run NLTK NER on the text and return a dictionary with counts per entity type.
    """
    sentences = nltk.sent_tokenize(text)
    entity_counts = {'PERSON': Counter(), 'ORGANIZATION': Counter(), 'LOCATION': Counter()}
    
    for sent in sentences:
        words = nltk.word_tokenize(sent)
        pos_tags = nltk.pos_tag(words)
        chunks = nltk.ne_chunk(pos_tags, binary=False)
        
        for chunk in chunks:
            if hasattr(chunk, 'label'):
                entity = ' '.join(c[0] for c in chunk)
                label = chunk.label()
                # Map NLTK labels to our three categories
                if label == 'PERSON':
                    entity_counts['PERSON'][entity] += 1
                elif label == 'ORGANIZATION':
                    entity_counts['ORGANIZATION'][entity] += 1
                elif label == 'GPE':
                    entity_counts['LOCATION'][entity] += 1
                # (Other labels like FACILITY, GSP etc. are ignored as per spec)
    
    return entity_counts