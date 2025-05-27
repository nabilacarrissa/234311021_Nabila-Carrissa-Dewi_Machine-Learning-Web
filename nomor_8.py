import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Atur halaman
st.set_page_config(page_title="Dashboard Pinjaman", layout="wide")

# Sidebar
st.sidebar.title("Select Page")
page = st.sidebar.selectbox("Pilih Halaman", ["Home"])

# Halaman Home
if page == "Home":
    st.image("https://cdn-icons-png.flaticon.com/512/201/201623.png", width=300)

    # Dataset dummy (bisa diganti dengan file CSV asli)
    data = {
        "Loan_ID": ["LP001", "LP002", "LP003", "LP004", "LP005"],
        "Gender": ["Male", "Male", "Male", "Female", "Male"],
        "Married": ["No", "Yes", "Yes", "No", "Yes"],
        "Education": [
            "Graduate",
            "Graduate",
            "Not Graduate",
            "Graduate",
            "Not Graduate",
        ],
        "Self_Employed": ["No", "Yes", "No", "No", "Yes"],
        "ApplicantIncome": [5000, 3000, 4000, 2500, 6000],
        "LoanAmount": [200, 120, 150, 100, 250],
    }

    df = pd.DataFrame(data)

    # Tampilkan data
    st.subheader("Dataset:")
    st.dataframe(df)

# Visualisasi
st.subheader("Applicant Income VS Loan Amount")

fig, ax = plt.subplots(figsize=(6, 4))  # ukuran lebih kecil
ax.bar(
    df["Loan_ID"],
    df["ApplicantIncome"],
    label="Applicant Income",
    width=0.4,
    align="center",
)
ax.bar(
    df["Loan_ID"],
    [x * 100 for x in df["LoanAmount"]],
    label="Loan Amount x100",
    alpha=0.7,
    width=0.4,
)
ax.set_xlabel("Loan ID")
ax.set_ylabel("Amount")
ax.set_title("Applicant Income vs Loan Amount")
ax.legend()
st.pyplot(fig)
