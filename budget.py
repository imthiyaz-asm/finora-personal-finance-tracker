
import sqlite3
from decimal import Decimal, InvalidOperation
from datetime import date

from database import get_connection


# ==================================================
# 1. VALIDATE BUDGET DETAILS
# ==================================================

def validate_budget(category, amount, month):
    """
    Validate budget details before saving.
    """

    if not category or not category.strip():
        raise ValueError("Budget category cannot be empty.")

    try:
        decimal_amount = Decimal(str(amount))
    except InvalidOperation:
        raise ValueError("Enter a valid budget amount.")

    if not decimal_amount.is_finite() or decimal_amount <= 0:
        raise ValueError("Budget amount must be greater than zero.")

    amount_paise = decimal_amount * 100

    if amount_paise != amount_paise.to_integral_value():
        raise ValueError(
            "Budget amount cannot have more than two decimal places."
        )

    try:
        parsed_month = date.fromisoformat(str(month) + "-01")
    except ValueError:
        raise ValueError("Month must use YYYY-MM format.")

    if parsed_month.strftime("%Y-%m") != str(month):
        raise ValueError("Enter a valid month in YYYY-MM format.")

    return int(amount_paise)


# ==================================================
# 2. CREATE OR UPDATE A MONTHLY BUDGET
# ==================================================

def set_budget(category, amount, month):
    """
    Create a new monthly budget or update an existing one.

    A category can have only one budget per month.
    """

    amount_paise = validate_budget(
        category,
        amount,
        month
    )

    connection = get_connection()

    try:

        connection.execute(
            """
            INSERT INTO budgets
            (category, amount_paise, month)

            VALUES (?, ?, ?)

            ON CONFLICT(category, month)
            DO UPDATE SET
                amount_paise = excluded.amount_paise
            """,
            (
                category.strip(),
                amount_paise,
                str(month)
            )
        )

        connection.commit()

        return True

    finally:
        connection.close()


# ==================================================
# 3. GET ALL BUDGETS
# ==================================================

def get_budgets(month=None):
    """
    Retrieve all budgets or budgets for a particular month.
    """

    connection = get_connection()

    try:

        if month:

            rows = connection.execute(
                """
                SELECT id, category, amount_paise, month
                FROM budgets
                WHERE month = ?
                ORDER BY category
                """,
                (str(month),)
            ).fetchall()

        else:

            rows = connection.execute(
                """
                SELECT id, category, amount_paise, month
                FROM budgets
                ORDER BY month DESC, category
                """
            ).fetchall()

        budgets = []

        for row in rows:

            budget = dict(row)

            budget["amount"] = (
                budget.pop("amount_paise") / 100
            )

            budgets.append(budget)

        return budgets

    finally:
        connection.close()


# ==================================================
# 4. UPDATE AN EXISTING BUDGET
# ==================================================

def update_budget(budget_id, category, amount, month):
    """
    Update an existing budget using its unique ID.
    """

    amount_paise = validate_budget(
        category,
        amount,
        month
    )

    connection = get_connection()

    try:

        cursor = connection.execute(
            """
            UPDATE budgets

            SET
                category = ?,
                amount_paise = ?,
                month = ?

            WHERE id = ?
            """,
            (
                category.strip(),
                amount_paise,
                str(month),
                budget_id
            )
        )

        connection.commit()

        return cursor.rowcount > 0

    finally:
        connection.close()


# ==================================================
# 5. DELETE A BUDGET
# ==================================================

def delete_budget(budget_id):
    """
    Delete a budget using its unique ID.
    """

    connection = get_connection()

    try:

        cursor = connection.execute(
            """
            DELETE FROM budgets
            WHERE id = ?
            """,
            (budget_id,)
        )

        connection.commit()

        return cursor.rowcount > 0

    finally:
        connection.close()


# ==================================================
# 6. CALCULATE BUDGET USAGE
# ==================================================

def get_budget_status(month):
    """
    Calculate spending, remaining budget and usage percentage
    for every category in a selected month.
    """

    connection = get_connection()

    try:

        rows = connection.execute(
            """
            SELECT
                budgets.id,
                budgets.category,
                budgets.amount_paise,
                budgets.month,

                COALESCE(
                    SUM(transactions.amount_paise),
                    0
                ) AS spent_paise

            FROM budgets

            LEFT JOIN transactions

                ON budgets.category = transactions.category

                AND budgets.month = substr(
                    transactions.date, 1, 7
                )

                AND transactions.type = 'Expense'

            WHERE budgets.month = ?

            GROUP BY
                budgets.id,
                budgets.category,
                budgets.amount_paise,
                budgets.month

            ORDER BY budgets.category
            """,
            (str(month),)
        ).fetchall()

        budget_status = []

        for row in rows:

            budget_amount = row["amount_paise"] / 100

            spent_amount = row["spent_paise"] / 100

            remaining_amount = budget_amount - spent_amount

            usage_percentage = (
                spent_amount / budget_amount
            ) * 100

            budget_status.append({

                "id": row["id"],

                "category": row["category"],

                "month": row["month"],

                "budget": budget_amount,

                "spent": spent_amount,

                "remaining": remaining_amount,

                "usage_percentage": usage_percentage,

                "is_exceeded": spent_amount > budget_amount

            })

        return budget_status

    finally:
        connection.close()
