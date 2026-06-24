#from application.interactors import ImportAgentsI, ImportQueriesI, ExecuteFullTraceI, BuildMASFromSpecsI, SetupInputData
import application.interactors, application.database_interface, application.agent_repo, application.event_bus, application.transcript
import src.agent_node, src.mas

# class CleanTraceController:
#     def __init__(self, iai:ImportAgentsI, iqi:ImportQueriesI, efti:ExecuteFullTraceI, bmfsi:BuildMASFromSpecsI, data: SetupInputData):
#         self._agent_importer = iai
#         self._query_import = iqi
#         self._trace_executor = efti
#         self._mas_builder = bmfsi
#         self._data = data

#     def execute(self):
#         self._agent_importer.import_agents_uc()
#         self._query_import.import_queries_uc()
#         self._trace_executor = efti
#         self._mas_builder = bmfsi
#         self._data = data

def main():
    query_path = "tests/clean_trace/sample_questions.json"
    agents_path = "tests/clean_trace/sample_agents.json"
    mas_path = "tests/clean_trace/sample_mas.json"

    json_db = application.database_interface.JSONDB()
    agent_repo = application.agent_repo.AgentRepo()
    event_bus = application.event_bus.EventBus()

    transcript = application.transcript.Transcript()
    action_listener = application.transcript.AgentActionListener(transcript)
    mas_listener = application.transcript.MASStateListener(transcript)
    event_bus.subscribe(src.agent_node.AddAgentAction, action_listener)
    event_bus.subscribe(src.mas.MASStateUpdate, mas_listener)

    query_importer = application.interactors.ImportQueriesInteractor(query_path, json_db)
    queries = query_importer.import_queries_uc()
    q = queries[0]

    agents_importer = application.interactors.ImportAgentsInteractor(agents_path, json_db, agent_repo, event_bus)
    agents_importer.import_agents_uc()

    mas_builder = application.interactors.BuildMASFromSpecsInteractor(mas_path, json_db, agent_repo, event_bus)
    mas = mas_builder.build_mas_from_specs_uc()
    event_bus.subscribe(src.agent_node.AddAgentAction, mas)

    trace_executor = application.interactors.ExecuteFullTraceInteractor(mas, q, agent_repo)
    trace_executor.execute_full_trace_uc()

    steps = transcript.get_steps()
    json_db.write_to(steps, "tests/clean_trace/output.json")

    

if __name__ == "__main__": main()


# class ExecuteFullTraceInteractor(ExecuteFullTraceI):
#     def execute_full_trace_uc(self) -> None:
#         #TODO: reset MAS fn (or multiple traces)
#         self._mas.set_question(self._question)
#         self._mas.plan_trajectory()
#         curr_actor = self._mas.next_agent()
#         agent_executor = ExecuteAgentInteractor(self._repo)
#         while curr_actor:
#             agent_executor.execute_agent_uc(curr_actor)
#             for adj in self._mas.get_adjacencies(curr_actor):
#                 adj_agent = self._repo.get_agent(adj)
#                 if not (adj_agent is None):
#                     curr_agent = self._repo.get_agent(curr_actor)
#                     adj_agent.receive_message(curr_agent.get_output())
#             curr_actor = self._mas.next_agent()

