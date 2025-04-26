import streamlit as st
import pandas as pd
import numpy as np

st.title("Random Line Chart")



data = pd.DataFrame(np.random.randn(50, 3), columns=['A', 'B', 'C'])

st.line_chart(data)
