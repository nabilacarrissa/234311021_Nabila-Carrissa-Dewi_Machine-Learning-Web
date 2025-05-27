import pickle as joblib
import streamlit as st
import pandas as pd
import os
import numpy as np
import altair as alt

# --- Konfigurasi Halaman ---
st.set_page_config(page_title="Prediksi Harga Mobil", layout="wide")

# --- Sidebar Navigasi ---
with st.sidebar:
    st.title("🚗 Prediksi Harga Mobil")
    st.markdown("Gunakan menu di bawah untuk navigasi:")
    page = st.radio(
        "Pilih Halaman:", ["📊 Dataset & Visualisasi", "💰 Prediksi Harga Mobil"]
    )
    st.markdown("---")
    st.info("👤 Dibuat oleh: Nabilacarrissa")
    st.caption("📅 Tahun: 2025")

# --- Load Model ---
MODEL_PATH = "CSV/model_prediksi_harga_mobil.sav"
if not os.path.exists(MODEL_PATH):
    st.error("❌ File model .sav tidak ditemukan.")
    st.stop()
model = joblib.load(MODEL_PATH)

# --- Load Dataset ---
DATA_PATH = "CSV/CarPrice_Assignment.csv"
if not os.path.exists(DATA_PATH):
    st.error("❌ File dataset tidak ditemukan.")
    st.stop()
df = pd.read_csv(DATA_PATH)

# --- Persiapan Data ---
df.columns = df.columns.str.strip()
df["brand"] = df["CarName"].apply(lambda x: x.split()[0].lower())

# --- Halaman Dataset & Visualisasi ---
if page == "📊 Dataset & Visualisasi":
    st.title("📊 Analisis Data Harga Mobil")
    st.subheader("🔍 Data Mobil")

    brand_filter = st.selectbox(
        "Filter Berdasarkan Merek Mobil", sorted(df["brand"].unique())
    )
    filtered_df = df[df["brand"] == brand_filter]

    st.dataframe(
        filtered_df[
            ["CarName", "price", "horsepower", "curbweight", "highwaympg"]
        ].head(),
        use_container_width=True,
    )

    st.subheader("📈 Grafik Harga Mobil per Model")
    chart_price = (
        alt.Chart(filtered_df)
        .mark_bar()
        .encode(
            x=alt.X("CarName", sort="-y", title="Nama Mobil"),
            y=alt.Y("price", title="Harga"),
            tooltip=["CarName", "price"],
        )
        .properties(width=800, height=400)
        .interactive()
    )
    st.altair_chart(chart_price, use_container_width=True)

    st.subheader("📉 Korelasi Fitur dengan Harga")
    num_features = ["horsepower", "curbweight", "enginesize", "highwaympg"]
    selected_feature = st.selectbox("Pilih Fitur:", num_features)

    scatter_plot = (
        alt.Chart(df)
        .mark_circle(size=70)
        .encode(
            x=selected_feature,
            y="price",
            color="brand",
            tooltip=["CarName", "price", selected_feature],
        )
        .interactive()
        .properties(width=800, height=400)
    )
    st.altair_chart(scatter_plot, use_container_width=True)

# --- Halaman Prediksi ---
elif page == "💰 Prediksi Harga Mobil":
    st.title("💰 Prediksi Harga Mobil Baru")
    st.markdown("Masukkan spesifikasi mobil:")

    highwaympg = st.slider("⛽ Highway MPG", 10, 60, 30)
    curbweight = st.slider("⚖️ Curb Weight", 1500, 4000, 2500)
    enginesize = st.slider("🛠️ Engine Size", 50, 350, 130)
    horsepower = st.slider("🔧 Horsepower", 40, 300, 100)

    input_data = np.array([[horsepower, curbweight, enginesize, highwaympg]])

    if st.button("🔮 Prediksi Sekarang"):
        harga_prediksi = model.predict(input_data)[0]
        harga_formatted = f"USD {harga_prediksi:,.2f}"
        st.success(f"🎉 Perkiraan Harga Mobil: **{harga_formatted}**")
        st.balloons()

        st.subheader("📊 Visualisasi Input & Prediksi")
        viz_df = pd.DataFrame(
            {
                "Fitur": [
                    "Horsepower",
                    "Curb Weight",
                    "Engine Size",
                    "Highway MPG",
                    "Predicted Price",
                ],
                "Nilai": [
                    horsepower,
                    curbweight,
                    enginesize,
                    highwaympg,
                    harga_prediksi,
                ],
            }
        )

        bar_chart = (
            alt.Chart(viz_df)
            .mark_bar(size=50)
            .encode(
                x=alt.X("Fitur", sort=None),
                y="Nilai",
                color=alt.condition(
                    alt.datum.Fitur == "Predicted Price",
                    alt.value("orange"),
                    alt.value("steelblue"),
                ),
                tooltip=["Fitur", "Nilai"],
            )
            .properties(height=400)
        )
        st.altair_chart(bar_chart, use_container_width=True)

        pred_df = pd.DataFrame(
            [
                {
                    "Horsepower": horsepower,
                    "CurbWeight": curbweight,
                    "EngineSize": enginesize,
                    "HighwayMPG": highwaympg,
                    "Predicted_Price": harga_prediksi,
                }
            ]
        )
        csv = pred_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Unduh Hasil Prediksi",
            data=csv,
            file_name="hasil_prediksi_harga_mobil.csv",
            mime="text/csv",
        )
