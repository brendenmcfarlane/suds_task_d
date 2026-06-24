from api_key import DEEPSEEK_API_KEY
from application.llm_interface import LLMInterface
from openai import OpenAI

class DeepSeekAPI(LLMInterface):
    def __init__(self):
        self._client = OpenAI(
            api_key=DEEPSEEK_API_KEY,
            base_url="https://api.deepseek.com")

    def format_input(self, input:list[dict]) -> list[dict[str,str]]:
        formatted_input = []
        for item in input:
            match item["type"]:
                case "prompt":
                    formatted_input.insert(0,{"role": "system", "content": item["prompt"]})
                case "text":
                    formatted_input.append({"role": "user", "content": item["text"]})
        return formatted_input
    
    def _api_call(self, msg:list[dict]):
        response = self._client.chat.completions.create(
            model="deepseek-v4-flash",
            messages=msg
        )
        return response

    def make_query(self, msg:list[dict]) -> list[dict]:
        messages = self.format_input(msg)
        chat_completion = self._api_call(messages)
        formatted_output = { "type": "text", "text": chat_completion.choices[0].message.content}
        return [formatted_output]

        
