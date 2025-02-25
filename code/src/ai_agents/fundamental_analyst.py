from ai_agents.base_agent import Agent

class FundamentalAnalyst(Agent):
    def analyze(self, data):
        prompt = f"Analyze the financial statements: {data}. Provide a report on valuation and growth potential."
        report = self.llm.generate(prompt)
        lines = report.splitlines()
        valuation = lines[0] if lines else "N/A"
        growth = lines[-1] if lines else "N/A"
        self.communicate({"valuation": valuation, "growth": growth})