
class WorkFlowNode():
    def __init__(self, key:str):
        self._id = key
        self._children = []
        self._transcript = []
        self._adjacencies = []

    def get_workflow(self):
        return self._adjacencies

    def add_child(self, child):
        self._children.append(child)

    def get_children(self):
        return self._children
    
    def add_adjacency(self, adj):
        self._adjacencies.append(adj)

    def set_transcript(self, transcript:list[dict]):
        self._transcript = transcript