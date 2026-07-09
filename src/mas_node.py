from src.events import EventListener, Event
from src.agent_node import AddAgentAction
from src.mas import MASStateUpdate

class MASNode(EventListener):
    def __init__(self, parent=None) -> None:
        self._question = ""
        self._topology = {}
        self._acting_agent_id = ""
        self._action_type = ""
        self._action_content = ""
        self._children = []
        self._parent = parent

    def get_children(self):
        return self._children[:]
    
    def create_child(self):
        child_node = MASNode(parent=self)
        self._children.append(child_node)
        return child_node
    
    def handle(self, event: Event):
        if isinstance(event, AddAgentAction):
            self._acting_agent_id = event.agent_id
            self._action_type = event.action_type
            self._action_content = event.action_content
        elif isinstance(event, MASStateUpdate):
            self._question = event.question
            self._topology = event.topology

    def get_partial_transcript(self):
        """Returns MAS partial transcript up to and include this nodes state"""
        if self._parent is None:
            transcript = []
        else:
            transcript = self._parent.get_partial_transcript()
            if self._acting_agent_id != "":
                transcript_line = f"Agent: {self._acting_agent_id}\n>>Input Prompt: {self._action_type}\n>>Response: {self._action_content}"
                transcript.append(transcript_line)
        return transcript 
    
