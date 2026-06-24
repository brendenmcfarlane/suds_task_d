from application.llm_interface import LLMInterface
from api.deepseek_client import DeepSeekAPI
LLM_INTERFACES = {
    "test": LLMInterface,
    "default": DeepSeekAPI,
    "deepseek": DeepSeekAPI
    }