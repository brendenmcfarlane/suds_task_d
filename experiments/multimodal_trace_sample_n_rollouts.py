import time
from src.query import Query, MultiMediaQuery
from src.mas_node import MASNode
from src.mas import MASStateUpdate
from src.agent_node import AddAgentAction, AgentNode
from src.events import QueueEventBus
from application.agent_repo import AgentRepo
from application.interactors import ExecuteAgentInteractor, ImportAgentsInteractor, BuildMASFromSpecsInteractor, ImportQueriesInteractor, SampleResponsesInteractor, ExecuteLLMSelectorInteractor
from application.database_interface import JSONDB, PKLDB

def main():
    # hyperparameters
    n_rollouts = 3
    # Import Queries
    json_db = JSONDB()
    pkl_db = PKLDB()
    query_path = "datasets/chartqa/questions.json"
    query_importer = ImportQueriesInteractor(query_path, json_db)
    queries = query_importer.import_queries_uc()

    # import agents
    agents_path = "datasets/chartqa/agents.json"
    judge_path = "datasets/chartqa/llm_judge.json"
    repo = AgentRepo()
    bus = QueueEventBus(n_rollouts)
    agent_importer = ImportAgentsInteractor(agents_path, json_db, repo, bus)
    agent_importer.import_agents_uc()
    judge_importer = ImportAgentsInteractor(judge_path, json_db, repo, QueueEventBus())
    judge_importer.import_agents_uc()

    # build mas
    mas_path = "datasets/chartqa/mas_clean.json"
    
    db_importer = BuildMASFromSpecsInteractor(mas_path, json_db, repo, bus)
    mas = db_importer.build_mas_from_specs_uc()

    

    # mas node
    mas_node = MASNode(parent=None)
    bus.subscribe(MASStateUpdate, mas_node)

    # experiment configuration
    query = queries[0]
    seed = 27

    # trajectory execution
    perception = repo.get_agent("perception")
    if isinstance(query, MultiMediaQuery) and isinstance(perception, AgentNode):
        perception.receive_message({"type": "image_url", "image_url": query.get_image_path()})

    mas.set_question(query.get_question())
    acting_agent = mas.next_agent()
    curr_node = mas_node
    while acting_agent is not None:
        # set up child node for this state
        for i in range(n_rollouts):
            child_node = curr_node.create_child()
            bus.subscribe(AddAgentAction, child_node)
            bus.subscribe(MASStateUpdate, child_node)
        # execute agent n times
        agent_executor = SampleResponsesInteractor(repo)
        outputs = agent_executor.sample_n_responses_uc(n_rollouts, acting_agent)
        json_outputs = [json_db.to_string(o) for o in outputs]
        # pick best output
        #TODO: reset the judge, give image, remove other context
        llm_selector = ExecuteLLMSelectorInteractor(repo)
        verdict = llm_selector.execute_judge_llm_uc("vlm-preference-judge", json_outputs)
        parsed_verdict = json_db.from_string(verdict)
        best_output_ind = int(parsed_verdict["agent_selected"]) - 1
        best_output = outputs[best_output_ind]
        # update agent inputs
        for adj in mas.get_adjacencies(acting_agent):
            adj_agent = repo.get_agent(adj)
            if not (adj_agent is None):
                for o in best_output:
                    adj_agent.receive_message(o)
        # iterate
        acting_agent = mas.next_agent()
        curr_node = curr_node.get_children()[best_output_ind]
    # transcript = curr_node.get_partial_transcript()
    curr_node = mas_node
    while True:
        print(' ')
        print(f"Current Node Question: {curr_node._question}")
        print(f"Current Node Topology: {curr_node._topology}")
        print(f"Current Node Acting Agent: {curr_node._acting_agent_id}")
        print(f"Current Node Action Type: {curr_node._action_type}")
        print(f"Current Node Action Content: {curr_node._action_content}")
        print(f"Current Node Children Count: {len(curr_node.get_children())}")
        print(f"Current Node Transcript: {curr_node.get_partial_transcript()}")
        if len(curr_node.get_children()) == 0:
            break
        curr_node = curr_node.get_children()[0]

    for i, child in enumerate(mas_node.get_children()):
        print(f"Child {i} Question: {child._question}")
        print(f"Child {i} Topology: {child._topology}")
        print(f"Child {i} Acting Agent: {child._acting_agent_id}")
        print(f"Child {i} Action Type: {child._action_type}")
        print(f"Child {i} Action Content: {child._action_content}")
        print(f"Child {i} Children Count: {len(child.get_children())}")
        print(f"Child {i} Transcript: {child.get_partial_transcript()}")
    print(' ')
    ex_time = str(time.time_ns())
    pkl_db.write_to(mas_node, "datasets/chartqa/archived_results/results_" + ex_time + ".pkl")
    pkl_db.write_to(mas_node, "datasets/chartqa/results.pkl")

if __name__ == "__main__":
    main()

