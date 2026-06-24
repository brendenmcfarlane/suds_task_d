# python3 -m streamlit run frameworks/script.py
import streamlit as st
import pandas as pd
import graphviz
import test_imp

class WorkFlowNode():
    def __init__(self, key:str):
        self._id = key
        self._children = []
        self._transcript = []
        self._adjacencies = []

    def get_workflow(self):
        return self._adjacencies

    def add_child(self, child):
        self._children.append(child)

    def get_children(self):
        return self._children
    
    def add_adjacency(self, adj):
        self._adjacencies.append(adj)

    def set_transcript(self, transcript:list[dict]):
        self._transcript = transcript

clean_trace = [
    {
        "question": "The Rotary Club is holding its annual fundraising Omelet Breakfast, with tickets sold in advance. The tickets come in different price levels, for young children, older children, adults, and seniors. This year they sold 53 small children tickets, 35 older children tickets, 75 adult tickets, and 37 senior tickets. To figure out how many eggs they need to buy, the club estimates that small children can eat a half omelet, older children can eat a whole omelet, adults will eat two omelets, and seniors will eat one and a half omelets. Just to be on the safe side, they get enough eggs to make 25 extra omelets. If they use 2 eggs for each omelet, how many eggs will they need to buy?",
        "step": 1,
        "agent": "planner",
        "state_before": [],
        "action": {
            "type": "You are the Planner. Propose a concise plan to solve the task.",
            "content": [
                {
                    "type": "text",
                    "text": "They will need to buy 584 eggs."
                }
            ]
        },
        "state_after": [
            "Agent: planner\n>>Input Prompt: You are the Planner. Propose a concise plan to solve the task.\n>>Response: [{'type': 'text', 'text': 'They will need to buy 584 eggs.'}]"
        ]
    },
    {
        "question": "The Rotary Club is holding its annual fundraising Omelet Breakfast, with tickets sold in advance. The tickets come in different price levels, for young children, older children, adults, and seniors. This year they sold 53 small children tickets, 35 older children tickets, 75 adult tickets, and 37 senior tickets. To figure out how many eggs they need to buy, the club estimates that small children can eat a half omelet, older children can eat a whole omelet, adults will eat two omelets, and seniors will eat one and a half omelets. Just to be on the safe side, they get enough eggs to make 25 extra omelets. If they use 2 eggs for each omelet, how many eggs will they need to buy?",
        "step": 2,
        "agent": "reader",
        "state_before": [
            "Agent: planner\n>>Input Prompt: You are the Planner. Propose a concise plan to solve the task.\n>>Response: [{'type': 'text', 'text': 'They will need to buy 584 eggs.'}]"
        ],
        "action": {
            "type": "You are the Reader. Extract key facts for another agent to use to generate the final answer.",
            "content": [
                {
                    "type": "text",
                    "text": "Key facts extracted from the problem:\n\n- Small children tickets sold: 53\n- Older children tickets sold: 35\n- Adult tickets sold: 75\n- Senior tickets sold: 37\n- Omelet consumption per person: small children = 0.5, older children = 1, adults = 2, seniors = 1.5\n- Extra omelets for safety: 25\n- Eggs per omelet: 2\n\nCalculate total omelets needed: (53 \u00d7 0.5) + (35 \u00d7 1) + (75 \u00d7 2) + (37 \u00d7 1.5) + 25. Then multiply by 2 to find total eggs."
                }
            ]
        },
        "state_after": [
            "Agent: planner\n>>Input Prompt: You are the Planner. Propose a concise plan to solve the task.\n>>Response: [{'type': 'text', 'text': 'They will need to buy 584 eggs.'}]",
            "Agent: reader\n>>Input Prompt: You are the Reader. Extract key facts for another agent to use to generate the final answer.\n>>Response: [{'type': 'text', 'text': 'Key facts extracted from the problem:\\n\\n- Small children tickets sold: 53\\n- Older children tickets sold: 35\\n- Adult tickets sold: 75\\n- Senior tickets sold: 37\\n- Omelet consumption per person: small children = 0.5, older children = 1, adults = 2, seniors = 1.5\\n- Extra omelets for safety: 25\\n- Eggs per omelet: 2\\n\\nCalculate total omelets needed: (53 \u00d7 0.5) + (35 \u00d7 1) + (75 \u00d7 2) + (37 \u00d7 1.5) + 25. Then multiply by 2 to find total eggs.'}]"
        ]
    },
    {
        "question": "The Rotary Club is holding its annual fundraising Omelet Breakfast, with tickets sold in advance. The tickets come in different price levels, for young children, older children, adults, and seniors. This year they sold 53 small children tickets, 35 older children tickets, 75 adult tickets, and 37 senior tickets. To figure out how many eggs they need to buy, the club estimates that small children can eat a half omelet, older children can eat a whole omelet, adults will eat two omelets, and seniors will eat one and a half omelets. Just to be on the safe side, they get enough eggs to make 25 extra omelets. If they use 2 eggs for each omelet, how many eggs will they need to buy?",
        "step": 3,
        "agent": "solver",
        "state_before": [
            "Agent: planner\n>>Input Prompt: You are the Planner. Propose a concise plan to solve the task.\n>>Response: [{'type': 'text', 'text': 'They will need to buy 584 eggs.'}]",
            "Agent: reader\n>>Input Prompt: You are the Reader. Extract key facts for another agent to use to generate the final answer.\n>>Response: [{'type': 'text', 'text': 'Key facts extracted from the problem:\\n\\n- Small children tickets sold: 53\\n- Older children tickets sold: 35\\n- Adult tickets sold: 75\\n- Senior tickets sold: 37\\n- Omelet consumption per person: small children = 0.5, older children = 1, adults = 2, seniors = 1.5\\n- Extra omelets for safety: 25\\n- Eggs per omelet: 2\\n\\nCalculate total omelets needed: (53 \u00d7 0.5) + (35 \u00d7 1) + (75 \u00d7 2) + (37 \u00d7 1.5) + 25. Then multiply by 2 to find total eggs.'}]"
        ],
        "action": {
            "type": "You are the Solver. Carry out the plan and compute results given the facts",
            "content": [
                {
                    "type": "text",
                    "text": "The total number of eggs needed is 584."
                }
            ]
        },
        "state_after": [
            "Agent: planner\n>>Input Prompt: You are the Planner. Propose a concise plan to solve the task.\n>>Response: [{'type': 'text', 'text': 'They will need to buy 584 eggs.'}]",
            "Agent: reader\n>>Input Prompt: You are the Reader. Extract key facts for another agent to use to generate the final answer.\n>>Response: [{'type': 'text', 'text': 'Key facts extracted from the problem:\\n\\n- Small children tickets sold: 53\\n- Older children tickets sold: 35\\n- Adult tickets sold: 75\\n- Senior tickets sold: 37\\n- Omelet consumption per person: small children = 0.5, older children = 1, adults = 2, seniors = 1.5\\n- Extra omelets for safety: 25\\n- Eggs per omelet: 2\\n\\nCalculate total omelets needed: (53 \u00d7 0.5) + (35 \u00d7 1) + (75 \u00d7 2) + (37 \u00d7 1.5) + 25. Then multiply by 2 to find total eggs.'}]",
            "Agent: solver\n>>Input Prompt: You are the Solver. Carry out the plan and compute results given the facts\n>>Response: [{'type': 'text', 'text': 'The total number of eggs needed is 584.'}]"
        ]
    },
    {
        "question": "The Rotary Club is holding its annual fundraising Omelet Breakfast, with tickets sold in advance. The tickets come in different price levels, for young children, older children, adults, and seniors. This year they sold 53 small children tickets, 35 older children tickets, 75 adult tickets, and 37 senior tickets. To figure out how many eggs they need to buy, the club estimates that small children can eat a half omelet, older children can eat a whole omelet, adults will eat two omelets, and seniors will eat one and a half omelets. Just to be on the safe side, they get enough eggs to make 25 extra omelets. If they use 2 eggs for each omelet, how many eggs will they need to buy?",
        "step": 4,
        "agent": "verifier",
        "state_before": [
            "Agent: planner\n>>Input Prompt: You are the Planner. Propose a concise plan to solve the task.\n>>Response: [{'type': 'text', 'text': 'They will need to buy 584 eggs.'}]",
            "Agent: reader\n>>Input Prompt: You are the Reader. Extract key facts for another agent to use to generate the final answer.\n>>Response: [{'type': 'text', 'text': 'Key facts extracted from the problem:\\n\\n- Small children tickets sold: 53\\n- Older children tickets sold: 35\\n- Adult tickets sold: 75\\n- Senior tickets sold: 37\\n- Omelet consumption per person: small children = 0.5, older children = 1, adults = 2, seniors = 1.5\\n- Extra omelets for safety: 25\\n- Eggs per omelet: 2\\n\\nCalculate total omelets needed: (53 \u00d7 0.5) + (35 \u00d7 1) + (75 \u00d7 2) + (37 \u00d7 1.5) + 25. Then multiply by 2 to find total eggs.'}]",
            "Agent: solver\n>>Input Prompt: You are the Solver. Carry out the plan and compute results given the facts\n>>Response: [{'type': 'text', 'text': 'The total number of eggs needed is 584.'}]"
        ],
        "action": {
            "type": "You are the Verifier. Double-check the result and produce the final answer only.",
            "content": [
                {
                    "type": "text",
                    "text": "The total number of eggs needed is 584."
                }
            ]
        },
        "state_after": [
            "Agent: planner\n>>Input Prompt: You are the Planner. Propose a concise plan to solve the task.\n>>Response: [{'type': 'text', 'text': 'They will need to buy 584 eggs.'}]",
            "Agent: reader\n>>Input Prompt: You are the Reader. Extract key facts for another agent to use to generate the final answer.\n>>Response: [{'type': 'text', 'text': 'Key facts extracted from the problem:\\n\\n- Small children tickets sold: 53\\n- Older children tickets sold: 35\\n- Adult tickets sold: 75\\n- Senior tickets sold: 37\\n- Omelet consumption per person: small children = 0.5, older children = 1, adults = 2, seniors = 1.5\\n- Extra omelets for safety: 25\\n- Eggs per omelet: 2\\n\\nCalculate total omelets needed: (53 \u00d7 0.5) + (35 \u00d7 1) + (75 \u00d7 2) + (37 \u00d7 1.5) + 25. Then multiply by 2 to find total eggs.'}]",
            "Agent: solver\n>>Input Prompt: You are the Solver. Carry out the plan and compute results given the facts\n>>Response: [{'type': 'text', 'text': 'The total number of eggs needed is 584.'}]",
            "Agent: verifier\n>>Input Prompt: You are the Verifier. Double-check the result and produce the final answer only.\n>>Response: [{'type': 'text', 'text': 'The total number of eggs needed is 584.'}]"
        ]
    }
]
root = WorkFlowNode("graph_one")
child1 = WorkFlowNode("graph_two")
child2 = WorkFlowNode("graph_three")
root.add_child(child1)
root.add_child(child2)
root._adjacencies = [("question", "planner"), 
                     ("question", "reader"), 
                     ("question", "verifier"),
                     ("planner", "solver"),
                     ("reader", "solver"),
                     ("solver", "verifier")]
root._transcript = clean_trace[:]
child1._adjacencies = [("question", "planner"), 
                     ("question", "reader"), 
                     ("question", "verifier"),
                     ("planner", "reader"),
                     ("reader", "solver"),
                     ("solver", "verifier")]
child2._adjacencies = [("question", "planner"), 
                     ("question", "reader"), 
                     ("planner", "solver"),
                     ("reader", "solver"),
                     ("solver", "verifier")]
child1._transcript = clean_trace[:-1]
child2._transcript = clean_trace[:2]

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
    col1.write(left_convo)
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
    col2.write(right_convo)
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