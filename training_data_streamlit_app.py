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
pkl_db = PKLDB()
trajectory = pkl_db.read_in(test_path)
# init conditions
question_index = 0
workflow_index = 0
# select question
# question_key = st.radio(
#     "Select A Question To View MAS Trajectories",
#     traces.keys(),
#     format_func=lambda k: traces[k]["0"][0]["question"],
#     index=0,
# )

# 
def recursively_update_trajectories(state_space: graphviz.Digraph, 
                                    root_node: MASNode,
                                    mas_state_list: list):
    i = len(mas_state_list)
    state_space.node(str(i), f"{root_node._acting_agent_id}") # \nResponse: {root_node._action_content}
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
    t = mas_state_list[left_key].get_partial_transcript()
    col1.write(t)

if isinstance(right_key, int):
    col2.subheader("Transcript")
    t = mas_state_list[right_key].get_partial_transcript()
    col2.write(t)