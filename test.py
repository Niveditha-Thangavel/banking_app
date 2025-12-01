import json
from datetime import datetime

with open("credits_loan.json", "r") as f:
    data = json.load(f)

today = datetime.today()

results = []

for customer in data["customer_accounts"]:
    customer_id = customer["customer_id"]

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
        utilization = (balance / limit) * 100
        utilization_values.append(utilization)

    credit_utilization_ratio = (
        sum(utilization_values) / len(utilization_values)
        if utilization_values else 0
    )

    created = datetime.strptime(customer["account_creation_date"], "%Y-%m-%d")

    account_age_months = (today.year - created.year) * 12 + (today.month - created.month)

    results.append({
        "customer_id": customer_id,
        "late_payment_count": late_count,
        "current_loans": active_loans,
        "credit_utilization_ratio": round(credit_utilization_ratio, 2),
        "account_age_months": account_age_months
    })

print(json.dumps(results, indent=4))
