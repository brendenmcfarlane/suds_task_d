from application.llm_interface import LLMInterface
from api.deepseek_client import DeepSeekAPI
from api.openai_client import OpenAIAPI
LLM_INTERFACES = {
    "test": LLMInterface,
    "default": DeepSeekAPI,
    "deepseek": DeepSeekAPI,
    "openai": OpenAIAPI,
    "default-vision": OpenAIAPI
    }