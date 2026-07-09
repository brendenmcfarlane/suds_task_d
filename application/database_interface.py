from abc import ABC, abstractmethod
import json
import pickle

class DBInterface(ABC):
    @abstractmethod
    def read_in(self, path:str) -> object:
        pass

    @abstractmethod
    def write_to(self, data:object|str, path:str) -> None:
        pass
    
class JSONDB(DBInterface):
    def read_in(self, path:str) -> object:
        """ Precondition: path is a .json file
        """
        with open(path, "r") as f:
            data = json.load(f)
        return data
    def write_to(self, data:object|str, path:str) -> None:
        """ Precondition: path is a .json file
        """
        with open(path, "w") as f:
            json.dump(data, f, indent=4)
        return None
    def to_string(self, data:object|str) -> str:
        result = json.dumps(data, indent=4)
        return result
    def from_string(self, json_str) -> dict|list:
        result = json.loads(json_str)
        return result

class PKLDB(DBInterface):
    def read_in(self, path: str) -> object:
        """ Precondition: path is a .pkl file
        """
        with open(path, "rb") as file:
            loaded_data = pickle.load(file)
        return loaded_data
    
    def write_to(self, data: object | str, path: str) -> None:
        """ Precondition: path is a .pkl file
        """
        with open(path, "wb") as file:
            pickle.dump(data, file)
    
def main():
    json_db = JSONDB()
    test_obj = {"first": ["1", "2", "3"], "second": ["4", "5", "6"]}
    output = json_db.to_string(test_obj)
    print(output)
    print(test_obj)
    print("")

    from_str_output = json_db.from_string("{'value': 1.0,'origin_risk': 'none_or_low','responsible_agent_guess': 'none_or_low','reason': 'The planner correctly computed the total eggs needed based on the given numbers, so the final answer is correct.'}")


if __name__ == "__main__": main()