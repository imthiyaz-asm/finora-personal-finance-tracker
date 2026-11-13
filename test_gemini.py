
from ai_assistant import (
    build_financial_context,
    generate_financial_response
)

print("Fetching financial data from SQLite...")
print("--------------------------------")

# Fetch actual financial information
financial_context = build_financial_context()

print(financial_context)

print("\nConnecting to Gemini...")
print("--------------------------------")

# Ask Gemini a question
question = "Analyse my spending this month and suggest ways to save money."

answer = generate_financial_response(
    question,
    financial_context
)

print("\nFinora AI Response:")
print("--------------------------------")
print(answer)

print("--------------------------------")
