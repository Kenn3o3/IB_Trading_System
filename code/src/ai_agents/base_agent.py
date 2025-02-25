from utils.llm_client import LLMClient

class Agent:
    def __init__(self, name, blackboard):
        self.name = name
        self.blackboard = blackboard
        self.llm = LLMClient()

    def communicate(self, report):
        """Post analysis to the blackboard."""
        self.blackboard.post_report(self.name, report)

    def analyze(self, data):
        """Abstract method to be implemented by subclasses."""
        raise NotImplementedError