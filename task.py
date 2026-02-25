from crewai import Task
from agents import financial_analyst, verifier
from tools import FinancialDocumentTool

# =========================
# Task 1: Analyze
# =========================
analyze_financial_document = Task(
    description=(
    "Use the financial_document_reader tool to read the PDF at {path}.\n\n"
    "STRICT INSTRUCTIONS:\n"
    "- Base your answer ONLY on the document\n"
    "You MUST use the financial_document_reader tool before answering\n"
    "- Do NOT assume missing data\n"
    "- If information is missing, say 'Not found in document'\n"
    "- Quote exact numbers when available\n\n"
    "Then answer the user's query: {query}.\n\n"
    "Output must include:\n"
    "1. Key financial metrics (with values)\n"
    "2. Risks (document-backed only)\n"
    "3. Opportunities (document-backed only)\n"
    "4. Final summary"
),
    expected_output="Structured financial analysis report.",
    agent=financial_analyst,
    tools=[FinancialDocumentTool()],
    async_execution=False,
)
# =========================
# Task 2: Verify
# =========================
verify_financial_analysis = Task(
    description=(
        "Review the previous financial analysis for accuracy and logical consistency."
    ),
    expected_output="Verified and improved financial analysis.",
    agent=verifier,
    async_execution=False,
)