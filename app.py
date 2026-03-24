import streamlit as st
import pandas as pd

# Page setup
st.set_page_config(page_title="Soil Nutrient Calculator", layout="wide")

# Title
st.title("🌱 Soil Nutrient Calculator")

# 👉 ADD GUIDE HERE (correct place)
with st.expander("📘 Parameter Guide (Click to expand)"):
    st.markdown("""
### 🌱 Soil Nutrient Parameters

**Nitrogen (Kjeldahl)**
- N_W → Soil weight (g)
- VS → Volume of acid used for sample (mL)
- VB → Volume of acid used for blank (mL)
- X → Normality of acid

**Phosphorus (Olsen/Bray)**
- P_W → Soil weight (g)
- P_VE → Volume of extractant (mL)
- P_VA → Aliquot taken (mL)
- P_VC → Final coloured volume (mL)
- P_R → Concentration (mg/L)

**Potassium**
- K_W → Soil weight (g)
- K_VE → Volume of extractant (mL)
- K_VA → Aliquot (mL)
- K_VF → Final volume (mL)
- K_FR → Flame photometer reading (mg/L)

**Micronutrients (DTPA)**
- M_W → Soil weight (g)
- M_VE → Volume of extractant (mL)
- M_VA → Aliquot (mL)
- M_VF → Final volume (mL)
- M_S → Sample concentration (mg/L)
- M_B → Blank concentration (mg/L)
""")

st.write("Upload your Excel file to calculate soil nutrients automatically.")

uploaded_file = st.file_uploader("📂 Upload Excel file", type=["xlsx"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)

    st.subheader("📊 Input Data")
    st.dataframe(df)

    # --- FUNCTIONS ---
    def n_boric(W, VS, VB, X):
        return ((VS - VB) * X * 14 * 100) / (W * 1000)

    def available_p(W, VE, VA, VC, R):
        return (R * VC * VE) / (VA * W)

    def available_k(W, VE, VA, VF, FR):
        return (FR * VF * VE) / (VA * W)

    def dtpa_micro(W, VE, VA, VF, S, B):
        return ((S - B) * VF * VE) / (VA * W)

    # --- CALCULATIONS ---
    df["N (%)"] = df.apply(lambda x: n_boric(x["N_W"], x["VS"], x["VB"], x["X"]), axis=1)
    df["N (mg/kg)"] = df["N (%)"] * 10000
    df["N (kg/ha)"] = df["N (mg/kg)"] * 2

    df["P (mg/kg)"] = df.apply(lambda x: available_p(x["P_W"], x["P_VE"], x["P_VA"], x["P_VC"], x["P_R"]), axis=1)
    df["P (kg/ha)"] = df["P (mg/kg)"] * 2

    df["K (mg/kg)"] = df.apply(lambda x: available_k(x["K_W"], x["K_VE"], x["K_VA"], x["K_VF"], x["K_FR"]), axis=1)
    df["K (kg/ha)"] = df["K (mg/kg)"] * 2

    df["Micro (mg/kg)"] = df.apply(lambda x: dtpa_micro(x["M_W"], x["M_VE"], x["M_VA"], x["M_VF"], x["M_S"], x["M_B"]), axis=1)
    df["Micro (kg/ha)"] = df["Micro (mg/kg)"] * 2

    st.subheader("✅ Output Data")
    st.dataframe(df)

    st.download_button(
        label="⬇ Download Results",
        data=df.to_csv(index=False),
        file_name="soil_results.csv",
        mime="text/csv"
    )