import pickle
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
    st.markdown("Gunakan menu di bawah untuk menavigasi:")
    page = st.radio("📂 Menu", ["📊 Dataset & Visualisasi", "💰 Prediksi Harga Mobil"])
    st.markdown("---")
    st.info("👤 Dibuat oleh: Nabilacarrissa")
    st.write("📅 Tahun: 2025")

# --- Load Model ---
MODEL_PATH = "CSV/model_prediksi_harga_mobil.sav"
if not os.path.exists(MODEL_PATH):
    st.error("❌ File model .sav tidak ditemukan.")
    st.stop()
model = pickle.load(open(MODEL_PATH, "rb"))

# --- Load Dataset ---
DATA_PATH = "CSV/CarPrice_Assignment.csv"
if not os.path.exists(DATA_PATH):
    st.error("❌ File dataset tidak ditemukan.")
    st.stop()
df = pd.read_csv(DATA_PATH)

# --- Persiapan Dataset ---
df.columns = df.columns.str.strip()
df["brand"] = df["CarName"].apply(lambda x: x.split()[0].lower())

# --- Halaman Dataset & Visualisasi ---
if page == "📊 Dataset & Visualisasi":
    st.title("📊 Analisis Data Harga Mobil")
    st.subheader("🔍 Tabel Data Mobil")

    brand_filter = st.selectbox(
        "🔎 Filter Berdasarkan Merek Mobil", sorted(df["brand"].unique())
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
            y=alt.Y("price", title="Harga (USD)"),
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
        .mark_circle(size=60)
        .encode(
            x=selected_feature,
            y="price",
            color="brand",
            tooltip=["CarName", "price", selected_feature],
        )
        .interactive()
        .properties(width=800)
    )
    st.altair_chart(scatter_plot, use_container_width=True)

# --- Halaman Prediksi ---
elif page == "💰 Prediksi Harga Mobil":
    st.title("💰 Prediksi Harga Mobil Baru")
    st.markdown("Masukkan spesifikasi mobil yang ingin diprediksi:")

    col1, col2 = st.columns(2)

    with col1:
        horsepower = st.slider("🔧 Horsepower", 40, 300, 100)
        enginesize = st.slider("🛠️ Engine Size", 50, 350, 130)

    with col2:
        curbweight = st.slider("⚖️ Curb Weight", 1500, 4000, 2500)
        highwaympg = st.slider("⛽ Highway MPG", 10, 60, 30)

    input_data = np.array([[horsepower, curbweight, enginesize, highwaympg]])

    st.markdown("---")
    if st.button("🔮 Prediksi Sekarang", use_container_width=True):
        harga_prediksi = model.predict(input_data)[0]
        harga_formatted = f"USD {harga_prediksi:,.2f}"
        st.balloons()

        col_left, col_right = st.columns([2, 1])

        with col_left:
            st.subheader("📊 Visualisasi Spesifikasi")
            viz_df = pd.DataFrame(
                {
                    "Fitur": [
                        "Horsepower",
                        "Curb Weight",
                        "Engine Size",
                        "Highway MPG",
                    ],
                    "Nilai": [horsepower, curbweight, enginesize, highwaympg],
                }
            )

            bar_chart = (
                alt.Chart(viz_df)
                .mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6)
                .encode(
                    x=alt.X("Fitur", sort=None, title=None),
                    y=alt.Y("Nilai", title="Nilai Spesifikasi"),
                    color=alt.Color("Nilai", scale=alt.Scale(scheme="tealblues")),
                    tooltip=["Fitur", "Nilai"],
                )
                .properties(height=300)
            )

            label = (
                alt.Chart(viz_df)
                .mark_text(dy=-10)
                .encode(x="Fitur", y="Nilai", text=alt.Text("Nilai", format=".0f"))
            )

            st.altair_chart(bar_chart + label, use_container_width=True)

        with col_right:
            st.subheader("💰 Prediksi Harga")
            st.markdown(
                f"""
                <div style='padding:20px; background:#f9f9f9; border-radius:10px; text-align:center; box-shadow:2px 2px 8px rgba(0,0,0,0.1);'>
                    <h2 style='color:darkgreen;'>Estimasi</h2>
                    <h1 style='color:orange; font-size:40px;'>💵 {harga_formatted}</h1>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("### ⬇️ Unduh Hasil Prediksi")
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
            label="📥 Unduh CSV",
            data=csv,
            file_name="hasil_prediksi_harga_mobil.csv",
            mime="text/csv",
        )
