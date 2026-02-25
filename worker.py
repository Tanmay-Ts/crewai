from celery_app import celery_app
from crewai import Crew, Process
from agents import financial_analyst, verifier
from task import analyze_financial_document, verify_financial_analysis
from database import SessionLocal, AnalysisResult

financial_crew = Crew(
    agents=[financial_analyst, verifier],
    tasks=[analyze_financial_document, verify_financial_analysis],
    process=Process.sequential,
    verbose=True,
)


@celery_app.task(name="worker.process_document")
def process_document(file_path: str, query: str):
    # Run Crew
    result = financial_crew.kickoff(
        inputs={
            "query": query,
            "path": file_path,
        }
    )

    # Save to DB
    db = SessionLocal()
    record = AnalysisResult(
        filename=file_path,
        query=query,
        result=str(result),
    )
    db.add(record)
    db.commit()
    db.close()

    return str(result)