# python3 -m streamlit run frameworks/script.py
import streamlit as st
import pandas as pd
import graphviz
from frameworks.workflow_node import WorkFlowNode as WorkFlowNode
import json

test_path = "frameworks/outputs2.json"
question_index = 0
workflow_index = 0
with open(test_path, "r") as f:
        traces = json.load(f)
trace = traces[str(question_index)][str(workflow_index)]

root = WorkFlowNode("graph_one")
child1 = WorkFlowNode("graph_two")
# child2 = WorkFlowNode("graph_three")
root.add_child(child1)
# root.add_child(child2)
root._adjacencies = trace[0]["topology"]
# [("question", "planner"), 
#                      ("question", "reader"), 
#                      ("question", "verifier"),
#                      ("planner", "solver"),
#                      ("reader", "solver"),
#                      ("solver", "verifier")]
root._transcript = trace[-1]["state_after"]
child1._adjacencies  = traces[str(question_index)][str(1)][0]["topology"]

# [("question", "planner"), 
#                      ("question", "reader"), 
#                      ("question", "verifier"),
#                      ("planner", "reader"),
#                      ("reader", "solver"),
#                      ("solver", "verifier")]
# child2._adjacencies = [("question", "planner"), 
#                      ("question", "reader"), 
#                      ("planner", "solver"),
#                      ("reader", "solver"),
#                      ("solver", "verifier")]
child1._transcript = traces[str(question_index)][str(1)][-1]["state_after"]
# child2._transcript = trace[:2]

def recursively_update_search_space(ss:graphviz.Digraph, graph_dict, convo_dict, wfn: WorkFlowNode):
    workflow = graphviz.Digraph()
    for edge in wfn._adjacencies:
        workflow.edge(edge[0], edge[1])
    graph_dict[wfn._id] = workflow
    convo_dict[wfn._id] = wfn._transcript
    for child in wfn._children:
        recursively_update_search_space(ss, graph_dict, convo_dict, child)
        ss.edge(wfn._id, child._id)



workflow_search_space = graphviz.Digraph()
graph_dict = {}
convo_dict = {}
recursively_update_search_space(workflow_search_space, graph_dict, convo_dict, root)
st.graphviz_chart(workflow_search_space)
st.divider()


col1, col2 = st.columns(2)
left_key = col1.radio(
    "Select Left Graph",
    graph_dict.keys(),
    index=None,
)
if isinstance(left_key, str):
    left_graph = graph_dict.get(left_key)
    col1.graphviz_chart(left_graph)
    left_convo = convo_dict[left_key]
    col1.json(left_convo)
else:
    col1.write("Select a Workflow to View")

right_key = col2.radio(
    "Select Right Graph",
    graph_dict.keys(),
    index=None,
)
if isinstance(right_key, str):
    right_graph = graph_dict.get(right_key)
    col2.graphviz_chart(right_graph)
    right_convo = convo_dict[right_key]
    col2.json(right_convo)
else:
    col2.write("Select a Workflow to View")


# convo_dict = {"graph_one": clean_trace[2].get("state_after"), 
#               "graph_two": clean_trace[3].get("state_after"), 
#               "graph_three": clean_trace[4].get("state_after")}

# if isinstance(left_key, str):
#     left_graph = graph_dict.get(left_key)
#     col1.graphviz_chart(left_graph)
# else:
#     col1.write("Select a Workflow to View")

# if isinstance(right_key, str):
#     right_graph = graph_dict.get(right_key)
#     col2.graphviz_chart(right_graph)
# else:
#     col2.write("Select a Workflow to View")



# workflow_search_space.edge("graph_one", "graph_two")
# workflow_search_space.edge("graph_one", "graph_three")
# st.graphviz_chart(workflow_search_space)
# st.divider() #horitontal line

# # Create a graphlib graph object
# G = graphviz.Digraph()
# G.edge("question", "planner")
# G.edge("que

# I = graphviz.Digraph()
# I.edge("question", "planner")
# I.edge("question", "reader")
# I.edge("planner", "solver")
# I.edge("reader", "solver")
# I.edge("solver", "verifier")

# graph_dict = {"graph_one": G, "graph_two": H, "graph_three": I}




# G.edge("question", "verifier")
# G.edge("planner", "solver")
# G.edge("reader", "solver")
# G.edge("solver", "verifier")

# H = graphviz.Digraph()
# H.edge("question", "planner")
# H.edge("question", "reader")
# H.edge("question", "verifier")
# H.edge("planner", "reader")
# H.edge("planner", "solver")
# H.edge("reader", "solver")
# H.edge("solver", "verifier")                   ("planner", "solver"),