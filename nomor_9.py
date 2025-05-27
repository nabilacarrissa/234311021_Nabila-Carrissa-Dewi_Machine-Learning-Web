import streamlit as st
import pickle
import numpy as np
from PIL import Image

# --- Konfigurasi halaman ---
st.set_page_config(page_title="Prediksi Harga Mobil", layout="centered")

# --- Load model ---
try:
    model = pickle.load(open("CSV/model_prediksi_harga_mobil.sav", "rb"))
except FileNotFoundError:
    st.error("❌ File model tidak ditemukan. Pastikan path-nya benar.")
    st.stop()

# --- Header Aplikasi ---
st.markdown(
    "<h1 style='text-align: center; color: #4A90E2;'>🚗 Prediksi Harga Mobil</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "Masukkan spesifikasi mobil Anda di bawah ini, lalu tekan tombol **Prediksi** untuk melihat estimasi harga jual."
)

st.divider()

# --- Form Input Pengguna ---
with st.form("form_prediksi"):
    col1, col2 = st.columns(2)

    with col1:
        horsepower = st.slider("🔧 Horsepower", 40, 300, 100)
        enginesize = st.slider("🛠️ Engine Size", 50, 350, 130)

    with col2:
        curbweight = st.slider("⚖️ Curb Weight (lbs)", 1500, 4000, 2500)
        highwaympg = st.slider("⛽ Highway MPG", 10, 60, 30)

    prediksi_button = st.form_submit_button("🔍 Prediksi Harga")

# --- Hasil Prediksi ---
if prediksi_button:
    input_data = np.array([[horsepower, curbweight, enginesize, highwaympg]])
    harga = model.predict(input_data)
    st.success(f"💰 Perkiraan Harga Mobil: **USD {harga[0]:,.2f}**")
    st.balloons()
