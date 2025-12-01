import json

def load_data(file_path):
    with open(file_path, "r") as f:
        return json.load(f)

def score_customer(c):
    score = 0

    spend_ratio = c["avg_monthly_spend"] / c["avg_monthly_income"]
    if spend_ratio < 0.4:
        score += 150
    elif 0.4 < spend_ratio < 0.8:
        score += 80
    else:
        score -= 50

    tp = c["transaction_pattern"]

    if tp["transaction_count_last_30_days"] > 30:
        score += 120
    elif tp["transaction_count_last_30_days"] > 15:
        score += 70
    else:
        score += 20

    if tp["avg_transaction_amount"] < (c["avg_monthly_income"] / 50):
        score += 60
    else:
        score += 20

    if tp["incoming_to_outgoing_ratio"] >= 1:
        score += 100
    else:
        score += 40

    score -= tp["anomaly_flags"] * 80

    if c["late_payment_count"] == 0:
        score += 150
    elif c["late_payment_count"] == 1:
        score += 70
    elif c["late_payment_count"] <= 3:
        score += 20
    else:
        score -= 100

    util = c["credit_utilization_ratio"]
    if util < 30:
        score += 150
    elif util < 60:
        score += 70
    else:
        score -= 100

    score -= c["current_loans"] * 40

    if c["account_age_months"] >= 24:
        score += 120
    elif c["account_age_months"] >= 12:
        score += 60
    else:
        score += 20

    score -= c["suspicious_transaction_flags"] * 120

    return score

def classify(score):
    if score >= 700:
        return "APPROVED"
    elif score >= 600:
        return "REVIEW"
    else:
        return "REJECTED"

def process_credit_scores(input_file):
    data = load_data(input_file)
    results = []

    for c in data["customers"]:
        score = score_customer(c)
        decision = classify(score)
        results.append({
            "customer_id": c["customer_id"],
            "score": score,
            "decision": decision
        })

    return results


if __name__ == "__main__":
    results = process_credit_scores("customer_data.json")
    for r in results:
        print(r)