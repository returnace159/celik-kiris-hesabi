import streamlit as st

st.set_page_config(page_title="Korkmaz Profil Hesap", layout="centered")

st.title("🏗️ Korkmaz Çelik Hesap Makinesi")
st.write("Sadece Standart IPE ve HEA profilleriyle hızlı hesap.")

# --- PROFİL VERİTABANLARI ---
# [Ağırlık_kg/m, Ix_cm4]
hea_db = {
    "HEA 100": [16.7, 349.2], "HEA 120": [19.9, 606.2], "HEA 140": [24.7, 1033.0],
    "HEA 160": [30.4, 1673.0], "HEA 180": [35.5, 2510.0], "HEA 200": [42.3, 3692.0],
    "HEA 220": [50.5, 5410.0], "HEA 240": [60.3, 7763.0], "HEA 260": [68.2, 10450.0],
    "HEA 280": [76.4, 13670.0], "HEA 300": [88.3, 18260.0], "HEA 400": [125.0, 45070.0],
    "HEA 500": [155.0, 86970.0], "HEA 600": [178.0, 141200.0]
}

# Sadece Standart IPE Serisi (PDF'den güncellendi )
ipe_db = {
    "IPE 100": [8.1, 171.0], "IPE 120": [10.4, 317.8], "IPE 140": [12.9, 541.2],
    "IPE 160": [15.8, 869.3], "IPE 180": [18.8, 1317.0], "IPE 200": [22.4, 1943.0],
    "IPE 220": [26.2, 2772.0], "IPE 240": [30.7, 3892.0], "IPE 270": [36.1, 5790.0],
    "IPE 300": [42.2, 8356.0], "IPE 330": [49.1, 11770.0], "IPE 360": [57.1, 16270.0],
    "IPE 400": [66.3, 23130.0], "IPE 450": [77.6, 33740.0], "IPE 500": [90.7, 48200.0],
    "IPE 550": [106.0, 67120.0], "IPE 600": [122.0, 92080.0]
}

# --- GİRDİLER ---
col1, col2 = st.columns(2)
with col1:
    L = st.number_input("Kiriş Boyu (metre):", value=12.0)
    P_kg = st.number_input("Yük (kg):", value=5000)

with col2:
    tip = st.radio("Profil Tipi:", ["HEA", "IPE"])
    db = hea_db if tip == "HEA" else ipe_db
    liste = list(db.keys())
    profil = st.selectbox("Profil Seçin:", liste, index=len(liste)//2)

# --- MATEMATİKSEL HESAP ---
Ix_cm4 = db[profil][1]
Ix_mm4 = Ix_cm4 * 10000 # cm4 -> mm4 çevrimi
L_mm = L * 1000
P_N = P_kg * 9.81
E = 210000 # Çelik için standart değer

sehim = (P_N * (L_mm**3)) / (48 * E * Ix_mm4)
limit = L_mm / 300

# --- SONUÇ ---
st.divider()
st.subheader(f"📊 Analiz: {profil}")

c1, c2 = st.columns(2)
c1.metric("Hesaplanan Sehim", f"{sehim:.2f} mm")
c2.metric("Müsaade Edilen (L/300)", f"{limit:.2f} mm")

if sehim > limit:
    st.error("❌ Sehim limiti aşıldı! Profil yetersiz.")
else:
    st.success("✅ Profil bu yük için uygundur.")
