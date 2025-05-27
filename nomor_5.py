import streamlit as st
import datetime

# Input number
st.number_input("Pick a number", min_value=0)

# Email
st.text_input("Email address")

# Tanggal
st.date_input("Travelling date", value=datetime.date(2022, 6, 17))

# Jam
st.time_input("School time", value=datetime.time(8, 0))

# Text area (multi-line)
st.text_area("Description")

# Upload file
st.file_uploader("Upload a photo", type=["jpg", "png", "jpeg"])

# Pilih warna
st.color_picker("Choose your favourite color", "#ff00ff")

# Tutup border
st.markdown("</div>", unsafe_allow_html=True)
