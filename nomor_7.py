import streamlit as st
import pandas as pd
import numpy as np

# Membuat DataFrame dengan data acak
df3 = pd.DataFrame(np.random.randn(10, 2), columns=["x", "y"])

# Menampilkan line chart
st.subheader("Line Chart")
st.line_chart(df3)

# Menampilkan bar chart
st.subheader("Bar Chart")
st.bar_chart(df3)

# Menampilkan area chart
st.subheader("Area Chart")
st.area_chart(df3)
