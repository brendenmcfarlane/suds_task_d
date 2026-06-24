# python3 -m streamlit run frameworks/script.py
import streamlit as st
import pandas as pd

st.write("Here's our first attempt at using data to create a table:")
st.write(pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
}))
y = st.slider('y')  
st.write(y, 'squared is', y * y)