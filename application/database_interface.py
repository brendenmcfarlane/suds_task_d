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
    def to_string(self, data:object|str) -> str:
        result = json.dumps(data, indent=4)
        return result
    def from_string(self, json_str) -> dict|list:
        # json_str = json_str.replace("\n", "")
        result = json.loads(json_str)
        return result
    
def main():
    json_db = JSONDB()
    test_obj = {"first": ["1", "2", "3"], "second": ["4", "5", "6"]}
    output = json_db.to_string(test_obj)
    print(output)
    print(test_obj)
    print("")

    from_str_output = json_db.from_string("{'value': 1.0,'origin_risk': 'none_or_low','responsible_agent_guess': 'none_or_low','reason': 'The planner correctly computed the total eggs needed based on the given numbers, so the final answer is correct.'}")

if __name__ == "__main__": main()