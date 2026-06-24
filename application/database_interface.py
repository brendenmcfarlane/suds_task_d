import json
class DBInterface:
    def read_in(self, path:str) -> object:
        return object()
    def write_to(self, data:object|str, path:str) -> None:
        return None
    
class JSONDB(DBInterface):
    def read_in(self, path:str) -> object:
        with open(path, "r") as f:
            data = json.load(f)
        return data
    def write_to(self, data:object|str, path:str) -> None:
        with open(path, "w") as f:
            json.dump(data, f, indent=4)
        return None