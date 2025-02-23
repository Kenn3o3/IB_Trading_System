from openai import OpenAI

class LLMClient:
    def __init__(self, model="gpt-4-1106-preview"):
        self.client = OpenAI()
        self.model = model
        
    def generate(self, prompt, temperature=0.3):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature
        )
        return response.choices[0].message.content