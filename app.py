
import streamlit as st
import pandas as pd
import plotly.express as px
from database import create_tables
from datetime import date
from textwrap import dedent

from transactions import (
    get_transactions,
    add_transaction,
    update_transaction,
    delete_transaction
)

from analytics import (
    create_monthly_trend_chart,
    create_expense_category_chart,
    create_monthly_comparison_chart,
    create_top_spending_chart
)

from budget import (
    set_budget,
    get_budgets,
    update_budget,
    delete_budget,
    get_budget_status
)

from ai_assistant import (
    build_financial_context,
    generate_financial_response
)

from smart_insights import (
    generate_smart_insights,
    generate_ai_recommendations,
    detect_unusual_spending
)

# Initialize database tables
create_tables()
# ==========================================================
# 1. PAGE CONFIGURATION
# ==========================================================


# ==========================================================
# 2. FINORA PREMIUM UI DESIGN
# ==========================================================

st.markdown("""
<style>

/* =========================================
   GLOBAL THEME
========================================= */

:root {
    color-scheme: light;
    --primary: #087F5B;
    --primary-dark: #066649;
    --primary-light: #E7F5EF;
    --background: #F5F7F6;
    --surface: #FFFFFF;
    --text: #172B24;
    --muted: #687A72;
    --border: #E4EBE7;
    --income: #07865B;
    --expense: #D9485F;
}

.stApp {
    background: var(--background);
    color: var(--text);
    font-family: "Segoe UI", Arial, sans-serif;
}

[data-testid="stAppViewContainer"] {
    background: var(--background);
}

.block-container {
    max-width: 1500px;
    padding-top: 2.2rem;
    padding-bottom: 3rem;
    padding-left: 3rem;
    padding-right: 3rem;
}

[data-testid="stHeader"] {
    background: rgba(245, 247, 246, 0.95);
}

/* =========================================
   TYPOGRAPHY — FIX TEXT VISIBILITY
========================================= */

html, body, [class*="css"] {
    color: var(--text);
}

.stApp p,
.stApp label,
.stApp span,
.stApp li,
.stApp small {
    color: #34483F;
}

.stApp h1 {
    color: #142D23 !important;
    font-size: 2rem !important;
    font-weight: 750 !important;
    letter-spacing: -0.7px;
}

.stApp h2 {
    color: #19382B !important;
    font-weight: 700 !important;
}

.stApp h3, .stApp h4 {
    color: #244638 !important;
    font-weight: 650 !important;
}

.stMarkdown {
    color: #34483F;
}

.stCaption,
[data-testid="stCaptionContainer"] {
    color: #718078 !important;
}

/* =========================================
   SIDEBAR
========================================= */

[data-testid="stSidebar"] {
    background: #FFFFFF;
    border-right: 1px solid #E4EBE7;
}

[data-testid="stSidebar"] > div:first-child {
    padding: 1.5rem 1rem;
}

[data-testid="stSidebar"] h2 {
    color: var(--primary) !important;
    font-size: 2rem !important;
    font-weight: 800 !important;
}

[data-testid="stSidebar"] p {
    color: #74847C !important;
}

[data-testid="stSidebar"] h3 {
    color: #263D32 !important;
    font-size: 0.95rem !important;
}

[data-testid="stSidebar"] .stButton {
    margin-bottom: 8px;
}

[data-testid="stSidebar"] .stButton button {
    width: 100%;
    min-height: 47px;
    border-radius: 10px;
    text-align: left;
    justify-content: flex-start;
    padding: 10px 15px;
    font-size: 14px;
    font-weight: 600;
    transition: all 0.2s ease;
}

[data-testid="stSidebar"] button[kind="secondary"] {
    background: transparent !important;
    color: #53665C !important;
    border: 1px solid transparent !important;
}

[data-testid="stSidebar"] button[kind="secondary"]:hover {
    background: #F0F7F3 !important;
    color: var(--primary) !important;
    border-color: #DCEDE4 !important;
}

[data-testid="stSidebar"] button[kind="primary"] {
    background: #E7F5EF !important;
    color: #087F5B !important;
    border: 1px solid #CBE9DA !important;
    border-left: 4px solid #087F5B !important;
}

/* =========================================
   METRIC CARDS
========================================= */

.metric-card {
    background: #FFFFFF;
    border: 1px solid #E5ECE8;
    border-radius: 16px;
    padding: 23px;
    min-height: 145px;
    box-shadow: 0 4px 14px rgba(25, 55, 40, 0.035);
    transition: all 0.2s ease;
}

.metric-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 22px rgba(25, 55, 40, 0.07);
}

.metric-label {
    font-size: 13px;
    color: #687A72 !important;
    font-weight: 600;
    margin-bottom: 14px;
}

.metric-value {
    font-size: 27px;
    font-weight: 750;
    color: #18382A !important;
    letter-spacing: -0.5px;
}

.metric-caption {
    font-size: 12px;
    color: #829087 !important;
    margin-top: 10px;
}

.income-value {
    color: #07865B !important;
}

.expense-value {
    color: #D9485F !important;
}

.section-heading {
    font-size: 19px;
    font-weight: 750;
    color: #19382B;
    margin-top: 20px;
    margin-bottom: 15px;
}

/* =========================================
   BUTTONS
========================================= */

.stButton > button,
.stFormSubmitButton > button,
.stDownloadButton > button {
    background: #087F5B !important;
    color: #FFFFFF !important;
    border: 1px solid #087F5B !important;
    border-radius: 9px !important;
    min-height: 42px;
    font-weight: 650 !important;
    transition: all 0.2s ease;
}

.stButton > button p,
.stFormSubmitButton > button p,
.stDownloadButton > button p {
    color: #FFFFFF !important;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover,
.stDownloadButton > button:hover {
    background: #066649 !important;
    border-color: #066649 !important;
    box-shadow: 0 4px 12px rgba(8, 127, 91, 0.18);
}

/* =========================================
   FORMS AND INPUT FIELDS
========================================= */

[data-testid="stForm"] {
    background: #FFFFFF;
    border: 1px solid #E5ECE8;
    border-radius: 15px;
    padding: 24px;
}

[data-baseweb="input"] input,
[data-baseweb="textarea"] textarea {
    background: #FFFFFF !important;
    color: #172B24 !important;
    border: 1px solid #D8E3DD !important;
    border-radius: 9px !important;
    caret-color: #087F5B !important;
}

[data-baseweb="input"] input::placeholder,
[data-baseweb="textarea"] textarea::placeholder {
    color: #98A69E !important;
}

[data-baseweb="input"] > div,
[data-baseweb="textarea"] > div {
    background: #FFFFFF !important;
    border-color: #D8E3DD !important;
}

[data-baseweb="select"] > div {
    background: #FFFFFF !important;
    color: #172B24 !important;
    border-color: #D8E3DD !important;
    border-radius: 9px !important;
}

[data-baseweb="select"] span {
    color: #263D32 !important;
}

[data-baseweb="popover"] {
    background: #FFFFFF !important;
}

[data-baseweb="menu"] {
    background: #FFFFFF !important;
}

[data-baseweb="menu"] li {
    color: #263D32 !important;
}

/* Date picker */

[data-testid="stDateInput"] input {
    background: #FFFFFF !important;
    color: #172B24 !important;
}

/* =========================================
   EXPANDERS
========================================= */

[data-testid="stExpander"] {
    background: #FFFFFF;
    border: 1px solid #E3EBE6;
    border-radius: 12px;
    overflow: hidden;
}

[data-testid="stExpander"] summary {
    color: #244638 !important;
    font-weight: 650;
}

[data-testid="stExpander"] summary:hover {
    color: #087F5B !important;
}

/* =========================================
   TABLES
========================================= */

[data-testid="stDataFrame"] {
    background: #FFFFFF;
    border: 1px solid #E4EBE7;
    border-radius: 12px;
    overflow: hidden;
}

[data-testid="stTable"] {
    background: #FFFFFF;
    border-radius: 12px;
}

[data-testid="stDataFrame"] * {
    color: #263D32;
}

/* =========================================
   CHARTS
========================================= */

[data-testid="stPlotlyChart"] {
    background: #FFFFFF;
    border: 1px solid #E5ECE8;
    border-radius: 15px;
    padding: 10px;
    box-shadow: 0 3px 12px rgba(25, 55, 40, 0.025);
}

/* =========================================
   CHAT INTERFACE
========================================= */

[data-testid="stChatMessage"] {
    background: #FFFFFF !important;
    border: 1px solid #E4EBE7 !important;
    border-radius: 14px !important;
    padding: 15px !important;
    margin-bottom: 12px !important;
}

[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] span {
    color: #263D32 !important;
}

[data-testid="stChatInput"] {
    background: #FFFFFF !important;
    border: 1px solid #DCE7E0 !important;
    border-radius: 13px !important;
    box-shadow: 0 4px 15px rgba(20, 50, 35, 0.05);
}

[data-testid="stChatInput"] textarea {
    background: #FFFFFF !important;
    color: #172B24 !important;
    caret-color: #087F5B !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: #84938A !important;
}

/* =========================================
   ALERTS AND STATUS MESSAGES
========================================= */

[data-testid="stAlert"] {
    border-radius: 11px;
}

[data-testid="stAlert"] p {
    color: #263D32 !important;
}

[data-testid="stNotification"] {
    border-radius: 10px;
}

/* =========================================
   CHECKBOXES AND RADIO BUTTONS
========================================= */

[data-testid="stCheckbox"] label,
[data-testid="stRadio"] label {
    color: #34483F !important;
}

/* =========================================
   EMPTY STATES
========================================= */

.empty-state {
    background: #FFFFFF;
    border: 1px solid #E4EBE7;
    border-radius: 16px;
    padding: 40px 25px;
    text-align: center;
}

.empty-state h3 {
    color: #087F5B !important;
}

.empty-state p {
    color: #718078 !important;
}

/* =========================================
   DIVIDERS AND FOOTER
========================================= */

hr {
    border-color: #E3EBE6 !important;
}

[data-testid="stCaptionContainer"] {
    color: #78877F !important;
}

/* =========================================
   SCROLLBAR
========================================= */

::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: #F5F7F6;
}

::-webkit-scrollbar-thumb {
    background: #CBD8D0;
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: #91A99A;
}

/* =========================================
   RESPONSIVE LAYOUT
========================================= */

@media (max-width: 768px) {
    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }

    .metric-value {
        font-size: 21px;
    }
}

/* =========================================
   FINORA UI FINAL OVERRIDE
========================================= */

/* Force light appearance */
:root {
    color-scheme: light !important;
}

html, body, .stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="stMainBlockContainer"] {
    background: #F6F8F7 !important;
    color: #20352B !important;
}

/* Main content spacing */
.block-container {
    max-width: 1450px !important;
    padding: 2rem 2.5rem 3rem !important;
}

/* All headings */
.stApp h1,
.stApp h2,
.stApp h3,
.stApp h4 {
    color: #183B2C !important;
    font-weight: 700 !important;
}

.stApp p,
.stApp label,
.stApp li,
.stApp [data-testid="stMarkdownContainer"] {
    color: #34483E !important;
}

/* SIDEBAR */
[data-testid="stSidebar"] {
    background: #FFFFFF !important;
    border-right: 1px solid #E3EAE5 !important;
}

[data-testid="stSidebar"] * {
    color: #34483E;
}

[data-testid="stSidebar"] h2 {
    color: #087F5B !important;
}

[data-testid="stSidebar"] button {
    background: transparent !important;
    color: #34483E !important;
    border: 1px solid transparent !important;
    border-radius: 10px !important;
    text-align: left !important;
    justify-content: flex-start !important;
}

[data-testid="stSidebar"] button p,
[data-testid="stSidebar"] button span {
    color: #34483E !important;
}

[data-testid="stSidebar"] button:hover {
    background: #EFF7F2 !important;
    border-color: #DCECE2 !important;
}

[data-testid="stSidebar"] button[kind="primary"] {
    background: #E5F4EB !important;
    border: 1px solid #C8E6D3 !important;
    border-left: 4px solid #087F5B !important;
}

[data-testid="stSidebar"] button[kind="primary"] p,
[data-testid="stSidebar"] button[kind="primary"] span {
    color: #087F5B !important;
    font-weight: 700 !important;
}

/* MAIN BUTTONS */
[data-testid="stMain"] .stButton button,
[data-testid="stMain"] .stFormSubmitButton button,
[data-testid="stMain"] .stDownloadButton button {
    background: #087F5B !important;
    color: #FFFFFF !important;
    border: 1px solid #087F5B !important;
    border-radius: 9px !important;
    font-weight: 600 !important;
    min-height: 42px;
}

[data-testid="stMain"] .stButton button p,
[data-testid="stMain"] .stFormSubmitButton button p,
[data-testid="stMain"] .stDownloadButton button p {
    color: #FFFFFF !important;
}

[data-testid="stMain"] .stButton button:hover,
[data-testid="stMain"] .stFormSubmitButton button:hover {
    background: #066649 !important;
}

/* METRIC CARDS */
.metric-card {
    background: #FFFFFF !important;
    border: 1px solid #E3EBE6 !important;
    border-radius: 15px !important;
    padding: 23px !important;
    min-height: 140px;
    box-shadow: 0 3px 12px rgba(20, 50, 35, 0.04) !important;
}

.metric-label {
    color: #687A70 !important;
}

.metric-value {
    color: #183B2C !important;
    font-size: 26px !important;
    font-weight: 750 !important;
}

.metric-caption {
    color: #75867C !important;
}

.income-value {
    color: #07865B !important;
}

.expense-value {
    color: #D9485F !important;
}

/* INPUTS */
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input,
[data-testid="stDateInput"] input,
[data-testid="stTextArea"] textarea,
[data-testid="stChatInput"] textarea {
    background: #FFFFFF !important;
    color: #20352B !important;
    -webkit-text-fill-color: #20352B !important;
    caret-color: #087F5B !important;
    border-color: #D7E3DC !important;
}

[data-testid="stTextInput"] input::placeholder,
[data-testid="stChatInput"] textarea::placeholder {
    color: #829187 !important;
    -webkit-text-fill-color: #829187 !important;
}

/* SELECT BOXES */
[data-baseweb="select"] > div {
    background: #FFFFFF !important;
    color: #20352B !important;
    border-color: #D7E3DC !important;
}

[data-baseweb="select"] span {
    color: #20352B !important;
}

[data-baseweb="popover"],
[data-baseweb="menu"] {
    background: #FFFFFF !important;
}

[data-baseweb="menu"] li {
    color: #20352B !important;
}

/* FORMS AND EXPANDERS */
[data-testid="stForm"],
[data-testid="stExpander"] {
    background: #FFFFFF !important;
    border: 1px solid #E3EBE6 !important;
    border-radius: 13px !important;
}

[data-testid="stExpander"] summary,
[data-testid="stExpander"] summary span {
    color: #244638 !important;
}

/* TABLES */
[data-testid="stDataFrame"],
[data-testid="stTable"] {
    background: #FFFFFF !important;
    border: 1px solid #E3EBE6 !important;
    border-radius: 12px !important;
}

/* CHARTS */
[data-testid="stPlotlyChart"] {
    background: #FFFFFF !important;
    border: 1px solid #E3EBE6 !important;
    border-radius: 14px !important;
    padding: 10px !important;
}

/* CHAT AREA — REMOVE BLACK BACKGROUND */
[data-testid="stBottom"],
[data-testid="stBottom"] > div,
[data-testid="stChatInput"],
[data-testid="stChatInput"] > div {
    background: #F6F8F7 !important;
}

[data-testid="stChatInput"] {
    border: 1px solid #DCE7E0 !important;
    border-radius: 13px !important;
    box-shadow: 0 3px 12px rgba(20, 50, 35, 0.06) !important;
}

[data-testid="stChatMessage"] {
    background: #FFFFFF !important;
    border: 1px solid #E3EBE6 !important;
    border-radius: 13px !important;
    padding: 15px !important;
}

[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] span {
    color: #263D32 !important;
}

/* ALERTS */
[data-testid="stAlert"] {
    border-radius: 11px !important;
}

[data-testid="stAlert"] p {
    color: #263D32 !important;
}

/* DIVIDERS */
hr {
    border-color: #E3EBE6 !important;
}

/* RESPONSIVE */
@media (max-width: 768px) {
    .block-container {
        padding: 1.2rem 1rem 2rem !important;
    }

    .metric-value {
        font-size: 21px !important;
    }
}


</style>
""", unsafe_allow_html=True)



