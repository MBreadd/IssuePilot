from langchain.tools import tool


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