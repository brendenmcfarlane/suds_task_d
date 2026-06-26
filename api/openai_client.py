from api_key import OPEN_AI_API_KEY
from application.llm_interface import LLMInterface
from openai import OpenAI

class OpenAIAPI(LLMInterface):
    def __init__(self):
        self._client = OpenAI(api_key=OPEN_AI_API_KEY)

    def format_input(self, input:list[dict]) -> list[dict[str,str]]:
        formatted_input = [{"role": "system"}, {"role": "user", "content": ""}]
        for item in input:
            match item["type"]:
                case "prompt":
                    formatted_input[0]["content"] = item["prompt"]
                case "text":
                    formatted_input[1]["content"] =  formatted_input[1]["content"] + item["text"]
        return formatted_input
    
    def _api_call(self, msg:list[dict]):
        response = self._client.responses.create(
            model="gpt-5.4-mini",
            instructions=msg[0]["content"],
            input=[
                {
                    "role": "user",
                    "content": msg[1]["content"]
                }
            ]
        )
        return response

    def make_query(self, msg:list[dict]) -> list[dict]:
        messages = self.format_input(msg)
        response = self._api_call(messages)
        return [{"type": "text", "text": response.output_text}]

        
