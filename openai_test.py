from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv(override=True)

api_key = os.getenv("OPENAI_API_KEY").strip()
org_id = os.getenv("OPENAI_ORG_ID").strip()
project_id = os.getenv("OPENAI_PROJECT_ID").strip()

client = OpenAI(
    api_key=api_key,
    organization=org_id,
    project=project_id,
)

response = client.responses.create(
    model="gpt-4.1-mini",
    input="Say API working"
)

print(response.output_text)