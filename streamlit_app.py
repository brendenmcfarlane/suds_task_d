# python3 -m streamlit run frameworks/script.py
import streamlit as st
import pandas as pd
import graphviz

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
st.write("Here's our first attempt at using data to create a table:")
st.write(pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
}))
y = st.slider('y')  
st.write(y, 'squared is', y * y)
st.write(clean_trace)
st.divider() #horitontal line

# Create a graphlib graph object
G = graphviz.Digraph()
G.edge("question", "planner")
G.edge("question", "reader")
G.edge("question", "verifier")
G.edge("planner", "solver")
G.edge("reader", "solver")
G.edge("solver", "verifier")

H = graphviz.Digraph()
H.edge("question", "planner")
H.edge("question", "reader")
H.edge("question", "verifier")
H.edge("planner", "reader")
H.edge("planner", "solver")
H.edge("reader", "solver")
H.edge("solver", "verifier")

I = graphviz.Digraph()
I.edge("question", "planner")
I.edge("question", "reader")
I.edge("planner", "solver")
I.edge("reader", "solver")
I.edge("solver", "verifier")

graph_dict = {"graph_one": G, "graph_two": H, "graph_three": I}
col1, col2 = st.columns(2)
left_key = col1.radio(
    "Select Left Graph",
    graph_dict.keys(),
    index=None,
)
if isinstance(left_key, str):
    left_graph = graph_dict.get(left_key)
    col1.graphviz_chart(left_graph)

right_key = col2.radio(
    "Select Right Graph",
    graph_dict.keys(),
    index=None,
)
if isinstance(right_key, str):
    right_graph = graph_dict.get(right_key)
    col2.graphviz_chart(right_graph)

action = col1.menu_button("left graph", options=["graph_one", "graph_two", "graph_three"])
if action == "graph_one":
    col1.graphviz_chart(G)
elif action == "graph_two":
    col1.graphviz_chart(H)
elif action == "graph_three":
    col1.graphviz_chart(I)

action_two = col2.menu_button("right graph", options=["graph_one", "graph_two", "graph_three"])
if action_two == "graph_one":
    col2.graphviz_chart(G)
elif action_two == "graph_two":
    col2.graphviz_chart(H)
elif action_two == "graph_three":
    col2.graphviz_chart(I)