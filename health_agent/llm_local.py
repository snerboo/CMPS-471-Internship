import ollama


class LocalTherapyLLM:
    def __init__(self, model_name):
        self.model_name = model_name

    def generate(self, messages):
        response = ollama.chat(model=self.model_name, messages=messages)
        message = response.get("message", {})
        return message.get("content", "").strip()
