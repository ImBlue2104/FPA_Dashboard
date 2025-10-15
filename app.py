from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In-memory storage
data = {
    "budget": 0,
    "expenses": [],
    "month": "October"
}

@app.route("/", methods=["GET", "POST"])
def home():
    global data

    if request.method == "POST":
        # Handle month selection
        if "month" in request.form:
            data["month"] = request.form["month"]

        # Set budget
        elif "set_budget" in request.form:
            data["budget"] = float(request.form["budget"])

        # Add expense
        elif "add_expense" in request.form:
            name = request.form["expense_name"]
            amount = float(request.form["expense_amount"])
            category = request.form["expense_category"]
            data["expenses"].append({"name": name, "amount": amount, "category": category})

        # Delete all expenses
        elif "delete_all_expenses" in request.form:
            data["expenses"].clear()

        # Delete one expense
        elif "delete_expense" in request.form:
            name_to_delete = request.form["delete_expense_name"]
            data["expenses"] = [e for e in data["expenses"] if e["name"] != name_to_delete]

        # Delete budget
        elif "delete_budget" in request.form:
            data["budget"] = 0

        return redirect(url_for("home"))

    total_spent = sum(e["amount"] for e in data["expenses"])
    remaining = data["budget"] - total_spent

    return render_template(
        "index.html",
        budget=data["budget"],
        expenses=data["expenses"],
        total_spent=total_spent,
        remaining=remaining,
        month=data["month"]
    )


if __name__ == "__main__":
    app.run(debug=True)

