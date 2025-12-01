import json 
import input

with open("customer_data.json") as f:
    statement = json.load(f)



def calculate(statement):
    avg_month_spend = 0
    avg_month_income = 0
    no_of_transaction = len(statement["transactions"])
    for trans in statement["transactions"]:
        if trans["type"] == "credit":
            avg_month_income+= trans["amount"]
        else:
            avg_month_spend+= trans["amount"]
    total_transacrtion_amount =  avg_month_spend+avg_month_income 
    avg_spend_ratio = (avg_month_spend/avg_month_income) * 100
    avg_transaction_amount= total_transacrtion_amount
    for trans in statement["transaction"]:
        mean_diff = avg_transaction_amount - trans["amount"]
        

   



        

    
