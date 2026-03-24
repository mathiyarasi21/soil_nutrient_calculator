import pandas as pd

# ==============================
# FUNCTIONS
# ==============================

# Nitrogen
def n_Kjeldahl(W, VS, VB, X):
    return ((VS - VB) * X * 14 * 100) / (W * 1000)

# Phosphorus
def available_p(W, VE, VA, VC, R):
    return (R * VC * VE) / (VA * W)

# Potassium
def available_k(W, VE, VA, VF, FR):
    return (FR * VF * VE) / (VA * W)

# Micronutrients
def dtpa_micro(W, VE, VA, VF, S, B):
    return ((S - B) * VF * VE) / (VA * W)

# ==============================
# LOAD DATA
# ==============================

df = pd.read_excel("input.xlsx")

# ==============================
# CALCULATIONS
# ==============================

# Nitrogen
df["N (%)"] = df.apply(
    lambda x: n_Kjeldahl(x["N_W"], x["VS"], x["VB"], x["X"]),
    axis=1
)
# Convert N % → mg/kg
df["N (mg/kg)"] = df["N (%)"] * 10000

# Convert mg/kg → kg/ha
df["N (kg/ha)"] = df["N (mg/kg)"] * 2
# Phosphorus
df["P (mg/kg)"] = df.apply(
    lambda x: available_p(x["P_W"], x["P_VE"], x["P_VA"], x["P_VC"], x["P_R"]),
    axis=1
)
# Potassium
df["K (mg/kg)"] = df.apply(
    lambda x: available_k(x["K_W"], x["K_VE"], x["K_VA"], x["K_VF"], x["K_FR"]),
    axis=1
)

# Micronutrients
df["Micro (mg/kg)"] = df.apply(
    lambda x: dtpa_micro(x["M_W"], x["M_VE"], x["M_VA"], x["M_VF"], x["M_S"], x["M_B"]),
    axis=1
)

# ==============================
# CONVERSION (kg/ha)
# ==============================

df["P (kg/ha)"] = df["P (mg/kg)"] * 2
df["K (kg/ha)"] = df["K (mg/kg)"] * 2
df["Micro (kg/ha)"] = df["Micro (mg/kg)"] * 2

# ==============================
# SAVE OUTPUT
# ==============================

df.to_excel("output.xlsx", index=False)

print("✅ All nutrient calculations completed! Check output.xlsx")