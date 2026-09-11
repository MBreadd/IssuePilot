import os

from dotenv import load_dotenv
from google import genai

from models import IssueAnalysis


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY was not found in the .env file."
    )


client = genai.Client(api_key=api_key)


def analyze_issue(issue_text: str) -> IssueAnalysis:

    prompt = f"""
    You are IssuePilot, an assistant for software development teams.

    Analyze the following software issue:

    {issue_text}

    Determine:
    - the issue type
    - its priority
    - the main software area involved
    - a concise summary
    - a practical developer checklist

    Base your analysis only on the information available.
    Do not invent technical details that are not supported by the issue.
    """

    interaction = client.interactions.create(
        model="gemini-3.8-flash",
        input=prompt,
        response_format={
            "type": "text",
            "mime_type": "application/json",
            "schema": IssueAnalysis.model_json_schema(),
        },
    )

    return IssueAnalysis.model_validate_json(
        interaction.output_text
    )


def generate_response(prompt: str) -> str:

    interaction = client.interactions.create(
        model="gemini-3.8-flash",
        input=prompt,
    )

    return interaction.output_text