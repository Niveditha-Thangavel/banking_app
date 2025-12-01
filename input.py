import json

def create_details(customer_id):
    with open ("bank_statement.json","r") as f:
        statement = json.load(f)

    with open ("credits_loan.json","r") as f1:
        credit_loan = json.load(f1)

    statement_customer = -1
    account_creation = -1
    credit = -1
    loans = -1

    for id in statement["bank_statements"]:
        if id["customer_id"] == customer_id:
            statement_customer = id["transactions"]

    for id in credit_loan["customer_accounts"]:
        if id["customer_id"] == customer_id:
            account_creation = id["account_creation_date"]
            credit = id["credit_cards"]
            loans = id["loans"]


    with open ("customer_data.json", "w") as w:
        data = {"transactions": statement_customer, "account_creation_date":account_creation,"credit_card":credit, "loans":loans}
        json.dump(data,w,indent = 4)   
