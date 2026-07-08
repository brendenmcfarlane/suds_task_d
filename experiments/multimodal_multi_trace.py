#manuallly send image to perception, ground truth to verifier

import time
from src.query import MultiMediaQuery
from src.agent_node import AgentNode
import application.interactors, application.database_interface, application.agent_repo, application.event_bus, application.transcript
import src.agent_node, src.mas
import numpy as np
import pandas as pd


def main():
    json_db = application.database_interface.JSONDB()
    query_path = "datasets/chartqa/questions.json"
    query_importer = application.interactors.ImportQueriesInteractor(query_path, json_db)
    queries = query_importer.import_queries_uc()
    
    mas_paths = ["datasets/chartqa/mas_clean.json", 
                 "datasets/chartqa/mas_faulty_perception.json", 
                 "datasets/chartqa/mas_faulty_handoff.json", 
                 "datasets/chartqa/mas_faulty_reasoning.json"]
    results = {}
    # scores = {} TODO: convert to ndarray using numpy.empty()
    for i in range(len(queries[:])):
        results[i] = {}
        # scores[i] = {} 
        for j in range(len(mas_paths[:])):
            q = queries[i]
            mas_path = mas_paths[j]
            agents_path = "datasets/chartqa/agents.json"

            agent_repo = application.agent_repo.AgentRepo()
            event_bus = application.event_bus.EventBus()

            transcript = application.transcript.Transcript()
            action_listener = application.transcript.AgentActionListener(transcript)
            mas_listener = application.transcript.MASStateListener(transcript)
            event_bus.subscribe(src.agent_node.AddAgentAction, action_listener)
            event_bus.subscribe(src.mas.MASStateUpdate, mas_listener)

            

            agents_importer = application.interactors.ImportAgentsInteractor(agents_path, json_db, agent_repo, event_bus)
            agents_importer.import_agents_uc()

            mas_builder = application.interactors.BuildMASFromSpecsInteractor(mas_path, json_db, agent_repo, event_bus)
            mas = mas_builder.build_mas_from_specs_uc()
            event_bus.subscribe(src.agent_node.AddAgentAction, mas)

            trace_executor = application.interactors.ExecuteFullTraceInteractor(mas, q, agent_repo)

            # =======
            perception = agent_repo.get_agent("perception")
            if isinstance(q, MultiMediaQuery) and isinstance(perception, AgentNode):
                perception.receive_message({"type": "image_url", "image_url": q.get_image_path()})

            verifier = agent_repo.get_agent("verifier")
            gt = q.get_ground_truth()
            if isinstance(verifier, AgentNode) and isinstance(gt, str):
                verifier.receive_message({"type": "text", "text": "ground truth: " + gt})

            # ======

            trace_executor.execute_full_trace_uc()

            results[i][j] = transcript.get_steps()
    num_agents = len(agent_repo._repo)
    scores = pd.DataFrame(columns=['question', 'workflow', 'step', 'agent', 'metric', 'value'])
    
    for query_ind in results.keys():
        for wrkflw_ind in results[query_ind].keys():
            for part_tran_ind in range(len(results[query_ind][wrkflw_ind])):
                # convert results[i][j][:k+1] to json_str
                json_str = json_db.to_string(results[query_ind][wrkflw_ind][:part_tran_ind+1])
                agents_path = "datasets/chartqa/llm_judge.json" 

                agent_repo = application.agent_repo.AgentRepo()

                agents_importer = application.interactors.ImportAgentsInteractor(agents_path, json_db, agent_repo, application.event_bus.EventBus())
                agents_importer.import_agents_uc()

                llj_judge_executor = application.interactors.ExecuteLLMJudgeInteractor(agent_repo)
                v = llj_judge_executor.execute_judge_llm_uc("judge", json_str)
                results[query_ind][wrkflw_ind][part_tran_ind]["V"] = json_db.from_string(v) # removed [:part_tran_ind+1]
                #scores[query_ind, wrkflw_ind, part_tran_ind] = results[query_ind][wrkflw_ind][:part_tran_ind+1][part_tran_ind]["V"]["value"]
                scores.loc[len(scores)] = {'question': f"question {query_ind}", 
                                           'workflow': mas_paths[wrkflw_ind], 
                                           'step': part_tran_ind, 
                                           'agent': results[query_ind][wrkflw_ind][part_tran_ind]["agent"], 
                                           'metric': "raw V", 
                                           'value': results[query_ind][wrkflw_ind][part_tran_ind]["V"]["value"]} # removed [:part_tran_ind+1]
                if part_tran_ind > 0:
                    scores.loc[len(scores)] = {'question': f"question {query_ind}", 
                                            'workflow': mas_paths[wrkflw_ind], 
                                            'step': part_tran_ind, 
                                            'agent': results[query_ind][wrkflw_ind][part_tran_ind]["agent"], 
                                            'metric': "delta V", 
                                            'value': results[query_ind][wrkflw_ind][part_tran_ind]["V"]["value"] - results[query_ind][wrkflw_ind][part_tran_ind - 1]["V"]["value"]}

    
    # for query_ind in results.keys():
    #     for wrkflw_ind in results[query_ind].keys():
    #         for part_tran_ind in range(len(results[query_ind][wrkflw_ind])):
    #             # calculate diffeernce metric
    scores.to_csv('scores.csv')


    ex_time = str(time.time_ns())
    json_db.write_to(results, "datasets/chartqa/archived_results/results_" + ex_time + ".json")
    json_db.write_to(results, "datasets/chartqa/results.json")
    

    

if __name__ == "__main__": main()



