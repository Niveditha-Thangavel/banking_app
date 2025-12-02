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

def create_agents():
    fetch_agent =  Agent(
        role="Fetch Bank Statement Agent",
        goal="Fetch the bank statement for a given customer_id.",
        backstory="Responsible for fetching customer bank statements.",
        tools=[FetchBankStatementTool()],
        llm=llm
    )

    metrics_agent = Agent(
        role="Credit Metrics Agent",
        goal="Calculate metrics from bank statement data.",
        backstory="Responsible for analyzing transactions and loans.",
        tools=[CalculateMetricsTool()],
        llm=llm
    )

    scoring_agent = Agent(
        role="Credit Scoring Agent",
        goal="Generate final credit decision using calculated metrics.",
        backstory="Responsible for computing credit score and approval.",
        tools=[RunCreditScoreTool()],
        llm=llm
    )

    return fetch_agent, metrics_agent, scoring_agent

def create_tasks(customer_id):
    fetch_agent, metrics_agent, scoring_agent = create_agents()
    
    fetch_task = Task(
        description=f"Fetch bank statement for customer_id '{customer_id}'",
        agent=fetch_agent,
        expected_output="Bank statement JSON"
    )

    metrics_task = Task(
        description="Calculate metrics from fetched bank statement",
        agent=metrics_agent,
        expected_output="Calculated metrics JSON"
    )

    scoring_task = Task(
        description="Generate final credit decision",
        agent=scoring_agent,
        expected_output="Final credit decision JSON"
    )

    return fetch_task, metrics_task, scoring_task


user_id = input("Enter customer ID: ")
fetch_agent, metrics_agent, scoring_agent = create_agents()
fetch_task, metrics_task, scoring_task = create_tasks(user_id)

crew = Crew(
    agents=[fetch_agent, metrics_agent, scoring_agent],
    tasks=[fetch_task, metrics_task, scoring_task],
    verbose=True
)
result = crew.kickoff()

print("\n🎯 FINAL CREDIT DECISION:\n", result)
