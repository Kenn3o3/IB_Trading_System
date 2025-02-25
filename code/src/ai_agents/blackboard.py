class Blackboard:
    def __init__(self):
        self.reports = {}

    def post_report(self, agent_name, report):
        self.reports[agent_name] = report

    def get_report(self, agent_name):
        return self.reports.get(agent_name, {})