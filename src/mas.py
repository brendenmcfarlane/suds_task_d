from collections import deque
from src.events import Event, EventProducer, EventBus, EventListener, AddAgentAction, MASStateUpdate
from dataclasses import dataclass
from src.default_bus import DEFAULT_BUS

from src.mas_transcript import FullTranscript


class MAS(EventListener):
    def __init__(self, event_producer:EventProducer = DEFAULT_BUS):
        self._agents = []
        self._adjacencies = {}
        self._sorted = False
        self._topo_order = []
        self._curr_queue = deque([])
        self._question = " "
        self._informed_agents = []
        self._event_producer = event_producer
        # self._transcript_type = FullTranscript
        self._transcript = []

    # def set_transcript_type(self, transcript_type):
    #     self._transcript_type = transcript_type

    def handle(self, event: AddAgentAction):
        if event.agent_id in self._agents:
            transcript_line = f"Agent: {event.agent_id}\n>>Input Prompt: {event.action_type}\n>>Response: {event.action_content}"
            self._transcript.append(transcript_line)
        else: pass

    def next_agent(self): 
        edges =  self._get_all_adjacencies()[:]
        for agent in self._informed_agents:
            edges.append(("question", agent))
        topology = {"vertices": self._agents, "edges": edges}
        state = MASStateUpdate(self._question, topology, self._transcript[:])
        self._event_producer.publish(state)
        if len(self._curr_queue) == 0:
            return None
        else:
            return self._curr_queue.popleft()
    
    def set_question(self, q):
        self._question = q
        self.plan_trajectory()
        return self._informed_agents
        # self._transcript = self._transcript_type(q, self._topo_order, self._get_all_adjacencies)
    
    def get_agents(self):
       return self._agents
    
    def _get_all_adjacencies(self):
        edges = []
        for a1 in self._agents:
            for a2 in self._adjacencies.get(a1):
                edges.append((a1, a2))
        return edges
    
    def add_agent(self, agent:str):
        self._agents.append(agent)
        self._adjacencies[agent] = []
        return None
    
    def get_adjacencies(self, agent:str):
        return self._adjacencies[agent]
    
    def add_adjacency(self, agent_one, agent_two):
        if (agent_one != "question") and (agent_two not in self._adjacencies.get(agent_one)):
            self._adjacencies[agent_one].append(agent_two)
        if agent_one == "question" and agent_two not in self._informed_agents:
            self._informed_agents.append(agent_two)
        return None
    
    def remove_adjacency(self, agent_one, agent_two):
        if (agent_one != "question") and (agent_two in self._adjacencies.get(agent_one)):
            self._adjacencies[agent_one].remove(agent_two)
        if agent_one == "question" and agent_two in self._informed_agents:
            self._informed_agents.remove(agent_two)
        return None
    
    def plan_trajectory(self) -> None:
        in_degree = {v: 0 for v in self._agents}
        for source in self._adjacencies:
            for destination in self._adjacencies[source]:
                if destination in in_degree:
                    in_degree[destination] += 1
        queue = deque([v for v in self._agents if in_degree[v] == 0])
        topo_order = []
        while queue:
            u = queue.popleft()
            topo_order.append(u)
            neighbors = self._adjacencies.get(u, [])
            for v in neighbors:
                in_degree[v] -= 1
                if in_degree[v] == 0:
                    queue.append(v)
        if len(topo_order) != len(self._agents):
            raise ValueError("The graph contains a cycle! Topological sort is impossible.")
        self._topo_order = topo_order
        self._curr_queue = deque(topo_order)
        self._sorted = True