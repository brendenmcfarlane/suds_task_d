# python3 -m streamlit run frameworks/script.py
import streamlit as st
import pandas as pd
import graphviz
from frameworks.workflow_node import WorkFlowNode as WorkFlowNode
import json


test_path = "datasets/chartqa/results.json"
question_index = 0
workflow_index = 0
with open(test_path, "r") as f:
        traces = json.load(f)

question_key = st.radio(
    "Select A Question To View MAS Trajectories",
    traces.keys(),
    format_func=lambda k: traces[k]["0"][0]["question"],
    index=0,
)

trace = traces[question_key][str(workflow_index)]

root = WorkFlowNode("root graph")
root._adjacencies = trace[0]["topology"]
root._transcript = trace[-1]["state_after"]
for workflow_key in traces[question_key].keys():
     if workflow_key == "0":
          pass
     else:
        child = WorkFlowNode("child " + workflow_key)
        root.add_child(child)
        child._adjacencies  = traces[question_key][workflow_key][0]["topology"]
        child._transcript = traces[question_key][workflow_key][-1]["state_after"]



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
st.header("Workflow Search Space Graph")
recursively_update_search_space(workflow_search_space, graph_dict, convo_dict, root)
st.graphviz_chart(workflow_search_space)
st.divider()

st.header("Compare Workflows Below")
col1, col2 = st.columns(2)
left_key = col1.radio(
    "Select Left Graph",
    graph_dict.keys(),
    index=None,
)
if isinstance(left_key, str):
    left_graph = graph_dict.get(left_key)
    col1.graphviz_chart(left_graph)
    col1.subheader("Transcript of Agent Prompts and Messages")
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
    col2.subheader("Transcript of Agent Prompts and Messages")
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