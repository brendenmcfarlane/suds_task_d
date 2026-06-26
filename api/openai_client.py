from api_key import OPEN_AI_API_KEY
from application.llm_interface import LLMInterface
from openai import OpenAI

class OpenAIAPI(LLMInterface):
    def __init__(self):
        self._client = OpenAI(api_key=OPEN_AI_API_KEY)

    def format_input(self, input:list[dict]) -> list[dict[str,str]]:
        formatted_input = [{"system_prompt": "", "text": ""}]
        for item in input:
            match item["type"]:
                case "prompt":
                    formatted_input[0]["system_prompt"] = item["prompt"]
                case "text":
                    formatted_input[0]["text"] =  formatted_input[0]["text"] + item["text"]
                case "image_url":
                    formatted_input[0]["image_url"] = item["image_url"]
        return formatted_input
    
    def _api_call(self, msg:list[dict]):
        if len(msg[0].keys()) == 2:
            content = msg[0]["text"]
        elif len(msg[0].keys()) == 3:
            text = msg[0]["text"]
            image_url = msg[0]["image_url"]
            content = [
                {
                    "type": "input_text",
                    "text": text,
                },
                {
                    "type": "input_image",
                    "image_url": image_url
                }
            ]

        response = self._client.responses.create(
            model="gpt-5.4-mini",
            instructions=msg[0]["system_prompt"],
            input=[
                {
                    "role": "user",
                    "content": content
                }
            ]
        )
        return response

    def make_query(self, msg:list[dict]) -> list[dict]:
        messages = self.format_input(msg)
        response = self._api_call(messages)
        return [{"type": "text", "text": response.output_text}]

        
