import PyPDF2

pdf_path = "test_resume.pdf"

with open(pdf_path, "rb") as file:
    reader = PyPDF2.PdfReader(file)

    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

print("======================================")
print("       EXTRACTED RESUME TEXT")
print("======================================")

print(text)

print("\n======================================")
print("PDF extraction completed successfully!")
print("======================================")