class Agent:
    def __init__(self, name, blackboard, llm_client):
        self.name = name
        self.blackboard = blackboard
        self.llm = llm_client

    def communicate(self, report):
        """Post analysis to the blackboard."""
        self.blackboard.post_report(self.name, report)

    def analyze(self, data):
        """Abstract method to be implemented by subclasses."""
        raise NotImplementedError