# ==========================================================
# 3. SESSION STATE
# ==========================================================

if "current_page" not in st.session_state:
    st.session_state.current_page = "Overview"

if "confirm_delete_transaction" not in st.session_state:
    st.session_state.confirm_delete_transaction = False

if "ai_chat_history" not in st.session_state:
    st.session_state.ai_chat_history = []


# ==========================================================
# 4. NAVIGATION
# ==========================================================

navigation_items = [
    ("Overview", "▦"),
    ("Transaction Management", "↔"),
    ("Financial Analytics", "▥"),
    ("Budget Planning", "◎"),
    ("AI Financial Assistant", "✦"),
    ("Smart Insights", "✧")
]


# ==========================================================
# 5. SIDEBAR
# ==========================================================

with st.sidebar:

    st.markdown(
        "<h2 style='color:#247A57;'>Finora.</h2>",
        unsafe_allow_html=True
    )

    st.caption("Personal Finance Management")

    st.divider()

    st.markdown("### Navigation")

    for page, symbol in navigation_items:

        is_active = (
            st.session_state.current_page == page
        )

        button_type = "primary" if is_active else "secondary"

        if st.button(
            f"{symbol}   {page}",
            key=f"nav_{page}",
            type=button_type,
            use_container_width=True
        ):

            st.session_state.current_page = page
            st.rerun()

    st.divider()

    st.caption("FINORA PERSONAL FINANCE")
    st.caption("Version 1.0")


