import pytesseract
from pdf2image import convert_from_path

# Replace with a path to one of your scanned quizzes
pdf_path = "C:/Users/ahmed/Downloads/Algo Final Exam (Solution) (Fall-2023).pdf"

# poppler_path is only needed if pdftoppm isn't in your PATH (which yours is!)
images = convert_from_path(pdf_path)

for i, image in enumerate(images):
    text = pytesseract.image_to_string(image, lang='eng+equ+Latn')
    print(f"--- Page {i+1} OCR Results ---")
    print(text[:500]) # Print first 500 chars