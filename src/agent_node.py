# responsible for the inpput output and role of an agent
from src.events import Event, EventBus
from dataclasses import dataclass
from tests.test_bus import TEST_BUS

@dataclass
class AddAgentAction(Event):
    agent_id: str
    action_type: str
    action_content: str

class AgentNode:
    def __init__(self, id="", prompt="", event_producer=TEST_BUS):
        self._id = id
        self._prompt = prompt
        self._inputs = []
        self._inputs.append({"type":"prompt", "prompt":prompt})
        self._output = {}
        self._event_producer = event_producer

    def get_id(self):
        return self._id
    def get_client_input(self):
        text_input = ""
        inputs = self._inputs[:]
        inputs_to_remove = []
        for input in inputs:
            if input.get("type")=="text":
                text_input = text_input + "\n" + input["text"]
                inputs_to_remove.append(input)
        for input in inputs_to_remove:
            inputs.remove(input)
        if text_input != "":
            inputs.insert(0, {"type": "text", "text":text_input})
        return inputs
    def get_output(self):
        return self._output
    def set_output(self, msg):
        self._output = msg
        agent_action = AddAgentAction(self._id, self._prompt, msg)
        self._event_producer.publish(agent_action)
        return None
    def check_is_executed(self):
        return (self._output != {})
    def receive_message(self, message):
        ''' Precondition: <message> of the form { "type": "input_type", "input_type": "input data" }
        '''
        self._inputs.append(message)
        return None
    def reset_agent(self):
        self._inputs = []
        self._inputs.append({"type":"prompt", "prompt":self._prompt})
        self._output = {}
        return None
    
    