import io
import os
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.high_level import extractText

# Function to extract text from PDF
def extract_text_from_pdf(file_path):
    text = ''
    with open(file_path, 'rb') as file:
        manager = PDFResourceManager()
        retstr = io.StringIO()
        layout = LAParams(all_texts=True, char_margin=3.0, line_margin=1.0, word_margin=0.1)
        device = TextConverter(manager, retstr, laparams=layout)
        interpreter = PDFPageInterpreter(manager, device)

        for page in PDFPage.get_pages(file):
            interpreter.process_page(page)
            text += retstr.getvalue()

        device.close()
        retstr.close()
    return text

# Main function
def extract_text_from_pdfs(directory, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if filename.endswith(".pdf"):
                text = extract_text_from_pdf(file_path)
                file.write(text)

# Example usage
book_directory = r'C:\Users\john\OneDrive\Desktop\chingese\books'
output_tokens_file = "output_tokens.txt"
extract_text_from_pdfs(book_directory, output_tokens_file)
