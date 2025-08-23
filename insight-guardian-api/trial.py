
from app.services.llm_service import LLMService
from app.services.text_extraction_service import TextExtractionService

def test_cv_extraction(pdf_path: str):
	# Read PDF file as bytes
	with open(pdf_path, "rb") as f:
		file_bytes = f.read()
	# Extract text from PDF
	extracted_text = TextExtractionService.extract_text(file_bytes, "pdf")
	print("--- Extracted Text ---")
	print(extracted_text)
	# Pass extracted text to LLM for CV info extraction
	cv_info = LLMService.extract_cv_info(extracted_text)
	print("--- LLM Extracted CV Info ---")
	print(cv_info)

if __name__ == "__main__":
	# Change this path to your test PDF file
	test_pdf_path = "sample_cv.pdf"
	test_cv_extraction(test_pdf_path)
