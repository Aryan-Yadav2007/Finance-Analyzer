from flask import Flask, render_template, request
import sqlite3
import matplotlib
import json

matplotlib.use("Agg")
import matplotlib.pyplot as plt

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("transaction.html")


@app.route("/submit", methods=["POST", "GET"])
def submit():
    if request.method == "POST":
        amount = request.form.get("amount")
        type = request.form.get("type")
        description = request.form.get("description")
        date = request.form.get("date")

        conn = sqlite3.connect("finance.db")
        cursor = conn.cursor()

        cursor.execute(
            """
     INSERT INTO transactions(amount,type,description,date) VALUES(?, ?, ?, ?)
     """,
            (amount, type, description, date),
        )

        conn.commit()
        conn.close()

        return "logs saved"


@app.route("/history")
def history():

    conn = sqlite3.connect("finance.db")

    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    rows = cursor.execute("SELECT * FROM transactions").fetchall()

    conn.close()

    return render_template("history.html", rows=rows)


@app.route("/summary")
def summary():

    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()

    cursor.execute("SELECT SUM(amount) FROM transactions WHERE type = 'expense'")
    result = cursor.fetchone()
    expenses = result[0]

    cursor.execute("SELECT SUM(amount) FROM transactions WHERE type = 'income'")
    result2 = cursor.fetchone()
    incomes = result2[0]

    return render_template("summary.html", incomes=incomes, expenses=expenses)


@app.route("/search", methods=["POST", "GET"])
def search():
    if request.method == "GET":
        return render_template("search.html")

    searchT = request.form.get("search")
    term = f"%{searchT}%"

    conn = sqlite3.connect("finance.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM transactions WHERE type LIKE ?", (term,))

    transactions = cursor.fetchall()

    conn.close()

    return render_template("search.html", transactions=transactions)


@app.route("/analysis")
def analysis():
    return render_template("analysis.html")


@app.route("/chart")
def chart():

    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT type, SUM(amount) FROM transactions
    GROUP BY TYPE
    """)

    data = cursor.fetchall()

    types = []
    amount = []

    for row in data:
        types.append(row[0])
        amount.append(row[1])

    conn.close()

    plt.bar(types, amount)

    plt.xlabel("Transaction Type")
    plt.ylabel("Amount")
    plt.title("Income vs Expense")

    plt.savefig("static/chart.png")

    return render_template("chart.html")


@app.route("/overtime")
def overtime():

    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()

    cursor.execute("SELECT amount,date FROM transactions")
    data = cursor.fetchall()

    amounts = [row[0] for row in data]
    dates = [row[1] for row in data]

    conn.close()

    plt.bar(dates, amounts)

    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Transaction over time")

    plt.savefig("static/chart2.png")

    return render_template("overtime.html")


@app.route("/filter")
def filter():
    return render_template("filter.html")


@app.route("/incomeFilter")
def typeFilter():

    conn = sqlite3.connect("finance.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM transactions WHERE type = ?", ("income",))

    data = cursor.fetchall()

    conn.close()
    html = ""

    for transaction in data:
        html += f"""
        <p>Amount: {transaction["amount"]}</p>
        <p>Type: {transaction["type"]}</p>
        <p>Description: {transaction["description"]}</p>
        <p>Date: {transaction["date"]}</p>
        <hr>
        """

    return html


@app.route("/expenseFilter")
def dateFilter():
    conn = sqlite3.connect("finance.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM transactions WHERE type = ?", ("expense",))

    data = cursor.fetchall()

    conn.close()
    html = ""

    for transaction in data:
        html += f"""
            <p>Amount: {transaction["amount"]}</p>
            <p>Type: {transaction["type"]}</p>
            <p>Description: {transaction["description"]}</p>
            <p>Date: {transaction["date"]}</p>
            <hr>
            """

    return html


@app.route("/MaxExpense")
def MaxExpense():

    conn = sqlite3.connect("finance.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(
        "SELECT amount,description,date FROM transactions WHERE type = 'expense' ORDER BY amount DESC LIMIT 1"
    )

    data = cursor.fetchall()

    # dict_data = [dict(row) for row in data]

    conn.close()

    html = ""

    for transaction in data:
        html += f"""
                <p>Amount: {transaction["amount"]}</p>
                <p>Description: {transaction["description"]}</p>
                <p>Date: {transaction["date"]}</p>
                <hr>
                """

    return html


@app.route("/MaxIncome")
def MaxIncome():

    conn = sqlite3.connect("finance.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(
        "SELECT amount,description,date FROM transactions WHERE type = 'income' ORDER BY amount DESC LIMIT 1"
    )

    data = cursor.fetchall()
    print(data)

    # dict_data = [dict(row) for row in data]

    conn.close()

    html = ""

    for transaction in data:
        html += f"""
                <p>Amount: {transaction["amount"]}</p>
                <p>Description: {transaction["description"]}</p>
                <p>Date: {transaction["date"]}</p>
                <hr>
                """

    return html


if __name__ == "__main__":
    app.run(debug=True)
