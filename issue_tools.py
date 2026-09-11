import os

import requests
from dotenv import load_dotenv
from langchain.tools import tool


load_dotenv()

@tool
def build_github_issue_draft(
    summary: str,
    issue_type: str,
    priority: str,
    area: str,
    checklist: list[str],
    specialized_analysis: str,
) -> str:
    """Build a Markdown draft for a GitHub Issue from an analyzed software issue."""

    checklist_markdown = "\n".join(
        f"- [ ] {task}"
        for task in checklist
    )

    return f"""
## Summary

{summary}

## Metadata

- Type: `{issue_type}`
- Priority: `{priority}`
- Area: `{area}`

## Checklist

{checklist_markdown}

## IssuePilot Analysis

{specialized_analysis}
""".strip()

@tool
def create_github_issue(
    title: str,
    body: str,
) -> str:
    """Create a new issue in the configured GitHub repository."""

    token = os.getenv("GITHUB_TOKEN")
    owner = os.getenv("GITHUB_OWNER")
    repo = os.getenv("GITHUB_REPO")

    if not token:
        raise ValueError(
            "GITHUB_TOKEN was not found in .env"
        )

    if not owner:
        raise ValueError(
            "GITHUB_OWNER was not found in .env"
        )

    if not repo:
        raise ValueError(
            "GITHUB_REPO was not found in .env"
        )

    url = (
        f"https://api.github.com/repos/"
        f"{owner}/{repo}/issues"
    )

    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2026-03-10",
    }

    payload = {
        "title": title,
        "body": body,
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=20,
    )

    if response.status_code != 201:
        raise RuntimeError(
            f"GitHub API error "
            f"{response.status_code}: "
            f"{response.text}"
        )

    data = response.json()

    return data["html_url"]