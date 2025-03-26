import google.generativeai as genai
import os
from dotenv import load_dotenv

class GenerativeAIParser:
    def __init__(self, api_key, debug=1):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")
        self.debug = debug

    def parse(self, prompt, request_options={}):
      cfg = genai.GenerationConfig()

      response = self.model.generate_content(prompt, request_options=request_options, generation_config=cfg)
      if self.debug:
          print(response.text)
          print(response.prompt_feedback)
      return response.text



def process_txt_files(path, parser):
  texts = []
  for filename in os.listdir(path):
    if filename.endswith(".txt"):
      file_path = os.path.join(path, filename)
      with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        prompt = "Resumi cada concepto ordenadamente en bullets este texto (y si el concepto trae ejemplos, listalos al final de cada uno)"
        print(f"Processing file: {filename}")
        texts.append(parser.parse(prompt + "\n\n" + content))
  return texts

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
path_to_txt_files = os.getenv("PATH_TO_TXT_FILES", "/home/ivan/Documents/idac/textos/analisis1/sintesis")
parser = GenerativeAIParser(api_key, debug=1)
texts = process_txt_files(path_to_txt_files, parser)
output_file = os.path.join(path_to_txt_files, "output_summary.md")
with open(output_file, 'w', encoding='utf-8') as file:
  for text in texts:
    file.write(text + "\n\n")
print(f"Summarized texts written to {output_file}")