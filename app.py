import os
import json
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

EXPENSE_FILE = "expenses.json"

# Ensure JSON file exists
if not os.path.exists(EXPENSE_FILE):
    with open(EXPENSE_FILE, "w") as f:
        json.dump({}, f, indent=4)

CATEGORIES = ["Groceries", "Entertainment", "Dining", "Gas", "Utilities", "Other"]

# Load all expenses
def load_expenses():
    with open(EXPENSE_FILE) as f:
        return json.load(f)

# Save expenses
def save_expenses(data):
    with open(EXPENSE_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Register a new month with all categories starting at 0
def register_month(month_name):
    data = load_expenses()
    if month_name not in data:
        data[month_name] = {cat: 0 for cat in CATEGORIES}
        data[month_name]["Total"] = 0
        save_expenses(data)

# Add or update an expense
def add_expense(month_name, category, amount):
    data = load_expenses()
    if month_name not in data:
        register_month(month_name)
    if category not in data[month_name]:
        data[month_name][category] = 0
    data[month_name][category] += amount
    # Update total
    data[month_name]["Total"] = sum(value for key, value in data[month_name].items() if key != "Total")
    save_expenses(data)

# Delete all expenses for a month
def delete_all_expenses(month_name):
    data = load_expenses()
    if month_name in data:
        data[month_name] = {cat: 0 for cat in CATEGORIES}
        data[month_name]["Total"] = 0
        save_expenses(data)

# Calculate percentage growth compared to previous month
def calculate_growth(current_month, previous_month):
    growth = {}
    for category in current_month:
        if category == "Total":
            continue
        prev = previous_month.get(category, 0)
        curr = current_month[category]
        growth[category] = ((curr - prev) / prev * 100) if prev else 0
    # Total growth
    prev_total = previous_month.get("Total", 0)
    curr_total = current_month.get("Total", 0)
    growth["Total"] = ((curr_total - prev_total) / prev_total * 100) if prev_total else 0
    return growth

@app.route("/", methods=["GET", "POST"])
def home():
    # Default month
    month = request.form.get("month") or "October"

    # Register month if it doesn't exist
    register_month(month)

    # Load data
    expenses = load_expenses()
    current = expenses.get(month, {})

    # Handle form submissions
    if request.method == "POST":
        # Add expense
        if "add_expense" in request.form:
            name = request.form.get("expense_name")
            category = request.form.get("expense_category")
            amount = float(request.form.get("expense_amount"))
            add_expense(month, category, amount)
            return redirect(url_for("home"))

        # Delete all expenses
        if "delete_all_expenses" in request.form:
            delete_all_expenses(month)
            return redirect(url_for("home"))

    # Previous month for growth calculation (fallback empty)
    months_list = list(expenses.keys())
    months_list.sort()
    prev_month_name = months_list[months_list.index(month)-1] if month in months_list and months_list.index(month) > 0 else None
    previous = expenses.get(prev_month_name, {}) if prev_month_name else {}

    growth = calculate_growth(current, previous)

    # Dummy budget (can extend with real budget handling)
    budget = None

    return render_template(
        "index.html",
        month=month,
        months=months_list,
        current=current,
        growth=growth,
        budget=budget
    )

if __name__ == "__main__":
    app.run(debug=True)
