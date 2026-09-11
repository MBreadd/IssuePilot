from graph import issue_graph


print("=== IssuePilot ===")
print("Describe the software issue:\n")

issue_text = input("> ").strip()

if not issue_text:
    raise ValueError(
        "The issue cannot be empty."
    )


result = issue_graph.invoke(
    {
        "issue_text": issue_text
    }
)


print("\n--- IssuePilot Analysis ---")

print("Type:", result["type"])
print("Priority:", result["priority"])
print("Area:", result["area"])
print("Summary:", result["summary"])

print("\nChecklist:")

for task in result["checklist"]:
    print("-", task)


print("\n--- Specialized Analysis ---")
print(result["response"])

if "issue_draft" in result:

    print("\n--- GitHub Issue Draft ---")
    print(result["issue_draft"])