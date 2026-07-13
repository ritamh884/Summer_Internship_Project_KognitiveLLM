from ocr.ocr import extract_text
from extraction.payslip_extractor import extract_salary
import os

files = os.listdir("uploads")

file_path = os.path.join("uploads", files[0])

text = extract_text(file_path)

salary = extract_salary(text)

print("\n=========== EXTRACTED ===========\n")

for k, v in salary.items():
    print(f"{k:15} : {v}")