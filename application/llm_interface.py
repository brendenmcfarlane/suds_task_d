# from google import genai
# from google.genai import types

# from api_key import GEMINI_API_KEY
# from src.api_throttler import GEMINI_THROTTLER
class LLMInterface:
    def make_query(self, msg:list[dict]) -> list[dict]:
        return [{"type": "text", "text":"query made"}]
    
# class SlowGeminiAPI(LLMInterface):
#     def __init__(self):
#         self._client = genai.Client(api_key=GEMINI_API_KEY)
#         self._model = "gemini-3.1-flash-lite"
#         self._config = {"temperature":1.5, "max_output_tokens": 1024, "seed": 42}

#     def make_query(self, msg: dict) -> str:
#         GEMINI_THROTTLER.make_call()
#         interaction = self._client.interactions.create(
#             model=self._model,
#             input={"type": "user_input",
#                    "content":msg},
#             generation_config=self._config
#         )
#         if interaction.output_text is None:
#             return ""
        
#         return interaction.output_text

