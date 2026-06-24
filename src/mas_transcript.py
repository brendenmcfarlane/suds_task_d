
class TranscriptInterface:
    def __init__(self, task_id, actors, edges, **kwargs):
        self._states = []
        self._actions = []
        self._task_id = task_id
        self._actors = actors
        self._edges = edges

    def update_transcript(self, **kwargs):
        self._actions.append(kwargs.get("action"))
        self._states.append(kwargs.get("state"))

    def print_transcript(self) -> list: 
        return self._states
    
class FullTranscript(TranscriptInterface):
    def print_transcript(self) -> list: 
        steps = []
        for i in range(len(self._actions)):
            step = {"task_id": self._task_id,
                    "step": i + 1,
                    "acting_agent": self._actors[i],
                    "state_before": self._states[i],
                    "action": self._actions[i],
                    "state_after": self._states[i+1]
                    }
            steps.append(step)

        return steps 


