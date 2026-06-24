from src.agent_node import AgentNode
from application.llm_interface import LLMInterface

class AgentRepo():
    def __init__(self):
        self._repo = {}

    def add_agent(self, id="", agent=None, llm_client=None):
        if isinstance(agent, AgentNode):
            self._repo[agent.get_id()] = {"node": agent, "client": llm_client}
        else:
            self._repo[id] = {"node": agent, "client": llm_client}

    def get_agent(self, id) -> AgentNode|None:
        return self._repo[id]["node"]
    
    def set_agent(self, id:str, agent:AgentNode) -> None:
        self._repo[id]["node"] = agent
        return None
    
    def get_client(self, id) -> LLMInterface|None:
        return self._repo[id]["client"]
    
    def set_client(self, id:str, client:LLMInterface) -> None:
        self._repo[id]["client"] = client
        return None