# ==========================================================
# 6. HELPER FUNCTIONS
# ==========================================================

def format_currency(amount):
    return f"₹{amount:,.2f}"


def display_metric(title, value, caption, css_class=""):

    card_html = dedent(f"""
        <div class="metric-card">
            <div class="metric-label">{title}</div>
            <div class="metric-value {css_class}">{value}</div>
            <div class="metric-caption">{caption}</div>
        </div>
    """)

    st.markdown(
        card_html,
        unsafe_allow_html=True
    )


def load_financial_data():

    transactions = get_transactions()

    if not transactions:
        return pd.DataFrame()

    dataframe = pd.DataFrame(transactions)

    dataframe["date"] = pd.to_datetime(
        dataframe["date"],
        errors="coerce"
    )

    dataframe["amount"] = pd.to_numeric(
        dataframe["amount"],
        errors="coerce"
    )

    dataframe = dataframe.dropna(
        subset=["date", "amount"]
    )

    return dataframe


def show_transaction_table(dataframe):

    if dataframe.empty:

        st.info("No transactions found.")

        return

    display_df = dataframe.copy()

    display_df["date"] = display_df["date"].dt.strftime(
        "%d %b %Y"
    )

    display_df["amount"] = display_df.apply(
        lambda row: (
            f"+ {format_currency(row['amount'])}"
            if row["type"] == "Income"
            else f"- {format_currency(row['amount'])}"
        ),
        axis=1
    )

    display_df = display_df[
        ["title", "category", "type", "date", "amount"]
    ]

    display_df.columns = [
        "Description",
        "Category",
        "Type",
        "Date",
        "Amount"
    ]

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        height=380
    )

