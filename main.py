import csv
import os
from datetime import datetime
from decimal import Decimal, InvalidOperation

FILE_NAME = "expenses.csv"

CATEGORIES = [
    "Food", "Travel", "College",
    "Shopping", "Bills", "Other"
]


def initialize_file():
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(
                ["ID", "Date", "Category", "Description", "Amount"]
            )


def load_expenses():
    initialize_file()
    with open(FILE_NAME, "r", newline="") as file:
        return list(csv.DictReader(file))


def add_expense():
    print("\n--- Add Expense ---")

    date = input(
        "Date (YYYY-MM-DD), or Enter for today: "
    ).strip()

    if not date:
        date = datetime.now().strftime("%Y-%m-%d")

    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        print("Invalid date.")
        return

    print("\nCategories:")
    for i, category in enumerate(CATEGORIES, 1):
        print(f"{i}. {category}")

    try:
        choice = int(input("Choose category (1-6): "))
        if not 1 <= choice <= len(CATEGORIES):
            print("Invalid category.")
            return
    except ValueError:
        print("Enter a valid number.")
        return

    category = CATEGORIES[choice - 1]

    description = input("Description: ").strip()
    if not description:
        print("Description cannot be empty.")
        return

    try:
        amount = Decimal(input("Amount in rupees: "))
        if not amount.is_finite() or amount <= 0:
            print("Amount must be positive.")
            return
        amount = amount.quantize(Decimal("0.01"))
    except (InvalidOperation, ValueError):
        print("Enter a valid amount.")
        return

    expenses = load_expenses()
    next_id = max(
        (int(item["ID"]) for item in expenses),
        default=0
    ) + 1

    with open(FILE_NAME, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            next_id, date, category,
            description, f"{amount:.2f}"
        ])

    print("Expense added successfully!")


def view_expenses():
    expenses = load_expenses()

    print("\n--- All Expenses ---")

    if not expenses:
        print("No expenses recorded.")
        return

    for item in expenses:
        print(
            f"ID: {item['ID']} | "
            f"Date: {item['Date']} | "
            f"Category: {item['Category']} | "
            f"Description: {item['Description']} | "
            f"Amount: Rs. {item['Amount']}"
        )


def show_summary():
    expenses = load_expenses()

    if not expenses:
        print("No expenses available.")
        return

    total = sum(
        (Decimal(item["Amount"]) for item in expenses),
        Decimal("0")
    )

    month = datetime.now().strftime("%Y-%m")

    monthly_total = sum(
        (
            Decimal(item["Amount"])
            for item in expenses
            if item["Date"].startswith(month)
        ),
        Decimal("0")
    )

    print(f"\nTotal expenses: Rs. {total:.2f}")
    print(f"This month's expenses: Rs. {monthly_total:.2f}")

    print("\nCategory-wise spending:")

    totals = {}

    for item in expenses:
        category = item["Category"]
        totals[category] = (
            totals.get(category, Decimal("0"))
            + Decimal(item["Amount"])
        )

    for category, amount in totals.items():
        print(f"{category}: Rs. {amount:.2f}")


def delete_expense():
    expenses = load_expenses()

    if not expenses:
        print("No expenses to delete.")
        return

    view_expenses()

    try:
        expense_id = int(input("Enter expense ID to delete: "))
    except ValueError:
        print("Invalid ID.")
        return

    updated = [
        item for item in expenses
        if int(item["ID"]) != expense_id
    ]

    if len(updated) == len(expenses):
        print("Expense not found.")
        return

    with open(FILE_NAME, "w", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "ID", "Date", "Category",
                "Description", "Amount"
            ]
        )
        writer.writeheader()
        writer.writerows(updated)

    print("Expense deleted successfully!")


def main():
    initialize_file()

    while True:
        print("\n==============================")
        print("   STUDENT EXPENSE TRACKER")
        print("==============================")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Expense Summary")
        print("4. Delete Expense")
        print("5. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            show_summary()
        elif choice == "4":
            delete_expense()
        elif choice == "5":
            print("Thank you for using the tracker!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
