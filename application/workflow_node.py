
class WorkFlowNode():
    def __init__(self):
        self._children = []
        self._transcript = []

    def add_child(self, child):
        self._children.append(child)

    def get_children(self):
        return self._children
    
    def set_transcript(self, transcript:list[dict]):
        self._transcript = transcript