# ==========================================================
# 7. LOAD FINANCIAL DATA
# ==========================================================

df = load_financial_data()

today = date.today()
current_month = today.strftime("%Y-%m")


# ==========================================================
# 8. FINANCIAL CALCULATIONS
# ==========================================================

if not df.empty:

    df["month"] = df["date"].dt.strftime("%Y-%m")

    total_income = df.loc[
        df["type"] == "Income", "amount"
    ].sum()

    total_expenses = df.loc[
        df["type"] == "Expense", "amount"
    ].sum()

    total_balance = total_income - total_expenses

    monthly_df = df[
        df["month"] == current_month
    ]

    monthly_income = monthly_df.loc[
        monthly_df["type"] == "Income", "amount"
    ].sum()

    monthly_expenses = monthly_df.loc[
        monthly_df["type"] == "Expense", "amount"
    ].sum()

    monthly_balance = monthly_income - monthly_expenses

    transaction_count = len(df)

else:

    total_income = 0
    total_expenses = 0
    total_balance = 0

    monthly_income = 0
    monthly_expenses = 0
    monthly_balance = 0

    transaction_count = 0


# ==========================================================
# 9. ADD TRANSACTION FORM
# ==========================================================

def show_add_transaction_form():

    with st.expander(
        "＋ Add a New Transaction",
        expanded=False
    ):

        st.markdown("### Transaction Details")

        with st.form("add_transaction_form"):

            col1, col2 = st.columns(2)

            with col1:

                title = st.text_input(
                    "Transaction Title",
                    placeholder="Example: Monthly Salary"
                )

                amount = st.number_input(
                    "Amount (₹)",
                    min_value=0.01,
                    value=100.00,
                    step=100.0,
                    format="%.2f"
                )

                transaction_type = st.selectbox(
                    "Transaction Type",
                    ["Expense", "Income"]
                )

            with col2:

                categories = [
                    "Food",
                    "Travel",
                    "Shopping",
                    "Bills",
                    "Salary",
                    "Healthcare",
                    "Education",
                    "Entertainment",
                    "Rent",
                    "Investment",
                    "Other"
                ]

                category = st.selectbox(
                    "Category",
                    categories
                )

                transaction_date = st.date_input(
                    "Transaction Date",
                    value=today,
                    max_value=today
                )

                notes = st.text_input(
                    "Notes",
                    placeholder="Optional description"
                )

            submitted = st.form_submit_button(
                "Save Transaction",
                use_container_width=True
            )

            if submitted:

                try:

                    if not title.strip():
                        raise ValueError("Enter a transaction title.")

                    add_transaction(
                        title=title,
                        amount=amount,
                        transaction_type=transaction_type,
                        category=category,
                        transaction_date=transaction_date.isoformat(),
                        notes=notes
                    )

                    st.success("Transaction added successfully!")

                    st.rerun()

                except Exception as error:

                    st.error(str(error))


# ==========================================================
# 10. FINANCIAL ANALYTICS PAGE
# ==========================================================

def show_financial_analytics():

    st.title("Financial Analytics")

    st.write(
        "Understand your financial habits through interactive charts."
    )

    st.divider()

    if df.empty:

        st.info("Add transactions to generate financial analytics.")

        return

    income_df = df[df["type"] == "Income"]
    expense_df = df[df["type"] == "Expense"]

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Income",
        format_currency(income_df["amount"].sum())
    )

    col2.metric(
        "Total Expenses",
        format_currency(expense_df["amount"].sum())
    )

    col3.metric(
        "Transactions",
        len(df)
    )

    st.write("")

    st.markdown("### Monthly Income vs Expenses")

    monthly_chart = create_monthly_trend_chart(df)

    if monthly_chart is not None:

        st.plotly_chart(
            monthly_chart,
            use_container_width=True
        )

    left_col, right_col = st.columns(2)

    with left_col:

        st.markdown("### Expense Category Breakdown")

        category_chart = create_expense_category_chart(df)

        if category_chart is not None:

            st.plotly_chart(
                category_chart,
                use_container_width=True
            )

        else:

            st.info("No expense transactions available.")

    with right_col:

        st.markdown("### Top Spending Categories")

        top_chart = create_top_spending_chart(df)

        if top_chart is not None:

            st.plotly_chart(
                top_chart,
                use_container_width=True
            )

        else:

            st.info("No expense transactions available.")

    st.markdown("### Monthly Financial Comparison")

    comparison_chart = create_monthly_comparison_chart(df)

    if comparison_chart is not None:

        st.plotly_chart(
            comparison_chart,
            use_container_width=True
        )


# ==========================================================
# 11. TRANSACTION MANAGEMENT PAGE
# ==========================================================

