
from datetime import date
from collections import defaultdict

from transactions import get_transactions
from budget import get_budget_status
from ai_assistant import generate_financial_response


def generate_smart_insights(month=None):
    """
    Analyse financial transactions and budgets
    and return structured financial insights.
    """

    if month is None:
        month = date.today().strftime("%Y-%m")

    transactions = get_transactions()

    current_transactions = [
        transaction
        for transaction in transactions
        if str(transaction["date"]).startswith(month)
    ]

    income = sum(
        transaction["amount"]
        for transaction in current_transactions
        if transaction["type"] == "Income"
    )

    expenses = sum(
        transaction["amount"]
        for transaction in current_transactions
        if transaction["type"] == "Expense"
    )

    balance = income - expenses

    savings_rate = (
        (balance / income) * 100
        if income > 0 else 0
    )

    # Expense category analysis
    category_totals = defaultdict(float)

    for transaction in current_transactions:

        if transaction["type"] == "Expense":
            category_totals[transaction["category"]] += (
                transaction["amount"]
            )

    highest_category = None

    if category_totals:
        highest_category = max(
            category_totals,
            key=category_totals.get
        )

    # Budget analysis
    budgets = get_budget_status(month)

    budget_warnings = []

    for budget in budgets:

        if budget["is_exceeded"]:

            budget_warnings.append({
                "category": budget["category"],
                "budget": budget["budget"],
                "spent": budget["spent"],
                "remaining": budget["remaining"],
                "status": "Exceeded"
            })

        elif budget["usage_percentage"] >= 80:

            budget_warnings.append({
                "category": budget["category"],
                "budget": budget["budget"],
                "spent": budget["spent"],
                "remaining": budget["remaining"],
                "status": "Near Limit"
            })

    # Previous month comparison
    current_year, current_month = map(int, month.split("-"))

    if current_month == 1:
        previous_month = f"{current_year - 1}-12"
    else:
        previous_month = (
            f"{current_year}-{current_month - 1:02d}"
        )

    previous_transactions = [
        transaction
        for transaction in transactions
        if str(transaction["date"]).startswith(previous_month)
    ]

    previous_expenses = sum(
        transaction["amount"]
        for transaction in previous_transactions
        if transaction["type"] == "Expense"
    )

    expense_change = expenses - previous_expenses

    if previous_expenses > 0:
        expense_change_percentage = (
            expense_change / previous_expenses
        ) * 100
    else:
        expense_change_percentage = None

    return {
        "month": month,
        "income": income,
        "expenses": expenses,
        "balance": balance,
        "savings_rate": savings_rate,
        "category_totals": dict(category_totals),
        "highest_category": highest_category,
        "budget_warnings": budget_warnings,
        "previous_month_expenses": previous_expenses,
        "expense_change": expense_change,
        "expense_change_percentage": expense_change_percentage
    }


def generate_ai_recommendations(insights):
    """
    Use Gemini to explain calculated insights
    and generate practical financial recommendations.
    """

    category_details = insights["category_totals"]

    if category_details:
        category_summary = "\n".join(
            f"{category}: ₹{amount:,.2f}"
            for category, amount in sorted(
                category_details.items(),
                key=lambda item: item[1],
                reverse=True
            )
        )
    else:
        category_summary = "No expense records available."

    if insights["budget_warnings"]:
        budget_summary = "\n".join(
            f"{item['category']}: {item['status']}. "
            f"Spent ₹{item['spent']:,.2f} of "
            f"₹{item['budget']:,.2f}."
            for item in insights["budget_warnings"]
        )
    else:
        budget_summary = "No budget warnings were detected."

    if insights["expense_change_percentage"] is None:
        comparison_summary = (
            "Previous-month expense data is unavailable. "
            "Do not make a month-over-month comparison."
        )
    else:
        comparison_summary = (
            f"Previous-month expenses: "
            f"₹{insights['previous_month_expenses']:,.2f}\n"
            f"Expense change: "
            f"{insights['expense_change_percentage']:+.2f}%"
        )

    financial_context = f"""
MONTH: {insights['month']}

INCOME: ₹{insights['income']:,.2f}
EXPENSES: ₹{insights['expenses']:,.2f}
REMAINING BALANCE: ₹{insights['balance']:,.2f}
SAVINGS RATE: {insights['savings_rate']:.2f}%

EXPENSE CATEGORY BREAKDOWN:
{category_summary}

HIGHEST SPENDING CATEGORY:
{insights['highest_category'] or 'No expense data available'}

BUDGET WARNINGS:
{budget_summary}

MONTHLY COMPARISON:
{comparison_summary}
"""

    question = """
Analyse these calculated financial insights.

Please provide:

1. A brief financial health overview.
2. An explanation of the highest spending category.
3. Budget warnings, if any.
4. Practical suggestions to improve savings.
5. Three specific actions the user can take.

Important rules:
- Use only the supplied figures.
- Do not invent transactions or financial amounts.
- Do not claim that a budget is exceeded unless the data says so.
- Do not compare months when previous-month data is unavailable.
- Clearly distinguish facts from suggestions.
- Use Indian Rupees (₹).
- Keep the answer clear and practical.
- Do not claim to be a certified financial advisor.
"""

    return generate_financial_response(
        question,
        financial_context
    )

def detect_unusual_spending(month=None):
    """
    Detect unusual category spending by comparing
    the selected month with the previous three months.
    """

    if month is None:
        month = date.today().strftime("%Y-%m")

    transactions = get_transactions()

    year, month_number = map(int, month.split("-"))

    current_month_start = date(year, month_number, 1)

    # Generate the previous three calendar months.
    previous_months = []

    for offset in range(1, 4):

        previous_year = year
        previous_month_number = month_number - offset

        while previous_month_number <= 0:
            previous_month_number += 12
            previous_year -= 1

        previous_months.append(
            f"{previous_year}-{previous_month_number:02d}"
        )

    current_expenses = defaultdict(float)
    historical_expenses = defaultdict(list)

    # Collect historical expenses by category.
    for transaction in transactions:

        transaction_month = str(transaction["date"])[:7]

        if transaction["type"] != "Expense":
            continue

        category = transaction["category"]
        amount = float(transaction["amount"])

        if transaction_month == month:

            current_expenses[category] += amount

        elif transaction_month in previous_months:

            historical_expenses[category].append(
                (transaction_month, amount)
            )

    unusual_spending = []

    for category, current_amount in current_expenses.items():

        # Calculate spending separately for each historical month.
        monthly_totals = {
            previous_month: 0.0
            for previous_month in previous_months
        }

        for historical_month, amount in historical_expenses.get(
            category, []
        ):
            monthly_totals[historical_month] += amount

        # Require actual records in all three historical months.
        months_with_records = sum(
            1
            for previous_month in previous_months
            if any(
                historical_month == previous_month
                for historical_month, amount
                in historical_expenses.get(category, [])
            )
        )

        if months_with_records < 3:
            continue

        historical_average = (
            sum(monthly_totals.values()) / 3
        )

        increase = current_amount - historical_average

        if (
            current_amount > historical_average * 1.5
            and increase >= 1000
        ):

            unusual_spending.append({
                "category": category,
                "current_spending": current_amount,
                "historical_average": historical_average,
                "increase": increase,
                "increase_percentage": (
                    increase / historical_average
                ) * 100
            })

    return sorted(
        unusual_spending,
        key=lambda item: item["increase"],
        reverse=True
    )
