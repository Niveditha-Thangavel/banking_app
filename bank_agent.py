from crewai import Agent, Task, Crew

def create_agents(customer_id):
    input_agent = Agent(
        role="Input Agent",
        goal=f"Gather all financial data for customer {customer_id} from the database: "
             "bank statements, credit card details, and loan details.",
        backstory=f"You are an information fetcher that accurately retrieves all the "
                  f"financial records for customer {customer_id}."
    )

    calculator_agent = Agent(
        role="Calculator Agent",
        goal="Transform raw financial records into structured metrics like "
             "average monthly income, average monthly spend, transaction patterns, etc., "
             "and forward them to the approval agent.",
        backstory="You are a fast, precise calculator who converts raw statements "
                  "into credit-scoring parameters."
    )

    approval_agent = Agent(
        role="Approval Agent",
        goal="Apply scoring rules on the calculator output, normalize the score between 0 and 10, "
             "and return loan approval status with reasons.",
        backstory=f"You are the loan manager who uses the generated metrics to decide whether "
                  f"customer {customer_id} should be approved."
    )
    
    return input_agent, calculator_agent, approval_agent

def create_task(customer_id):
    input_agent, calculator_agent, approval_agent = create_agents(customer_id)
    input_agent_task = Task(
        description=f"Fetch bank statements, credit card details, and loan data for customer {customer_id}.",
        expected_output="A JSON object containing all financial data for the customer.",
        agent=input_agent
    )

    calculator_agent_task = Task(
        description="Process the input data and compute metrics such as average monthly income, "
                    "average spend, transaction patterns, and credit utilization ratio.",
        expected_output="A structured JSON object containing processed credit-scoring parameters.",
        agent=calculator_agent
    )

    approval_agent_task = Task(
        description="Take the computed parameters and calculate credit score (0–10). "
                    "Provide approval or rejection with explanation.",
        expected_output="Loan approval decision, score, and reason.",
        agent=approval_agent
    )

    return input_agent_task, calculator_agent_task, approval_agent_task


customer_id = "C101"