def show_transaction_management():

    st.title("Transaction Management")

    st.write(
        "Add, edit, delete and manage your financial transactions."
    )

    st.divider()

    show_add_transaction_form()

    st.markdown("### Transaction History")

    if df.empty:

        st.info("No transactions available. Add your first transaction.")

        return

    # ------------------------------------------------------
    # FILTERS
    # ------------------------------------------------------

    st.markdown("#### Filter Transactions")

    col1, col2, col3 = st.columns(3)

    with col1:

        transaction_filter = st.selectbox(
            "Transaction Type",
            ["All", "Income", "Expense"],
            key="transaction_type_filter"
        )

    with col2:

        category_options = [
            "All"
        ] + sorted(
            df["category"].dropna().unique().tolist()
        )

        category_filter = st.selectbox(
            "Category",
            category_options,
            key="transaction_category_filter"
        )

    with col3:

        date_filter = st.selectbox(
            "Date Range",
            [
                "All Dates",
                "This Month",
                "Last 30 Days",
                "Custom Range"
            ],
            key="transaction_date_filter"
        )

    filtered_df = df.copy()

    if transaction_filter != "All":

        filtered_df = filtered_df[
            filtered_df["type"] == transaction_filter
        ]

    if category_filter != "All":

        filtered_df = filtered_df[
            filtered_df["category"] == category_filter
        ]

    if date_filter == "This Month":

        filtered_df = filtered_df[
            filtered_df["date"].dt.strftime("%Y-%m") == current_month
        ]

    elif date_filter == "Last 30 Days":

        start_date = pd.Timestamp(today) - pd.Timedelta(days=30)

        filtered_df = filtered_df[
            filtered_df["date"] >= start_date
        ]

    elif date_filter == "Custom Range":

        date_col1, date_col2 = st.columns(2)

        with date_col1:

            start_date = st.date_input(
                "Start Date",
                value=date(today.year, today.month, 1),
                key="filter_start_date"
            )

        with date_col2:

            end_date = st.date_input(
                "End Date",
                value=today,
                key="filter_end_date"
            )

        if start_date > end_date:

            st.error("Start date cannot be after end date.")

            return

        filtered_df = filtered_df[
            (filtered_df["date"].dt.date >= start_date)
            &
            (filtered_df["date"].dt.date <= end_date)
        ]

    # ------------------------------------------------------
    # FILTER SUMMARY
    # ------------------------------------------------------

    st.divider()

    income_total = filtered_df.loc[
        filtered_df["type"] == "Income", "amount"
    ].sum()

    expense_total = filtered_df.loc[
        filtered_df["type"] == "Expense", "amount"
    ].sum()

    summary_col1, summary_col2, summary_col3 = st.columns(3)

    summary_col1.metric(
        "Transactions",
        len(filtered_df)
    )

    summary_col2.metric(
        "Income",
        format_currency(income_total)
    )

    summary_col3.metric(
        "Expenses",
        format_currency(expense_total)
    )

    # ------------------------------------------------------
    # TRANSACTION TABLE
    # ------------------------------------------------------

    st.markdown("### Transaction Records")

    show_transaction_table(filtered_df)

    # ------------------------------------------------------
    # CSV DOWNLOAD
    # ------------------------------------------------------

    st.markdown("### Export Transactions")

    if not filtered_df.empty:

        export_df = filtered_df[
            [
                "id",
                "title",
                "amount",
                "type",
                "category",
                "date",
                "notes"
            ]
        ].copy()

        export_df["date"] = (
            export_df["date"].dt.strftime("%Y-%m-%d")
        )

        export_df.columns = [
            "Transaction ID",
            "Title",
            "Amount (INR)",
            "Type",
            "Category",
            "Date",
            "Notes"
        ]

        csv_data = export_df.to_csv(
            index=False
        ).encode("utf-8-sig")

        st.download_button(
            label="Download CSV Report",
            data=csv_data,
            file_name=f"finora_transactions_{today}.csv",
            mime="text/csv",
            use_container_width=True
        )

    else:

        st.info("No records available to export.")

    # ------------------------------------------------------
    # EDIT TRANSACTION
    # ------------------------------------------------------

    st.divider()

    st.markdown("### Edit Transaction")

    transaction_options = {
        f"#{int(row['id'])} | {row['title']} | "
        f"{format_currency(row['amount'])}": row
        for _, row in filtered_df.iterrows()
    }

    if not transaction_options:

        st.info("No transactions available to edit.")

    else:

        selected_label = st.selectbox(
            "Select a transaction to edit",
            list(transaction_options.keys()),
            key="edit_transaction_selector"
        )

        selected_transaction = transaction_options[selected_label]

        with st.expander("Edit Selected Transaction"):

            with st.form("edit_transaction_form"):

                edit_col1, edit_col2 = st.columns(2)

                with edit_col1:

                    edit_title = st.text_input(
                        "Transaction Title",
                        value=selected_transaction["title"]
                    )

                    edit_amount = st.number_input(
                        "Amount (₹)",
                        min_value=0.01,
                        value=float(selected_transaction["amount"]),
                        step=100.0,
                        format="%.2f"
                    )

                    edit_type = st.selectbox(
                        "Transaction Type",
                        ["Expense", "Income"],
                        index=(
                            0 if selected_transaction["type"] == "Expense"
                            else 1
                        )
                    )

                with edit_col2:

                    edit_categories = [
                        "Food",
                        "Travel",
                        "Shopping",
                        "Bills",
                        "Salary",
                        "Healthcare",
                        "Education",
                        "Entertainment",
                        "Rent",
                        "Investment",
                        "Other"
                    ]

                    existing_category = selected_transaction["category"]

                    if existing_category not in edit_categories:
                        edit_categories.append(existing_category)

                    edit_category = st.selectbox(
                        "Category",
                        edit_categories,
                        index=edit_categories.index(existing_category)
                    )

                    edit_date = st.date_input(
                        "Transaction Date",
                        value=selected_transaction["date"].date(),
                        max_value=today
                    )

                    edit_notes = st.text_input(
                        "Notes",
                        value=(
                            ""
                            if pd.isna(selected_transaction["notes"])
                            else str(selected_transaction["notes"])
                        )
                    )

                update_button = st.form_submit_button(
                    "Save Changes",
                    use_container_width=True
                )

                if update_button:

                    try:

                        if not edit_title.strip():
                            raise ValueError("Enter a transaction title.")

                        success = update_transaction(
                            int(selected_transaction["id"]),
                            edit_title,
                            edit_amount,
                            edit_type,
                            edit_category,
                            edit_date.isoformat(),
                            edit_notes
                        )

                        if success:

                            st.success("Transaction updated successfully!")

                            st.rerun()

                        else:

                            st.error("Transaction could not be found.")

                    except Exception as error:

                        st.error(str(error))

    # ------------------------------------------------------
    # DELETE TRANSACTION
    # ------------------------------------------------------

    st.divider()

    st.markdown("### Delete Transaction")

    delete_options = {
        f"#{int(row['id'])} | {row['title']} | "
        f"{format_currency(row['amount'])}": row
        for _, row in filtered_df.iterrows()
    }

    if delete_options:

        delete_label = st.selectbox(
            "Select a transaction to delete",
            list(delete_options.keys()),
            key="delete_transaction_selector"
        )

        selected_delete = delete_options[delete_label]

        confirm_delete = st.checkbox(
            "I confirm that I want to delete this transaction.",
            key="confirm_delete_checkbox"
        )

        if st.button(
            "Delete Transaction",
            type="primary",
            key="delete_transaction_button",
            disabled=not confirm_delete
        ):

            try:

                success = delete_transaction(
                    int(selected_delete["id"])
                )

                if success:

                    st.success("Transaction deleted successfully!")

                    st.rerun()

                else:

                    st.error("Transaction could not be found.")

            except Exception as error:

                st.error(str(error))

