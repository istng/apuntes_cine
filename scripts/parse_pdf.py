from llama_cloud_services import LlamaParse
import logging
import os
from dotenv import load_dotenv


class LlamaParser:
    def __init__(self, api_key, debug=0):
        if not api_key:
            raise ValueError("API key not found in environment variables")
            
        self.parser = LlamaParse(api_key=api_key)
        self.debug = debug

    def parse_document(self, document, extra_info=None) -> str:
        try:
            # Load and parse the PDF file
            documents = self.parser.load_data(document, extra_info=extra_info)
            
            if self.debug:
                # Print the parsed content with additional debug information
                for i, doc in enumerate(documents):
                    print(f"Text: {doc.text}")  # Print the full text content
                    print("\n" + "="*80 + "\n")
            
            # Combine all document texts into a single string
            full_text = ""
            for doc in documents:
                full_text += doc.text + "\n"
                
            return full_text
            
        except Exception as e:
            logging.error(f"Unexpected error parsing document: {e}")
            return ""

def parse_pdfs_in_path(path, parser):
  for root, _, files in os.walk(path):
    for file in files:
      if file.endswith(".pdf"):
        file_path = os.path.join(root, file)
        print(f"Parsing: {file_path}")
        parsed_text = parser.parse_document(file_path)
        output_file = os.path.splitext(file_path)[0] + ".txt"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(parsed_text)
        print(parsed_text)

if __name__ == "__main__":
  load_dotenv()
  api_key = os.getenv("LLAMA_API_KEY")
  path_to_pdfs = "/home/ivan/Documents/idac/textos/analisis1/sintesis"
  parser = LlamaParser(api_key=api_key, debug=1)
  parse_pdfs_in_path(path_to_pdfs, parser)