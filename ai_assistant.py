
import time
import streamlit as st

from google import genai
from transactions import get_transactions

from datetime import date


MODEL_NAME = "gemini-3.6-flash"


def build_financial_context():
    """
    Retrieve actual financial transactions and
    calculate the current month's financial summary.
    """

    transactions = get_transactions()

    today = date.today()
    current_month = today.strftime("%Y-%m")

    monthly_transactions = [
        transaction
        for transaction in transactions
        if str(transaction["date"]).startswith(current_month)
    ]

    total_income = sum(
        transaction["amount"]
        for transaction in monthly_transactions
        if transaction["type"] == "Income"
    )

    total_expenses = sum(
        transaction["amount"]
        for transaction in monthly_transactions
        if transaction["type"] == "Expense"
    )

    balance = total_income - total_expenses

    category_expenses = {}

    for transaction in monthly_transactions:

        if transaction["type"] == "Expense":

            category = transaction["category"]

            category_expenses[category] = (
                category_expenses.get(category, 0)
                + transaction["amount"]
            )

    context = f"""
FINANCIAL SUMMARY FOR {today.strftime("%B %Y")}

Total Income: ₹{total_income:,.2f}

Total Expenses: ₹{total_expenses:,.2f}

Remaining Balance: ₹{balance:,.2f}

EXPENSE BREAKDOWN BY CATEGORY:
"""

    if category_expenses:

        for category, amount in sorted(
            category_expenses.items(),
            key=lambda item: item[1],
            reverse=True
        ):
            context += f"\n{category}: ₹{amount:,.2f}"

    else:
        context += "\nNo expenses recorded this month."

    context += "\n\nRECENT TRANSACTIONS:\n"

    for transaction in monthly_transactions[:10]:

        context += (
            f"\nDate: {transaction['date']}"
            f" | Title: {transaction['title']}"
            f" | Type: {transaction['type']}"
            f" | Category: {transaction['category']}"
            f" | Amount: ₹{transaction['amount']:,.2f}"
        )

    if not monthly_transactions:
        context += "\nNo transactions recorded this month."

    return context


def generate_financial_response(question, financial_context):
    """
    Generate a Gemini response with automatic retries.
    """

    if not question or not question.strip():
        return "Please enter a question."

    client = None

    try:

        api_key = st.secrets["GEMINI_API_KEY"]

        client = genai.Client(api_key=api_key)

        prompt = f"""
You are Finora AI, a helpful personal finance assistant.

Rules:
1. Answer using the supplied financial information.
2. Never invent financial figures or transactions.
3. Use Indian Rupees (₹).
4. Give practical budgeting suggestions.
5. Clearly mention when information is unavailable.
6. Do not claim to be a certified financial advisor.

FINANCIAL DATA:
{financial_context}

USER QUESTION:
{question}

Provide a clear, friendly and useful answer.
"""

        max_attempts = 3

        for attempt in range(max_attempts):

            try:

                response = client.models.generate_content(
                    model=MODEL_NAME,
                    contents=prompt
                )

                if response.text:
                    return response.text

                return "Gemini returned an empty response. Please try again."

            except Exception as error:

                error_message = str(error)

                is_temporary_error = (
                    "503" in error_message
                    or "UNAVAILABLE" in error_message
                    or "504" in error_message
                    or "429" in error_message
                )

                if not is_temporary_error:
                    return f"AI assistant error: {error_message}"

                if attempt == max_attempts - 1:

                    return (
                        "Finora AI is temporarily unavailable because "
                        "Gemini is experiencing high demand. "
                        "Please try again in a few minutes."
                    )

                wait_seconds = 5 * (2 ** attempt)

                time.sleep(wait_seconds)

    except Exception as error:

        return f"AI assistant error: {str(error)}"

    finally:

        if client is not None:
            client.close()
