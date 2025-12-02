#This is a sample crewai code to demonstrate the use of huggingface model into crewai

from crewai import Agent, Task, Crew, LLM
import os

llm = LLM(
    model="huggingface/meta-llama/Meta-Llama-3-8B-Instruct",
    api_key=os.getenv("HUGGINGFACE_API_KEY"),
)

agent = Agent(
    name="ExplainAgent",
    role="Explainer",
    goal="Explain things clearly",
    backstory="You help explain concepts simply and clearly.",
    llm=llm
)

task = Task(
    description="Explain what transformers are in ML.",
    expected_output="Give two points on what transformers are in ML",
    agent=agent
)

crew = Crew(agents=[agent], tasks=[task])
output = crew.kickoff()
print(output)
