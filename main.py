import json
from input import create_details
from calculate import calculate

customer_id = input("Enter Customer id(C101): ")
create_details(customer_id)

with open("customer_data.json") as f:
    statement = json.load(f)

with open("credits_loan.json", "r") as f:
    data = json.load(f)
    
calculate(statement,data)


with open("calculated.json", "r") as f:
    data = json.load(f)


score = 0
rejection_reasons = []


spend_ratio = data["avg_monthly_spend"] / data["avg_monthly_income"]
if spend_ratio < 0.4:
    score += 150
elif 0.4 < spend_ratio < 0.8:
    score += 80
else:
    score -= 50
    rejection_reasons.append("High spending ratio")


tp = data["transaction_pattern"]


if tp["transaction_count"] > 30:
    score += 120
elif tp["transaction_count"] > 15:
    score += 70
else:
    score += 20


if tp["avg_transaction_amount"] < (data["avg_monthly_income"] / 50):
    score += 60
else:
    score += 20


if tp["spend_ratio"] < 1:
    score += 100
else:
    score += 40
    rejection_reasons.append("Transaction pattern shows high spending")


anomaly_penalty = tp["anamoly_flags"] * 80
score -= anomaly_penalty
if tp["anamoly_flags"] > 0:
    rejection_reasons.append(f"{tp['anamoly_flags']} anomaly flags detected")


if data["late_payment_counts"] == 0:
    score += 150
elif data["late_payment_counts"] == 1:
    score += 70
elif data["late_payment_counts"] <= 3:
    score += 20
else:
    score -= 100
    rejection_reasons.append("Too many late payments")

util = data["credit_utilization_ratio"]
if util < 30:
    score += 150
elif util < 60:
    score += 70
else:
    score -= 100
    rejection_reasons.append(f"High credit utilization ({util}%)")

loan_penalty = data["current_loans"] * 40
score -= loan_penalty
if data["current_loans"] > 1:
    rejection_reasons.append(f"{data['current_loans']} current loans")


if data["account_age_months"] >= 24:
    score += 120
elif data["account_age_months"] >= 12:
    score += 60
else:
    score += 20
    if data["account_age_months"] < 6:
        rejection_reasons.append("Account too new")


min_score = -1000
max_score = 1000
normalized = ((score - min_score) / (max_score - min_score)) * 10
normalized = round(normalized, 2)


if normalized >= 7.0:
    print("DECISION: APPROVED")
elif normalized >= 5.0:
    print("DECISION: REVIEW")
else:
    print("DECISION: REJECTED")
    if rejection_reasons:
        print("Reasons:", ", ".join(rejection_reasons[:3]))  