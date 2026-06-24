from src.events import EventListener
from src.agent_node import AddAgentAction
from src.mas import MASStateUpdate


class Transcript:
    def __init__(self) -> None:
        self.actions = []
        self.states = []
    def get_steps(self):
        steps = []
        for i in range(len(self.actions)):
            step = {}
            step["question"] = self.states[i].question.get_question()
            step["step"] = i + 1
            step["topology"] = self.states[i].topology["edges"]
            step["agent"] = self.actions[i].agent_id
            step["state_before"] = self.states[i].transcript
            step["action"] = {"type":self.actions[i].action_type, "content": self.actions[i].action_content}
            step["state_after"] = self.states[i+1].transcript
            steps.append(step)
        return steps

class AgentActionListener(EventListener):
    def __init__(self, transcript: Transcript) -> None:
        super().__init__()
        self._transcript = transcript

    def handle(self, event: AddAgentAction):
        self._transcript.actions.append(event)


class MASStateListener(EventListener):
    def __init__(self, transcript: Transcript) -> None:
        super().__init__()
        self._transcript = transcript

    def handle(self, event: MASStateUpdate):
        self._transcript.states.append(event)
