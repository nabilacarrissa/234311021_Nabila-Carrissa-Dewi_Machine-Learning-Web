import pickle
import streamlit as st
import pandas as pd
import os
import numpy as np
import altair as alt

# --- Konfigurasi Halaman ---
st.set_page_config(page_title="Prediksi Harga Mobil", layout="centered")

# --- Judul Aplikasi ---
st.title("🚗 Prediksi Harga Mobil")

# --- Load model dari file .sav ---
MODEL_PATH = "CSV/model_prediksi_harga_mobil.sav"
if not os.path.exists(MODEL_PATH):
    st.error("❌ Model file tidak ditemukan. Pastikan file .sav tersedia.")
    st.stop()
model = pickle.load(open(MODEL_PATH, "rb"))

# --- Header Dataset ---
DATA_PATH = "CSV/CarPrice_Assignment.csv"
if not os.path.exists(DATA_PATH):
    st.error("❌ Dataset 'CarPrice.csv' tidak ditemukan.")
    st.stop()

df1 = pd.read_csv(DATA_PATH)

# Tampilkan data mentah
st.subheader("Data Mobil")
st.dataframe(df1[["CarName", "price"]].head())  # tampilkan nama mobil & harga

# --- Visualisasi Data ---
st.subheader("📊 Grafik Visualisasi Data")

# Cek kolom yang dibutuhkan tersedia
required_cols = {"car_ID", "highwaympg", "curbweight", "horsepower"}
if not required_cols.issubset(df1.columns):
    st.error("Dataset tidak memiliki kolom yang dibutuhkan untuk visualisasi.")
else:
    # Grafik Highway MPG
    st.write("**Grafik Highway MPG**")
    chart_highwaympg = alt.Chart(df1).mark_line().encode(x="car_ID", y="highwaympg")
    st.altair_chart(chart_highwaympg, use_container_width=True)

    # Grafik Curb Weight
    st.write("**Grafik Curb Weight**")
    chart_curbweight = alt.Chart(df1).mark_line().encode(x="car_ID", y="curbweight")
    st.altair_chart(chart_curbweight, use_container_width=True)

    # Grafik Horsepower
    st.write("**Grafik Horsepower**")
    chart_horsepower = alt.Chart(df1).mark_line().encode(x="car_ID", y="horsepower")
    st.altair_chart(chart_horsepower, use_container_width=True)

# --- Input User untuk Prediksi ---
st.subheader("🔍 Masukkan Spesifikasi Mobil")

highwaympg = st.slider("⛽ Highway MPG", 10, 60, 30)
curbweight = st.slider("⚖️ Curb Weight", 1500, 4000, 2500)
enginesize = st.slider("🛠️ Engine Size", 50, 350, 130)
horsepower = st.slider("🔧 Horsepower", 40, 300, 100)

# --- Prediksi Harga Mobil ---
if st.button("💰 Prediksi Harga"):
    input_data = np.array([[horsepower, curbweight, enginesize, highwaympg]])
    car_prediction = model.predict(input_data)

    harga_mobil_float = float(car_prediction[0])
    harga_mobil_formatted = f"USD {harga_mobil_float:,.2f}"

    st.success(f"💸 Perkiraan Harga Mobil: **{harga_mobil_formatted}**")
    st.balloons()
