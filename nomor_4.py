import streamlit as st


# Checkbox
st.checkbox("yes")

# Button
st.button("Click")

# Radio Button
st.radio("Pick your gender", ["Male", "Female"])

# Selectbox (Dropdown)
st.selectbox("Pick your gender", ["Male", "Female"])

# Selectbox lain
st.selectbox(
    "choose a planet", ["Choose an option", "Mercury", "Venus", "Earth", "Mars"]
)

# Slider (Pick a mark)
st.slider(
    "Pick a mark",
    min_value=0,
    max_value=100,
    value=60,
    format="%d",
    help="Bad               Good               Excellent",
)

# Slider (Pick a number)
st.slider("Pick a number", 0, 50, 9)
