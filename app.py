from flask import Flask, render_template, request, redirect, url_for
import datetime

app = Flask(__name__)

# Store budget and expenses in memory
budget = 0
expenses = []  # each expense will be a dict like {'name':..., 'amount':..., 'category':..., 'month':...}

@app.route("/", methods=["GET", "POST"])
def index():
    global budget, expenses

    # Handle form submissions
    if request.method == "POST":
        # If the user submitted the "Set Budget" form
        if "set_budget" in request.form:
            budget = float(request.form["budget"])

        # If the user submitted the "Add Expense" form
        elif "add_expense" in request.form:
            name = request.form["expense_name"]
            amount = float(request.form["expense_amount"])
            category = request.form["expense_category"]
            month = datetime.date.today().strftime("%B %Y")  # e.g. "October 2025"

            # Add expense to list
            expenses.append({
                "name": name,
                "amount": amount,
                "category": category,
                "month": month
            })

    # Calculate summary info
    total_spent = sum(e["amount"] for e in expenses)
    remaining = budget - total_spent

    # Pass values to HTML template
    return render_template(
        "index.html",
        budget=budget,
        expenses=expenses,
        total_spent=total_spent,
        remaining=remaining
    )

# Run app
if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
