import json 
import input

with open("customer_data.json") as f:
    statement = json.load(f)

def calculate(statement):
    income = 0
    spend = 0
    month_spend = 0
    month_income = 0
    no_of_transaction = len(statement["transactions"])
    for trans in statement["transactions"]:
        if trans["type"] == "credit":
            month_income+= trans["amount"]
            income+=1
        else:
            month_spend+= trans["amount"]
            spend+=1
    avg_month_income = month_income/income
    avg_month_spend = month_spend/spend

    total_transaction_amount =  month_spend+ month_income 
    avg_spend_ratio = (avg_month_spend/avg_month_income) * 100
    avg_transaction_amount= total_transaction_amount / (income+spend)
    for trans in statement["transactions"]:
        mean_diff = avg_transaction_amount - trans["amount"]

    print(avg_month_income,avg_month_spend,avg_spend_ratio,avg_transaction_amount,mean_diff)

calculate(statement)