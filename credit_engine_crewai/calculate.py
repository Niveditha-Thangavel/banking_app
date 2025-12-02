import json
import math
from datetime import datetime

def calculate(statement):
    with open("credits_loan.json", "r") as f:
        data = json.load(f)

    income = 0
    spend = 0
    month_spend = 0
    month_income = 0
    no_of_transaction = len(statement["transactions"])

    for trans in statement["transactions"]:
        if trans["type"] == "credit":
            month_income += trans["amount"]
            income += 1
        else:
            month_spend += trans["amount"]
            spend += 1

    avg_month_income = month_income / income
    avg_month_spend = month_spend / spend

    total_transaction_amount = month_spend + month_income
    avg_spend_ratio = (avg_month_spend / avg_month_income) * 100
    avg_transaction_amount = total_transaction_amount / (income + spend)

    sum_of_sq = 0
    for trans in statement["transactions"]:
        diff = (avg_transaction_amount - trans["amount"]) ** 2
        sum_of_sq += diff
    variance = sum_of_sq / no_of_transaction
    standard_deviation = math.sqrt(variance)

    anomaly = 0
    for trans in statement["transactions"]:
        if trans["amount"] > standard_deviation:
            anomaly += 1

    today = datetime.today()

    results = []
    for customer in data["customer_accounts"]:
        late_count = 0
        for card in customer.get("credit_cards", []):
            for cycle in card.get("billing_cycles", []):
                payment_date = datetime.strptime(cycle["payment_date"], "%Y-%m-%d")
                cycle_end = datetime.strptime(cycle["cycle_end"], "%Y-%m-%d")
                if payment_date > cycle_end or cycle["amount_paid"] < cycle["amount_due"]:
                    late_count += 1

        loans = customer.get("loans", [])
        active_loans = sum(1 for loan in loans if loan["outstanding_amount"] > 0)

        utilization_values = []
        for card in customer.get("credit_cards", []):
            limit = card["credit_limit"]
            balance = card["current_balance"]
            utilization_values.append((balance / limit) * 100)

        credit_utilization_ratio = (
            sum(utilization_values) / len(utilization_values)
            if utilization_values else 0
        )

        created = datetime.strptime(customer["account_creation_date"], "%Y-%m-%d")
        account_age_months = (today.year - created.year) * 12 + (today.month - created.month)

        results.append({
            "late_payment_count": late_count,
            "current_loans": active_loans,
            "credit_utilization_ratio": credit_utilization_ratio,
            "account_age_months": account_age_months
        })

    output = {
        "avg_monthly_income": avg_month_income,
        "avg_monthly_spend": avg_month_spend,
        "transaction_pattern": {
            "transaction_count": no_of_transaction,
            "avg_transaction_amount": avg_transaction_amount,
            "spend_ratio": avg_spend_ratio,
            "anamoly_flags": anomaly
        },
        "late_payment_counts": late_count,
        "current_loans": active_loans,
        "credit_utilization_ratio": credit_utilization_ratio,
        "account_age_months": account_age_months
    }

    with open("calculated.json", "w") as w:
        json.dump(output, w, indent=4)

    return output
