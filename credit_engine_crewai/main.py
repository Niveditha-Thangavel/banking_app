import json

def run_scoring(metrics=None):
    # If CrewAI passed metrics directly
    if metrics:
        data = metrics
    else:
        # Fallback
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
        rejection_reasons.append(
            f"{tp['anamoly_flags']} anomaly flags detected"
        )

    late = data["late_payment_counts"]
    if late == 0:
        score += 150
    elif late == 1:
        score += 70
    elif late <= 3:
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

    score -= data["current_loans"] * 40
    if data["current_loans"] > 1:
        rejection_reasons.append(f"{data['current_loans']} current loans")

    age = data["account_age_months"]
    if age >= 24:
        score += 120
    elif age >= 12:
        score += 60
    else:
        score += 20
        if age < 6:
            rejection_reasons.append("Account too new")

    normalized = round(((score + 1000) / 2000) * 10, 2)

    if normalized >= 7.0:
        decision = "APPROVED"
    elif normalized >= 5.0:
        decision = "REVIEW"
    else:
        decision = "REJECTED"

    return {
        "decision": decision,
        "score": normalized,
        "reasons": rejection_reasons[:3]
    }
