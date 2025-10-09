from flask import Flask, render_template, request
from datetime import datetime
from collections import defaultdict

app = Flask(__name__)

# Store budgets and expenses
global_budget = 0
monthly_budget = defaultdict(float)
expenses = []

@app.route('/', methods=['GET', 'POST'])
def home():
    global global_budget, monthly_budget, expenses

    if request.method == 'POST':
        # --- Set global budget ---
        if 'set_global_budget' in request.form:
            global_budget = float(request.form['global_budget'])

        # --- Set monthly budget ---
        elif 'set_monthly_budget' in request.form:
            month = request.form['budget_month']  # e.g. "2025-10"
            budget = float(request.form['budget'])
            monthly_budget[month] = budget

        # --- Add expense ---
        elif 'add_expense' in request.form:
            name = request.form['expense_name']
            amount = float(request.form['expense_amount'])
            category = request.form['expense_category']

            # Parse date or use today's date
            date_str = request.form.get('expense_date')
            if date_str:
                date = datetime.strptime(date_str, "%Y-%m-%d")
            else:
                date = datetime.today()

            expenses.append({
                'name': name,
                'amount': amount,
                'category': category,
                'date': date
            })

    # --- Calculate totals ---
    total_spent = sum(e['amount'] for e in expenses)
    remaining_global = global_budget - total_spent

    # --- Monthly totals ---
    monthly_totals = defaultdict(float)
    for e in expenses:
        month_key = e['date'].strftime("%Y-%m")
        monthly_totals[month_key] += e['amount']

    # Collect all months seen in expenses or budgets
    months = sorted(set(list(monthly_budget.keys()) + list(monthly_totals.keys())))
    month_values = [monthly_totals[m] for m in months]
    month_budgets = [monthly_budget.get(m, 0) for m in months]
    month_remaining = [month_budgets[i] - month_values[i] for i in range(len(months))]

    return render_template(
        "index.html",
        global_budget=global_budget,
        remaining_global=remaining_global,
        expenses=expenses,
        months=months,
        month_values=month_values,
        month_budgets=month_budgets,
        month_remaining=month_remaining
    )

if __name__ == '__main__':
    app.run(debug=True)
