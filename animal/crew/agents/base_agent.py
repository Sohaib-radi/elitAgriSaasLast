from crewai import Agent

class BaseFarmAgent:
    """
    Abstract base agent class for all farm AI agents.
    Contains common properties and utilities that all agents share.
    """

    def __init__(self, role: str, goal: str, backstory: str, tools: list = None):
        self.agent = Agent(
            role=role,
            goal=goal,
            backstory=backstory,
            tools=tools or [],
            llm=None,  # Simulated offline agent
            verbose=True,
            allow_delegation=False
        )

    def get(self):
        return self.agent
