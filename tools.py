import os
import pdfplumber
from crewai.tools import BaseTool


class FinancialDocumentTool(BaseTool):
    name: str = "financial_document_reader"
    description: str = "Reads and extracts text from a financial PDF document."

    async def _run(self, path: str = "data/sample.pdf") -> str:
        if not os.path.exists(path):
            return f"ERROR: File not found at path: {path}"

        full_report = ""

        try:
            with pdfplumber.open(path) as pdf:
                for page in pdf.pages:
                    text = page.extract_text() or ""

                    while "\n\n" in text:
                        text = text.replace("\n\n", "\n")

                    full_report += text + "\n"

            if not full_report.strip():
                return "WARNING: No readable text found in the PDF."

            return full_report

        except Exception as e:
            return f"ERROR: Failed to read PDF. Details: {str(e)}"