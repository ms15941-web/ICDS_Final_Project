import ollama


class AIBot:
    def __init__(self, model="phi3:mini"):
        self.model = model
        self.default_prompt = "You are a helpful AI assistant. You must answer in English."
        self.history = [
            {"role": "system", "content": self.default_prompt}
        ]

    def set_personality(self, prompt):
        if not prompt.strip():
            prompt = self.default_prompt

        self.history = [
            {"role": "system", "content": prompt}
        ]
        return f"Personality set to: {prompt}"

    def ask(self, user_input):
        try:
            self.history.append({"role": "user", "content": user_input})

            response = ollama.chat(model=self.model, messages=self.history)

            bot_reply = response['message']['content']
            self.history.append({"role": "assistant", "content": bot_reply})

            return bot_reply

        except Exception as e:
            return f"Error: Cannot connect to Ollama. Ensure 'ollama serve' is running. Details: {str(e)}"

    def analyze_chat(self, chat_history_text, instruction):
        try:
            prompt = (
                f"Here is a chat log between users:\n"
                f"'''\n{chat_history_text}\n'''\n\n"
                f"Task: {instruction}\n"
                f"Answer in English. Be concise."
            )

            messages = [
                {"role": "system", "content": "You are a helpful assistant analyzing chat logs."},
                {"role": "user", "content": prompt}
            ]

            response = ollama.chat(model=self.model, messages=messages, options={'temperature': 0.3})
            return response['message']['content']

        except Exception as e:
            return f"Analysis Error: {str(e)}"
    def clear_memory(self):
        current_system = self.history[0]
        self.history = [current_system]