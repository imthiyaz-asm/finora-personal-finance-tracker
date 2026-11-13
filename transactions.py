
import sqlite3
from decimal import Decimal, InvalidOperation
from datetime import date

from database import get_connection


def validate_transaction(title, amount, transaction_type, category, transaction_date):
    """Validate transaction details before saving."""

    if not title.strip():
        raise ValueError("Transaction title cannot be empty.")

    if not category.strip():
        raise ValueError("Category cannot be empty.")

    if transaction_type not in ["Income", "Expense"]:
        raise ValueError("Type must be Income or Expense.")

    try:
        decimal_amount = Decimal(str(amount))
    except InvalidOperation:
        raise ValueError("Enter a valid transaction amount.")

    if not decimal_amount.is_finite() or decimal_amount <= 0:
        raise ValueError("Amount must be greater than zero.")

    paise_amount = decimal_amount * 100

    if paise_amount != paise_amount.to_integral_value():
        raise ValueError("Amount cannot have more than two decimal places.")

    try:
        date.fromisoformat(str(transaction_date))
    except ValueError:
        raise ValueError("Enter a valid date in YYYY-MM-DD format.")

    return int(paise_amount)


def add_transaction(title, amount, transaction_type, category, transaction_date, notes=""):
    """Insert a new income or expense transaction."""

    amount_paise = validate_transaction(
        title, amount, transaction_type, category, transaction_date
    )

    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            INSERT INTO transactions
            (title, amount_paise, type, category, date, notes)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                title.strip(),
                amount_paise,
                transaction_type,
                category.strip(),
                str(transaction_date),
                notes.strip()
            )
        )

        connection.commit()

        return cursor.lastrowid

    finally:
        connection.close()


def get_transactions():
    """Retrieve all transactions from the database."""

    connection = get_connection()

    try:
        rows = connection.execute(
            """
            SELECT
                id,
                title,
                amount_paise,
                type,
                category,
                date,
                notes,
                created_at
            FROM transactions
            ORDER BY date DESC, id DESC
            """
        ).fetchall()

        transactions = []

        for row in rows:
            transaction = dict(row)

            transaction["amount"] = (
                transaction.pop("amount_paise") / 100
            )

            transactions.append(transaction)

        return transactions

    finally:
        connection.close()


def update_transaction(
    transaction_id,
    title,
    amount,
    transaction_type,
    category,
    transaction_date,
    notes=""
):
    """Update an existing transaction."""

    amount_paise = validate_transaction(
        title, amount, transaction_type, category, transaction_date
    )

    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            UPDATE transactions
            SET
                title = ?,
                amount_paise = ?,
                type = ?,
                category = ?,
                date = ?,
                notes = ?
            WHERE id = ?
            """,
            (
                title.strip(),
                amount_paise,
                transaction_type,
                category.strip(),
                str(transaction_date),
                notes.strip(),
                transaction_id
            )
        )

        connection.commit()

        return cursor.rowcount > 0

    finally:
        connection.close()


def delete_transaction(transaction_id):
    """Delete a transaction using its unique ID."""

    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            DELETE FROM transactions
            WHERE id = ?
            """,
            (transaction_id,)
        )

        connection.commit()

        return cursor.rowcount > 0

    finally:
        connection.close()