# ==========================================================
# 12. BUDGET PLANNING PAGE
# ==========================================================

def show_budget_planning():

    st.title("Budget Planning")

    st.write(
        "Set monthly spending limits and monitor your expenses."
    )

    st.divider()

    # ------------------------------------------------------
    # CREATE OR UPDATE BUDGET
    # ------------------------------------------------------

    st.markdown("### Set Monthly Budget")

    budget_categories = [
        "Food",
        "Travel",
        "Shopping",
        "Bills",
        "Healthcare",
        "Education",
        "Entertainment",
        "Rent",
        "Investment",
        "Other"
    ]

    with st.form("budget_form"):

        col1, col2 = st.columns(2)

        with col1:

            budget_category = st.selectbox(
                "Category",
                budget_categories
            )

            budget_amount = st.number_input(
                "Monthly Budget Amount (₹)",
                min_value=1.0,
                value=5000.0,
                step=500.0
            )

        with col2:

            budget_month = st.date_input(
                "Select Month",
                value=date(today.year, today.month, 1)
            )

            budget_month_string = budget_month.strftime("%Y-%m")

            st.caption(
                f"Budget period: {budget_month.strftime('%B %Y')}"
            )

        save_budget = st.form_submit_button(
            "Save Budget",
            use_container_width=True
        )

        if save_budget:

            try:

                existing_budgets = get_budgets(budget_month_string)

                existing_budget = next(
                    (
                        budget for budget in existing_budgets
                        if budget["category"] == budget_category
                    ),
                    None
                )

                if existing_budget:

                    update_budget(
                        existing_budget["id"],
                        budget_amount
                    )

                    st.success("Budget updated successfully!")

                else:

                    set_budget(
                        budget_category,
                        budget_amount,
                        budget_month_string
                    )

                    st.success("Budget created successfully!")

                st.rerun()

            except Exception as error:

                st.error(str(error))

    st.divider()

    # ------------------------------------------------------
    # SELECT BUDGET MONTH
    # ------------------------------------------------------

    st.markdown("### Monthly Budget Overview")

    available_months = sorted(
        df["month"].dropna().unique().tolist(),
        reverse=True
    ) if not df.empty else []

    if current_month not in available_months:
        available_months.insert(0, current_month)

    selected_budget_month = st.selectbox(
        "View Budget For",
        available_months,
        key="budget_view_month"
    )

    selected_budgets = get_budgets(selected_budget_month)

    budget_status = get_budget_status(selected_budget_month)

    if not selected_budgets:

        st.info(
            "No budgets have been created for this month. "
            "Use the form above to create your first budget."
        )

    else:

        # --------------------------------------------------
        # BUDGET SUMMARY
        # --------------------------------------------------

        total_budget = sum(
            float(budget["amount"])
            for budget in selected_budgets
        )

        total_spent = sum(
            float(item["spent"])
            for item in budget_status
        )

        remaining_budget = total_budget - total_spent

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Total Budget",
            format_currency(total_budget)
        )

        col2.metric(
            "Total Spent",
            format_currency(total_spent)
        )

        col3.metric(
            "Remaining",
            format_currency(remaining_budget)
        )

        st.divider()

        # --------------------------------------------------
        # CATEGORY-WISE BUDGET STATUS
        # --------------------------------------------------

        st.markdown("### Category-wise Budget Status")

        for item in budget_status:

            category = item["category"]

            budget_amount_value = float(item["budget"])

            spent = float(item["spent"])

            remaining = budget_amount_value - spent

            progress = (
                spent / budget_amount_value
                if budget_amount_value > 0
                else 0
            )

            progress = min(progress, 1.0)

            st.markdown(f"**{category}**")

            col1, col2 = st.columns([3, 1])

            with col1:

                st.progress(progress)

            with col2:

                percentage = (
                    spent / budget_amount_value * 100
                    if budget_amount_value > 0
                    else 0
                )

                st.write(f"{percentage:.1f}%")

            detail_col1, detail_col2, detail_col3 = st.columns(3)

            detail_col1.caption(
                f"Budget: {format_currency(budget_amount_value)}"
            )

            detail_col2.caption(
                f"Spent: {format_currency(spent)}"
            )

            detail_col3.caption(
                f"Remaining: {format_currency(remaining)}"
            )

            if spent > budget_amount_value:

                st.error(
                    f"{category}: You exceeded your budget by "
                    f"{format_currency(abs(remaining))}."
                )

            elif percentage >= 80:

                st.warning(
                    f"{category}: You have used more than 80% "
                    "of your budget."
                )

            st.write("")

        st.divider()

        # --------------------------------------------------
        # EDIT OR DELETE BUDGET
        # --------------------------------------------------

        st.markdown("### Manage Budgets")

        budget_options = {
            f"{budget['category']} — "
            f"{format_currency(budget['amount'])}": budget
            for budget in selected_budgets
        }

        selected_budget_label = st.selectbox(
            "Select a budget",
            list(budget_options.keys()),
            key="manage_budget_selector"
        )

        selected_budget = budget_options[selected_budget_label]

        with st.expander("Edit Selected Budget"):

            with st.form("edit_budget_form"):

                new_budget_amount = st.number_input(
                    "New Budget Amount (₹)",
                    min_value=1.0,
                    value=float(selected_budget["amount"]),
                    step=500.0
                )

                update_budget_button = st.form_submit_button(
                    "Update Budget",
                    use_container_width=True
                )

                if update_budget_button:

                    try:

                        update_budget(
                            selected_budget["id"],
                            new_budget_amount
                        )

                        st.success("Budget updated successfully!")

                        st.rerun()

                    except Exception as error:

                        st.error(str(error))

        with st.expander("Delete Selected Budget"):

            confirm_budget_delete = st.checkbox(
                "I confirm that I want to delete this budget.",
                key="confirm_budget_delete"
            )

            if st.button(
                "Delete Budget",
                disabled=not confirm_budget_delete,
                key="delete_budget_button"
            ):

                try:

                    delete_budget(selected_budget["id"])

                    st.success("Budget deleted successfully!")

                    st.rerun()

                except Exception as error:

                    st.error(str(error))


# ==========================================================
# 13. OVERVIEW DASHBOARD
# ==========================================================

