from typing import Literal, TypedDict

from langgraph.graph import StateGraph, START, END

from analyzer import analyze_issue, generate_response

from issue_tools import build_github_issue_draft

# ---------------------------------
# 1. Estado compartido del grafo
# ---------------------------------

class IssueState(TypedDict, total=False):
    issue_text: str
    issue_draft: str

    type: Literal[
        "bug",
        "feature",
        "question",
        "other"
    ]

    priority: Literal[
        "low",
        "medium",
        "high",
        "critical"
    ]

    area: str
    summary: str
    checklist: list[str]

    response: str


# ---------------------------------
# 2. Nodo: analizar issue
# ---------------------------------

def analyze_node(state: IssueState):

    analysis = analyze_issue(
        state["issue_text"]
    )

    return {
        "type": analysis.type,
        "priority": analysis.priority,
        "area": analysis.area,
        "summary": analysis.summary,
        "checklist": analysis.checklist,
    }


# ---------------------------------
# 3. Router
# ---------------------------------

def route_issue(
    state: IssueState
) -> Literal[
    "bug",
    "feature",
    "question",
    "other"
]:

    return state["type"]


# ---------------------------------
# 4. Nodos especializados
# ---------------------------------

def bug_node(state: IssueState):

    prompt = f"""
    You are a software debugging assistant.

    Analyze this bug:

    Issue:
    {state["issue_text"]}

    Area:
    {state["area"]}

    Priority:
    {state["priority"]}

    Provide:

    1. A short technical diagnosis.
    2. Three possible causes.
    3. The recommended next debugging step.

    Clearly indicate that possible causes are hypotheses,
    not confirmed facts.

    Keep the response concise and practical.
    """

    response = generate_response(prompt)

    return {
        "response": response
    }


def feature_node(state: IssueState):

    prompt = f"""
    You are a software planning assistant.

    Analyze this feature request:

    Feature:
    {state["issue_text"]}

    Area:
    {state["area"]}

    Provide:

    1. The goal of the feature.
    2. A short implementation plan.
    3. Three acceptance criteria.

    Keep the response concise and practical.
    """

    response = generate_response(prompt)

    return {
        "response": response
    }


def question_node(state: IssueState):

    prompt = f"""
    You are a software development assistant.

    Answer the following technical question:

    {state["issue_text"]}

    Give:

    1. A direct answer.
    2. A brief explanation.
    3. A recommended next step.

    If there is not enough information,
    explicitly say what information is missing.

    Keep the response concise.
    """

    response = generate_response(prompt)

    return {
        "response": response
    }


def other_node(state: IssueState):

    return {
        "response": (
            "IssuePilot could not clearly classify this request. "
            "Please provide more technical context."
        )
    }

def draft_node(state: IssueState):

    draft = build_github_issue_draft.invoke(
        {
            "summary": state["summary"],
            "issue_type": state["type"],
            "priority": state["priority"],
            "area": state["area"],
            "checklist": state["checklist"],
            "specialized_analysis": state["response"],
        }
    )

    return {
        "issue_draft": draft
    }

# ---------------------------------
# 5. Construir grafo
# ---------------------------------

builder = StateGraph(IssueState)


# Nodos
builder.add_node(
    "analyze",
    analyze_node
)

builder.add_node(
    "bug",
    bug_node
)

builder.add_node(
    "feature",
    feature_node
)

builder.add_node(
    "question",
    question_node
)

builder.add_node(
    "other",
    other_node
)


# ---------------------------------
# 6. Edges
# ---------------------------------

builder.add_edge(
    START,
    "analyze"
)


builder.add_conditional_edges(
    "analyze",
    route_issue,
    {
        "bug": "bug",
        "feature": "feature",
        "question": "question",
        "other": "other",
    }
)


builder.add_edge(
    "bug",
    "draft"
)

builder.add_edge(
    "feature",
    "draft"
)

builder.add_edge(
    "draft",
    END
)

builder.add_edge(
    "question",
    END
)

builder.add_edge(
    "other",
    END
)


# ---------------------------------
# 7. Compilar
# ---------------------------------

issue_graph = builder.compile()