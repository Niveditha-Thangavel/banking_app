import json
import os
from crewai import Agent, Task, Crew, LLM
from crewai.tools import BaseTool
from dotenv import load_dotenv

load_dotenv()

class FetchBankStatementTool(BaseTool):
    name: str = "FetchBankStatement"
    description: str = "Fetch the bank statement for a specific customer_id"

    def _run(self, customer_id: str):
        with open("bank_statement.json", "r") as f:
            data = json.load(f)

        for customer in data["bank_statements"]:
            if customer["customer_id"] == customer_id:
                return customer

        return {"error": "Customer not found"}

class CalculateMetricsTool(BaseTool):
    name: str = "CalculateCreditMetrics"
    description: str = "Run transaction + credit card + loan metrics calculator"

    def _run(self, statement: dict):
        from calculate import calculate
        return calculate(statement)


class RunCreditScoreTool(BaseTool):
    name: str = "RunCreditScore"
    description: str = "Compute final credit scoring using calculated metrics"

    def _run(self, metrics: dict):
        from main import run_scoring
        return run_scoring(metrics)
        

llm = LLM(
    model="huggingface/meta-llama/Meta-Llama-3-8B-Instruct",
    api_key=os.getenv("HUGGINGFACE_API_KEY")
)

def create_agent():
    agent = Agent(
        role="Bank credit decision expert",
        goal="Determine the final credit approval result from customer data.",
        backstory="Processes statements, loans, spending, credit behavior and produces a final credit decision.",
        tools=[
            FetchBankStatementTool(),
            CalculateMetricsTool(),
            RunCreditScoreTool()
        ],
        llm=llm
    )
    return agent

def create_task(customer_id):
    credit_agent = create_agent()
    task = Task(
        description=f"""
        The user provides customer_id = "{customer_id}". 
        Follow these steps:
        1. Fetch bank statement using FetchBankStatement with the EXACT customer_id above.
        2. Calculate credit metrics using CalculateCreditMetrics.
        3. Run the final credit scoring using RunCreditScore.
        
        Return ONLY the final JSON result.
        """,
        agent=credit_agent,
        expected_output="A JSON credit decision."
    )
    return task


user_id = input("Enter customer ID: ")

crew = Crew(
    agents=[create_agent()],
    tasks=[create_task(user_id)],
    verbose=True
)
result = crew.kickoff()

print("\n🎯 FINAL CREDIT DECISION:\n", result)
