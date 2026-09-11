from typing import Literal

from pydantic import BaseModel, Field


class IssueAnalysis(BaseModel):

    type: Literal[
        "bug",
        "feature",
        "question",
        "other"
    ] = Field(
        description="Type of software issue"
    )

    priority: Literal[
        "low",
        "medium",
        "high",
        "critical"
    ] = Field(
        description="Priority of the issue"
    )

    area: str = Field(
        description="Main area of the software probably involved"
    )

    summary: str = Field(
        description="Short summary of the issue"
    )

    checklist: list[str] = Field(
        description="Short practical checklist for investigating or solving the issue"
    )