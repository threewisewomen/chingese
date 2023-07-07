import io
import os
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
import jieba
from nltk.tokenize import sent_tokenize

# Function to extract text from PDF
def extract_text_from_pdf(file_path):
    text = ''
    with open(file_path, 'rb') as file:
        manager = PDFResourceManager()
        retstr = io.StringIO()
        layout = LAParams(all_texts=True)
        device = TextConverter(manager, retstr, laparams=layout)
        interpreter = PDFPageInterpreter(manager, device)

        for page in PDFPage.get_pages(file):
            interpreter.process_page(page)
            text += retstr.getvalue()


        device.close()
        retstr.close()
    segmented_text = chinese_word_segmentation(text)
    sentences = sentence_tokenization(segmented_text)
    append_tokens_to_file(file_path, sentences)
    return text

# Function to perform Chinese word segmentation
def chinese_word_segmentation(text):
    seg_text = ' '.join(jieba.cut(text))
    return seg_text

# Function to perform sentence tokenization
def sentence_tokenization(text):
    sentences = sent_tokenize(text)
    return sentences

# Function to append tokens to a file
def append_tokens_to_file(file_path, tokens):
    with open(file_path, 'a', encoding='utf-8') as file:
        for token in tokens:
            file.write(token + '\n')

# Main function
def preprocess_chinese_books(directory, output_file):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if filename.endswith(".pdf"):
            text = extract_text_from_pdf(file_path)
            segmented_text = chinese_word_segmentation(text)
            tokens = segmented_text.split()
            append_tokens_to_file(output_file, tokens)
        elif filename.endswith(".epub"):
            # Handle EPUB files in a similar manner
            pass
        else:
            continue

# Example usage
book_directory = r'C:\Users\john\OneDrive\Desktop\chingese\books'
output_tokens_file = "output_tokens.txt"
preprocess_chinese_books(book_directory, output_tokens_file)
