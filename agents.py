from dotenv import load_dotenv
import os
from crewai import Agent, LLM
from tools import FinancialDocumentTool

# =========================
# Load environment
# =========================
load_dotenv(override=True)

# Ensure API key exists (fail fast)
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY not found in environment")

# =========================
# CrewAI LLM wrapper
# =========================
llm = LLM(
    model="gpt-4o-mini",  # modern fast model
    temperature=0.2
)

# =========================
# Financial Analyst Agent
# =========================
financial_analyst = Agent(
    role="Senior Financial Analyst",
    goal=(
        "Analyze the provided financial document and answer the user's query accurately: {query}."
    ),
    backstory=(
        "You are an experienced financial analyst specializing in corporate financial statements."
    ),
    tools=[FinancialDocumentTool()],
    llm=llm,
    verbose=True,
    allow_delegation=False,
)

# =========================
# Verifier Agent
# =========================
verifier = Agent(
    role="Financial Report Verifier",
    goal="Verify the financial analysis for accuracy and consistency.",
    backstory="You are a meticulous financial auditor.",
    llm=llm,
    verbose=True,
    allow_delegation=False,
)