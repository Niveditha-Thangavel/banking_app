import json

customer_id = input("Enter the customer ID: ")

def load_data():
    with open ("bank_statement.json","r") as f:
        statement = json.load(f)

    with open ("credits_load.json","r") as f1:
        credit_loan = json.load(f1)

    return statement, credit_loan