def show_overview():

    st.title("Good to see you!")

    st.write(
        f"Here is your financial overview for "
        f"{today.strftime('%B %Y')}."
    )

    st.divider()

    # ------------------------------------------------------
    # KEY FINANCIAL METRICS
    # ------------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        display_metric(
            "Total Balance",
            format_currency(total_balance),
            "Income minus expenses"
        )

    with col2:

        display_metric(
            "Total Income",
            format_currency(total_income),
            "All recorded income",
            "income-value"
        )

    with col3:

        display_metric(
            "Total Expenses",
            format_currency(total_expenses),
            "All recorded expenses",
            "expense-value"
        )

    with col4:

        display_metric(
            "Transactions",
            str(transaction_count),
            "Total records"
        )

    st.write("")

    # ------------------------------------------------------
    # MONTHLY SUMMARY
    # ------------------------------------------------------

    st.markdown("### This Month")

    month_col1, month_col2, month_col3 = st.columns(3)

    month_col1.metric(
        "Monthly Income",
        format_currency(monthly_income)
    )

    month_col2.metric(
        "Monthly Expenses",
        format_currency(monthly_expenses)
    )

    month_col3.metric(
        "Monthly Balance",
        format_currency(monthly_balance)
    )

    st.divider()

    if df.empty:

        st.markdown("""
        <div class="empty-state">
            <h3>Welcome to Finora</h3>
            <p>You haven't added any transactions yet.</p>
            <p>Start by adding your income and expenses to see your financial dashboard.</p>
        </div>
        """, unsafe_allow_html=True)

        show_add_transaction_form()

        return

    # ------------------------------------------------------
    # MONTHLY TREND
    # ------------------------------------------------------

    st.markdown("### Income and Expense Trends")

    monthly_chart = create_monthly_trend_chart(df)

    if monthly_chart is not None:

        st.plotly_chart(
            monthly_chart,
            use_container_width=True
        )

    # ------------------------------------------------------
    # CATEGORY BREAKDOWN AND TOP SPENDING
    # ------------------------------------------------------

    left_col, right_col = st.columns(2)

    with left_col:

        st.markdown("### Expense Breakdown")

        category_chart = create_expense_category_chart(df)

        if category_chart is not None:

            st.plotly_chart(
                category_chart,
                use_container_width=True
            )

        else:

            st.info("No expense data available.")

    with right_col:

        st.markdown("### Top Spending Categories")

        top_chart = create_top_spending_chart(df)

        if top_chart is not None:

            st.plotly_chart(
                top_chart,
                use_container_width=True
            )

        else:

            st.info("No expense data available.")

    st.divider()

    # ------------------------------------------------------
    # RECENT TRANSACTIONS
    # ------------------------------------------------------

    st.markdown("### Recent Transactions")

    recent_transactions = df.sort_values(
        "date",
        ascending=False
    ).head(5)

    show_transaction_table(recent_transactions)

    st.write("")

    if st.button(
        "View All Transactions",
        use_container_width=False
    ):

        st.session_state.current_page = "Transaction Management"

        st.rerun()

    st.divider()

    # ------------------------------------------------------
    # QUICK ADD TRANSACTION
    # ------------------------------------------------------

    show_add_transaction_form()

# ==========================================================
# 14. AI FINANCIAL ASSISTANT
# ==========================================================

def show_ai_assistant():

    st.title("AI Financial Assistant")

    st.write(
        "Ask questions about your finances and get insights "
        "based on your transaction history."
    )

    st.divider()

    # ------------------------------------------------------
    # FINANCIAL SUMMARY
    # ------------------------------------------------------

    st.markdown("### Your Financial Snapshot")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Monthly Income",
        format_currency(monthly_income)
    )

    col2.metric(
        "Monthly Expenses",
        format_currency(monthly_expenses)
    )

    col3.metric(
        "Monthly Balance",
        format_currency(monthly_balance)
    )

    st.divider()

    # ------------------------------------------------------
    # SUGGESTED QUESTIONS
    # ------------------------------------------------------

    st.markdown("### Suggested Questions")

    suggestions = [
        "Analyze my spending this month",
        "Which category am I spending the most on?",
        "How can I improve my savings?",
        "Give me practical ways to reduce expenses"
    ]

    suggestion_columns = st.columns(2)

    for index, suggestion in enumerate(suggestions):

        with suggestion_columns[index % 2]:

            if st.button(
                suggestion,
                key=f"ai_suggestion_{index}",
                use_container_width=True
            ):

                st.session_state.ai_pending_question = suggestion

    st.divider()

    # ------------------------------------------------------
    # CHAT HISTORY
    # ------------------------------------------------------

    for message in st.session_state.ai_chat_history:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])

    # ------------------------------------------------------
    # USER QUESTION
    # ------------------------------------------------------

    user_question = st.chat_input(
        "Ask something about your finances..."
    )

    pending_question = st.session_state.pop(
        "ai_pending_question",
        None
    )

    question = pending_question or user_question

    if question:

        st.session_state.ai_chat_history.append(
            {
                "role": "user",
                "content": question
            }
        )

        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):

            with st.spinner("Analyzing your financial data..."):

                try:

                    financial_context = build_financial_context()

                    prompt = f"""
                    You are Finora, a helpful personal finance assistant.

                    Answer the user's question using the financial
                    information provided below.

                    Give clear, practical and easy-to-understand advice.

                    Do not invent financial information.

                    Financial Information:
                    {financial_context}

                    User Question:
                    {question}
                    """

                    response = generate_financial_response(
    financial_context,
    question
)

                    st.markdown(response)

                    st.session_state.ai_chat_history.append(
                        {
                            "role": "assistant",
                            "content": response
                        }
                    )

                except Exception as error:

                    st.error(f"AI Error: {str(error)}")

                    st.exception(error)

    # ------------------------------------------------------
    # CLEAR CHAT
    # ------------------------------------------------------

    if st.session_state.ai_chat_history:

        if st.button("Clear Chat"):

            st.session_state.ai_chat_history = []

            st.rerun()


# ==========================================================
# 15. SMART INSIGHTS PAGE
# ==========================================================

