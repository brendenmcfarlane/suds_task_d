from src.agent_node import AgentNode
from src.mas import MAS
from src.query import Query
from src.events import EventProducer
from application.agent_repo import AgentRepo
from application.database_interface import DBInterface
from application.llm_interfaces_dict import LLM_INTERFACES
from api.deepseek_client import DeepSeekAPI
from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass
class SetupInputData:
    repo: AgentRepo
    db: DBInterface
    agent_path: str
    query_path: str
    event_producer: EventProducer


class ExecuteAgentI():
    def __init__(self, agent_repo):
        self._agent_repo = agent_repo
    def execute_agent_uc(self, agent_id:str):
        pass
    
class ExecuteAgentInteractor(ExecuteAgentI):
    def execute_agent_uc(self, agent_id):
        agent = self._agent_repo.get_agent(agent_id)
        content = agent.get_client_input()
        client = self._agent_repo.get_client(agent_id)
        output = client.make_query(content)
        agent.set_output(output)

class ImportAgentsI:
    def __init__(self, path:str, db:DBInterface, repo:AgentRepo, event_producer:EventProducer):
        self._path = path
        self._db = db
        self._repo = repo
        self._event_producer = event_producer
    def import_agents_uc(self):
        pass

class ImportAgentsInteractor(ImportAgentsI):
    def import_agents_uc(self):
        data = self._db.read_in(self._path)
        for id in data.keys():
            self._repo.add_agent(agent=AgentNode(id=id, prompt=data[id]["prompt"], event_producer=self._event_producer), llm_client=LLM_INTERFACES[data[id]["model"]]())
        return None

class BuildMASFromSpecsI:
    def __init__(self, path:str, db:DBInterface, repo:AgentRepo, event_producer:EventProducer):
        self._path = path
        self._db = db
        self._repo = repo
        self._event_producer = event_producer
    def build_mas_from_specs_uc(self) -> MAS:
        return MAS()

class BuildMASFromSpecsInteractor(BuildMASFromSpecsI):
    def build_mas_from_specs_uc(self):
        mas = MAS(event_producer=self._event_producer)
        mas_specs = self._db.read_in(self._path)
        for agent in mas_specs["agents"]:
            mas.add_agent(agent)
        for edge in mas_specs["edges"]:
            mas.add_adjacency(edge[0], edge[1])
        return mas

class ImportQueriesI:
    def __init__(self, path, db) -> None:
        self._path = path
        self._db = db  
    def import_queries_uc(self) -> list[Query]:
        return [Query()]
    
class ImportQueriesInteractor(ImportQueriesI):
    def import_queries_uc(self) -> list[Query]:
        queries = self._db.read_in(self._path)
        processed_queries = []
        for q in queries:
            processed_queries.append(Query(**q))
        return processed_queries
    
class ExecuteFullTraceI:
    def __init__(self, mas:MAS, q:Query, repo:AgentRepo):
        self._mas = mas
        self._question = q
        self._repo = repo
    def execute_full_trace_uc(self) -> None:
        pass

class ExecuteFullTraceInteractor(ExecuteFullTraceI):
    def execute_full_trace_uc(self) -> None:
        #TODO: reset MAS fn (or multiple traces)
        informed_agents = self._mas.set_question(self._question)
        for agent in informed_agents:
            self._repo.get_agent(agent).receive_message({"type": "text", "text": self._question.get_question()})
        curr_actor = self._mas.next_agent()
        agent_executor = ExecuteAgentInteractor(self._repo)
        while curr_actor:
            agent_executor.execute_agent_uc(curr_actor)
            for adj in self._mas.get_adjacencies(curr_actor):
                adj_agent = self._repo.get_agent(adj)
                if not (adj_agent is None):
                    curr_agent = self._repo.get_agent(curr_actor)
                    outputs = curr_agent.get_output()
                    for output in outputs:
                        adj_agent.receive_message(output)
            curr_actor = self._mas.next_agent()

class ExecuteLLMJudgeI(ABC):
    def __init__(self, agent_repo):
        self._agent_repo = agent_repo
    @abstractmethod
    def execute_judge_llm_uc(self, agent_id:str, json_str:str) ->str:
        pass
    
class ExecuteLLMJudgeInteractor(ExecuteAgentI):
    def execute_judge_llm_uc(self, agent_id, json_str) -> str:
        judge = self._agent_repo.get_agent(agent_id)
        judge.receive_message({"type": "text", "text": json_str})
        content = judge.get_client_input()
        client = self._agent_repo.get_client(agent_id)
        output = client.make_query(content)
        judge.set_output(output)
        return judge.get_output()[0].get("text")