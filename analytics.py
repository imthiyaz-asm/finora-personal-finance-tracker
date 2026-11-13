
import pandas as pd
import plotly.express as px


# ==================================================
# 1. PREPARE FINANCIAL DATA
# ==================================================

def prepare_data(dataframe):
    """
    Prepare transaction data for financial analysis.
    """

    if dataframe.empty:
        return pd.DataFrame()

    df = dataframe.copy()

    df["date"] = pd.to_datetime(
        df["date"],
        errors="coerce"
    )

    df["amount"] = pd.to_numeric(
        df["amount"],
        errors="coerce"
    )

    df = df.dropna(
        subset=["date", "amount"]
    )

    df["month"] = df["date"].dt.to_period("M").astype(str)

    return df


# ==================================================
# 2. MONTHLY INCOME AND EXPENSE TREND
# ==================================================

def monthly_financial_trend(dataframe):
    """
    Calculate monthly income and expenses.
    """

    df = prepare_data(dataframe)

    if df.empty:
        return pd.DataFrame()

    monthly_data = (
        df.groupby(["month", "type"])["amount"]
        .sum()
        .reset_index()
    )

    monthly_data = monthly_data.pivot(
        index="month",
        columns="type",
        values="amount"
    ).fillna(0)

    for column in ["Income", "Expense"]:

        if column not in monthly_data.columns:
            monthly_data[column] = 0

    monthly_data = monthly_data[
        ["Income", "Expense"]
    ]

    monthly_data = monthly_data.reset_index()

    monthly_data = monthly_data.sort_values("month")

    return monthly_data


def create_monthly_trend_chart(dataframe):
    """
    Create an interactive monthly income and expense line chart.
    """

    monthly_data = monthly_financial_trend(dataframe)

    if monthly_data.empty:
        return None

    fig = px.line(
        monthly_data,
        x="month",
        y=["Income", "Expense"],
        markers=True,
        title="Monthly Income vs Expenses",
        labels={
            "month": "Month",
            "value": "Amount (₹)",
            "variable": "Transaction Type"
        }
    )

    fig.update_layout(
        template="plotly_white",
        hovermode="x unified",
        legend_title_text="",
        margin=dict(l=20, r=20, t=60, b=20)
    )

    fig.update_yaxes(
        tickprefix="₹",
        separatethousands=True
    )

    return fig


# ==================================================
# 3. EXPENSE CATEGORY BREAKDOWN
# ==================================================

def expense_category_summary(dataframe):
    """
    Calculate total expenses for each category.
    """

    df = prepare_data(dataframe)

    if df.empty:
        return pd.DataFrame(
            columns=["category", "amount"]
        )

    expenses = df[
        df["type"] == "Expense"
    ]

    if expenses.empty:
        return pd.DataFrame(
            columns=["category", "amount"]
        )

    category_data = (
        expenses.groupby("category")["amount"]
        .sum()
        .reset_index()
        .sort_values("amount", ascending=False)
    )

    return category_data


def create_expense_category_chart(dataframe):
    """
    Create an interactive expense category donut chart.
    """

    category_data = expense_category_summary(dataframe)

    if category_data.empty:
        return None

    fig = px.pie(
        category_data,
        names="category",
        values="amount",
        hole=0.55,
        title="Expense Category Breakdown"
    )

    fig.update_traces(
        textposition="inside",
        textinfo="percent",
        hovertemplate=(
            "<b>%{label}</b><br>"
            "Amount: ₹%{value:,.2f}<br>"
            "Share: %{percent}"
            "<extra></extra>"
        )
    )

    fig.update_layout(
        template="plotly_white",
        margin=dict(l=20, r=20, t=60, b=20),
        legend_title_text="Categories"
    )

    return fig


# ==================================================
# 4. MONTHLY INCOME VS EXPENSE BAR CHART
# ==================================================

def create_monthly_comparison_chart(dataframe):
    """
    Create a grouped bar chart comparing income and expenses.
    """

    monthly_data = monthly_financial_trend(dataframe)

    if monthly_data.empty:
        return None

    chart_data = monthly_data.melt(
        id_vars=["month"],
        value_vars=["Income", "Expense"],
        var_name="Transaction Type",
        value_name="Amount"
    )

    fig = px.bar(
        chart_data,
        x="month",
        y="Amount",
        color="Transaction Type",
        barmode="group",
        title="Monthly Financial Comparison",
        labels={
            "month": "Month",
            "Amount": "Amount (₹)"
        }
    )

    fig.update_layout(
        template="plotly_white",
        margin=dict(l=20, r=20, t=60, b=20),
        legend_title_text=""
    )

    fig.update_yaxes(
        tickprefix="₹",
        separatethousands=True
    )

    return fig


# ==================================================
# 5. TOP SPENDING CATEGORIES
# ==================================================

def create_top_spending_chart(dataframe):
    """
    Display categories with the highest expenses.
    """

    category_data = expense_category_summary(dataframe)

    if category_data.empty:
        return None

    category_data = category_data.head(5)

    fig = px.bar(
        category_data.sort_values(
            "amount",
            ascending=True
        ),
        x="amount",
        y="category",
        orientation="h",
        title="Top 5 Spending Categories",
        labels={
            "amount": "Amount (₹)",
            "category": "Category"
        }
    )

    fig.update_layout(
        template="plotly_white",
        showlegend=False,
        margin=dict(l=20, r=20, t=60, b=20)
    )

    fig.update_xaxes(
        tickprefix="₹",
        separatethousands=True
    )

    return fig