def show_smart_insights():

    st.title("Smart Insights")

    st.write(
        "Understand your spending patterns, monitor your "
        "financial health and identify unusual expenses."
    )

    st.divider()

    # ------------------------------------------------------
    # GENERATE SMART INSIGHTS
    # ------------------------------------------------------

    try:

        insights = generate_smart_insights(current_month)

    except Exception as error:

        st.error(
            f"Unable to calculate Smart Insights: {error}"
        )

        return

    # ------------------------------------------------------
    # FINANCIAL HEALTH SUMMARY
    # ------------------------------------------------------

    st.markdown("### Monthly Financial Summary")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Income",
        format_currency(insights.get("income", 0))
    )

    col2.metric(
        "Expenses",
        format_currency(insights.get("expenses", 0))
    )

    col3.metric(
        "Balance",
        format_currency(insights.get("balance", 0))
    )

    col4.metric(
        "Savings Rate",
        f"{insights.get('savings_rate', 0):.1f}%"
    )

    st.divider()

    # ------------------------------------------------------
    # SPENDING ANALYSIS
    # ------------------------------------------------------

    st.markdown("### Spending Analysis")

    highest_category = insights.get(
        "highest_category",
        "No data"
    )

    if highest_category:

        st.info(
            f"Your highest spending category this month is "
            f"**{highest_category}**."
        )

    category_totals = insights.get(
        "category_totals",
        {}
    )
    if category_totals:

        category_df = pd.DataFrame(
            list(category_totals.items()),
            columns=["Category", "Amount"]
        )

        category_df = category_df.sort_values(
            "Amount",
            ascending=False
        )

        fig = px.bar(
            category_df,
            x="Category",
            y="Amount",
            color_discrete_sequence=["#82C7F8"],
            text_auto=".2s"
        )

        fig.update_layout(
            plot_bgcolor="#FFFFFF",
            paper_bgcolor="#FFFFFF",
            font=dict(
                family="Arial",
                color="#263B35",
                size=12
            ),
            xaxis=dict(
                title="Category",
                showgrid=False,
                zeroline=False
            ),
            yaxis=dict(
                title="Amount (₹)",
                showgrid=True,
                gridcolor="#E8EEEB",
                zeroline=False
            ),
            margin=dict(l=20, r=20, t=20, b=20),
            height=400
        )

        fig.update_traces(
            textposition="outside",
            marker_line_width=0
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False}
        )

    else:

        st.info("No category spending data available.")

    st.divider()

    # ------------------------------------------------------
    # BUDGET WARNINGS
    # ------------------------------------------------------

    st.markdown("### Budget Alerts")

    budget_warnings = insights.get(
        "budget_warnings",
        []
    )

    if budget_warnings:

        for warning in budget_warnings:

            if isinstance(warning, dict):

                category = warning.get(
                    "category",
                    "Category"
                )

                message = warning.get(
                    "message",
                    str(warning)
                )

                st.warning(
                    f"**{category}:** {message}"
                )

            else:

                st.warning(str(warning))

    else:

        st.success(
            "No budget warnings. Keep monitoring your spending!"
        )

    st.divider()

    # ------------------------------------------------------
    # PREVIOUS MONTH COMPARISON
    # ------------------------------------------------------

    st.markdown("### Previous Month Comparison")

    previous_expenses = insights.get(
        "previous_month_expenses",
        None
    )

    current_expenses = insights.get(
        "expenses",
        0
    )

    if previous_expenses is not None and previous_expenses > 0:

        difference = current_expenses - previous_expenses

        percentage_change = (
            difference / previous_expenses
        ) * 100

        if difference > 0:

            st.warning(
                f"Your expenses increased by "
                f"{percentage_change:.1f}% compared with last month."
            )

        elif difference < 0:

            st.success(
                f"Your expenses decreased by "
                f"{abs(percentage_change):.1f}% compared with last month."
            )

        else:

            st.info(
                "Your expenses are the same as last month."
            )

        comparison_col1, comparison_col2 = st.columns(2)

        comparison_col1.metric(
            "Previous Month",
            format_currency(previous_expenses)
        )

        comparison_col2.metric(
            "Current Month",
            format_currency(current_expenses),
            delta=f"{percentage_change:.1f}%"
        )

    else:

        st.info(
            "Not enough previous-month data for comparison."
        )

    st.divider()

    # ------------------------------------------------------
    # UNUSUAL SPENDING DETECTION
    # ------------------------------------------------------

    st.markdown("### Unusual Spending Detection")

    st.write(
        "Finora compares your current category spending "
        "with the average of the previous three months."
    )

    try:

        unusual_spending = detect_unusual_spending(
            current_month
        )

        if unusual_spending:

            for item in unusual_spending:

                category = item.get(
                    "category",
                    "Unknown"
                )

                current_amount = item.get(
                    "current_spending",
                    item.get("current", 0)
                )

                average_amount = item.get(
                    "average_spending",
                    item.get("average", 0)
                )

                st.warning(
                    f"**{category}** — Current spending: "
                    f"{format_currency(current_amount)}. "
                    f"Previous average: "
                    f"{format_currency(average_amount)}."
                )

        else:

            st.success(
                "No unusual spending detected, or there is "
                "not enough historical data to identify a pattern."
            )

    except Exception as error:

        st.error(
            f"Unable to detect unusual spending: {error}"
        )

    st.divider()

    # ------------------------------------------------------
    # AI FINANCIAL RECOMMENDATIONS
    # ------------------------------------------------------

    st.markdown("### AI Financial Recommendations")

    if st.button(
        "Generate AI Recommendations",
        use_container_width=True
    ):

        with st.spinner(
            "Generating personalized financial recommendations..."
        ):

            try:

                recommendations = generate_ai_recommendations(
                    insights
                )

                st.markdown(recommendations)

            except Exception:

                st.warning(
                    "AI recommendations are temporarily unavailable. "
                    "Please try again later."
                )


# ==========================================================
# 16. FINAL PAGE ROUTING
# ==========================================================

selected_page = st.session_state.current_page

if selected_page == "Overview":

    show_overview()

elif selected_page == "Transaction Management":

    show_transaction_management()

elif selected_page == "Financial Analytics":

    show_financial_analytics()

elif selected_page == "Budget Planning":

    show_budget_planning()

elif selected_page == "AI Financial Assistant":

    show_ai_assistant()

elif selected_page == "Smart Insights":

    show_smart_insights()

else:

    st.title("Page Not Found")

    st.info(
        "Please select a page from the sidebar navigation."
    )


# ==========================================================
# 17. FOOTER
# ==========================================================

st.divider()

st.markdown(
    """
    <div style="text-align:center; padding:15px 0;">
        <p style="color:#888; font-size:13px;">
            Finora — Personal Finance & Expense Tracker
        </p>
        <p style="color:#999; font-size:11px;">
            Manage your money. Understand your habits. Build better finances.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)
