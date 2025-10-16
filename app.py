from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

DATA_FILE = "data.json"

# Initialize empty data file if it doesn't exist
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({}, f, indent=4)

def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

@app.route("/", methods=["GET", "POST"])
def home():
    data = load_data()
    months = ["January","February","March","April","May","June","July","August","September","October","November","December"]
    
    # Default month
    month = request.args.get("month", "January")
    if month not in data:
        data[month] = {"budget": 0, "expenses": []}

    # Handle form submissions
    if request.method == "POST":
        # Month selection
        if "set_month" in request.form:
            month = request.form.get("month", month)
            if month not in data:
                data[month] = {"budget": 0, "expenses": []}

        # Set budget
        if "set_budget" in request.form:
            budget = float(request.form.get("budget", 0))
            data[month]["budget"] = budget

        # Delete budget
        if "delete_budget" in request.form:
            data[month]["budget"] = 0

        # Add expense
        if "add_expense" in request.form:
            name = request.form.get("expense_name")
            amount = float(request.form.get("expense_amount", 0))
            category = request.form.get("expense_category")
            data[month]["expenses"].append({
                "name": name,
                "amount": amount,
                "category": category
            })

        # Delete single expense
        if "delete_expense" in request.form:
            name_to_delete = request.form.get("delete_expense_name")
            data[month]["expenses"] = [e for e in data[month]["expenses"] if e["name"] != name_to_delete]

        # Delete all expenses
        if "delete_all_expenses" in request.form:
            data[month]["expenses"] = []

        save_data(data)
        return redirect(url_for("home", month=month))

    # Summary calculations
    expenses = data[month]["expenses"]
    total_spent = sum(e["amount"] for e in expenses)
    budget = data[month]["budget"]
    remaining = budget - total_spent

    # Growth rate vs previous month
    prev_index = months.index(month)-1
    growth_rate = None
    if prev_index >= 0:
        prev_month = months[prev_index]
        prev_total = sum(data.get(prev_month, {}).get("expenses", []), 0)
        prev_total = sum(e["amount"] for e in data.get(prev_month, {}).get("expenses", []))
        if prev_total > 0:
            growth_rate = round(((total_spent - prev_total)/prev_total)*100,2)

    # Data for chart
    categories = [e["category"] for e in expenses]
    amounts = [e["amount"] for e in expenses]

    return render_template(
        "index.html",
        month=month,
        months=months,
        expenses=expenses,
        total_spent=total_spent,
        budget=budget,
        remaining=remaining,
        growth_rate=growth_rate,
        categories=categories,
        amounts=amounts
    )

if __name__ == "__main__":
    app.run(debug=True)
