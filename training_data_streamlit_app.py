# python3 -m streamlit run frameworks/script.py
import streamlit as st
import pandas as pd
import graphviz
import json
from src.mas_node import MASNode # TODO: create interface or smth
from application.database_interface import PKLDB

st.set_page_config(layout="wide")
# upload training data
test_path = "datasets/chartqa/results.pkl"
test_path = "datasets/chartqa/archived_results/results_1784211546363239194_tuning_results.pkl"
pkl_db = PKLDB()
trajectories = pkl_db.read_in(test_path)
assert isinstance(trajectories, dict)
# init conditions
hyp_key = st.radio(
    "Select Hyperparameter Set",
    list(trajectories.keys())[:-1], #TODO: fix this so it is resolvedd manually
    key=f"action_{5}"
)
query_key = st.radio(
    "Select Question",
    list(trajectories[hyp_key].keys()),
    captions=["What was the average annual total income per household of those in the top decile group?",
              "Which gender is represented by the red color line?",
              "What's the average of two smallest bar?",
              "What did 92 percent of the top 400 charities and NPOs use for their organization?",
              "What's the percentage of revenue contributes by people under 44?",
              "What is the median of the three least raised biotech venture capitals?",
              "Between which two years , the GDP of New Zealand is maximum?",
              "What is the total of Bad and Good in the row Remain?",
              "What was the percentage of school children who read eBooks outside of class in 2016?",
              "Which country has a higher share of the population using safely managed drinking water over the years?"],
    key=f"action_{3}"
)

workflow_key = st.radio(
    "Select MAS Workflow",
    list(trajectories[hyp_key][query_key].keys()),
    captions=["datasets/chartqa/mas_clean.json", 
              "datasets/chartqa/mas_faulty_handoff.json", 
              "datasets/chartqa/mas_faulty_reasoning.json", 
              "datasets/chartqa/mas_faulty_perception.json"],
    key=f"action_{4}"
)

trajectory = trajectories[hyp_key][query_key][workflow_key]
def recursively_update_trajectories(state_space: graphviz.Digraph, 
                                    root_node: MASNode,
                                    mas_state_list: list):
    i = len(mas_state_list)
    state_space.node(str(i), f"{i}: {root_node._acting_agent_id}") # \nResponse: {root_node._action_content}
    mas_state_list.append(root_node)

    for c in root_node.get_children():
        j = recursively_update_trajectories(state_space, c, mas_state_list)
        state_space.edge(str(i), str(j))
    return i

trajectory_search_space = graphviz.Digraph()
trajectory_search_space.attr(
    rankdir="TB",      # Top to bottom
    ranksep="1.2",     # Vertical spacing
    nodesep="0.6",     # Horizontal spacing
    splines="ortho",   # Optional: right-angle edges
)
mas_state_list = []
recursively_update_trajectories(trajectory_search_space, trajectory, mas_state_list)
st.graphviz_chart(trajectory_search_space)

st.header("Compare Trajectories Below")
col1, col2 = st.columns(2)
left_key = col1.radio(
    "Select A State To View Partial Transcript",
    range(len(mas_state_list)),
    index=0,
    key=f"action_{1}"
)
right_key = col2.radio(
    "Select A State To View Partial Transcript",
    range(len(mas_state_list)),
    index=0,
    key=f"action_{2}"
)

if isinstance(left_key, int):
    col1.subheader("Transcript")
    t = []
    out = mas_state_list[left_key].get_partial_transcript()
    for o in out:
        t.extend(o.split("\n"))
    for line in t:
        col1.write(line)

if isinstance(right_key, int):
    col2.subheader("Transcript")
    t = []
    out = mas_state_list[right_key].get_partial_transcript()
    for o in out:
        t.extend(o.split("\n"))
    for line in t:
        col2.write(line)