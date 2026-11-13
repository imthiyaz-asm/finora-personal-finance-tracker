
from smart_insights import generate_smart_insights


print("Generating Finora Smart Insights...")
print("=" * 45)

insights = generate_smart_insights()

print(f"\nMonth: {insights['month']}")

print("\nFINANCIAL SUMMARY")
print("-" * 30)

print(f"Income: ₹{insights['income']:,.2f}")
print(f"Expenses: ₹{insights['expenses']:,.2f}")
print(f"Balance: ₹{insights['balance']:,.2f}")
print(f"Savings Rate: {insights['savings_rate']:.2f}%")

print("\nTOP SPENDING CATEGORY")
print("-" * 30)

if insights["highest_category"]:
    category = insights["highest_category"]
    amount = insights["category_totals"][category]

    print(f"{category}: ₹{amount:,.2f}")
else:
    print("No expenses recorded.")

print("\nBUDGET WARNINGS")
print("-" * 30)

if insights["budget_warnings"]:

    for warning in insights["budget_warnings"]:
        print(
            f"{warning['category']} | "
            f"{warning['status']} | "
            f"Spent: ₹{warning['spent']:,.2f} | "
            f"Budget: ₹{warning['budget']:,.2f}"
        )

else:
    print("No budget warnings.")

print("\nMONTHLY COMPARISON")
print("-" * 30)

print(
    f"Previous Month Expenses: "
    f"₹{insights['previous_month_expenses']:,.2f}"
)

if insights["expense_change_percentage"] is not None:

    print(
        f"Expense Change: "
        f"{insights['expense_change_percentage']:+.2f}%"
    )

else:
    print("No previous-month expense data for comparison.")

print("\n" + "=" * 45)
print("Smart Insights analysis completed!")
