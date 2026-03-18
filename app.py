import streamlit as st

st.set_page_config(page_title="Korkmaz Mühendislik", layout="centered")

st.title("🏗️ Korkmaz Çelik Hesap Makinesi")
st.write("Profil seçin, yükü girin ve limitinizi (1/500, 1/1000 vb.) belirleyin.")

# --- VERİTABANLARI ---
hea_db = {
    "HEA 100": 349.2, "HEA 120": 606.2, "HEA 140": 1033.0, "HEA 160": 1673.0,
    "HEA 180": 2510.0, "HEA 200": 3692.0, "HEA 240": 7763.0, "HEA 300": 18260.0,
    "HEA 400": 45070.0, "HEA 500": 86970.0, "HEA 600": 141200.0
}

# PDF'den sadece standart IPE serisi
ipe_db = {
    "IPE 100": 171.0, "IPE 140": 541.2, "IPE 180": 1317.0, "IPE 200": 1943.0,
    "IPE 240": 3892.0, "IPE 270": 5790.0, "IPE 300": 8356.0, "IPE 400": 23130.0,
    "IPE 500": 48200.0, "IPE 600": 92080.0
}

# --- GİRDİLER ---
col1, col2 = st.columns(2)

with col1:
    L = st.number_input("Kiriş Boyu (metre):", value=12.0)
    P_kg = st.number_input("Yük (kg):", value=5000)
    # Senin istediğin o kritik oran seçimi!
    oran_limit = st.selectbox("Sehim Limiti (L/X):", [300, 500, 900, 1000], index=1)

with col2:
    tip = st.radio("Profil Tipi:", ["HEA", "IPE"])
    db = hea_db if tip == "HEA" else ipe_db
    profil = st.selectbox("Profil Seçin:", list(db.keys()), index=len(db)//2)

# --- HESAPLAMA ---
Ix = db[profil] * 10000
L_mm = L * 1000
P_N = P_kg * 9.81
E = 210000

sehim = (P_N * (L_mm**3)) / (48 * E * Ix)
limit_degeri = L_mm / oran_limit
oran_gercek = L_mm / sehim if sehim > 0 else 0

# --- SONUÇ EKRANI ---
st.divider()
st.subheader(f"📊 {profil} Analiz Sonucu")

c1, c2, c3 = st.columns(3)
c1.metric("Hesaplanan", f"{sehim:.2f} mm")
c2.metric("Limit", f"{limit_degeri:.2f} mm")
c3.metric("Mevcut Oran", f"L/{int(oran_gercek)}")

if sehim > limit_degeri:
    st.error(f"❌ Yetersiz! Mevcut sehim L/{int(oran_gercek)}, hedef L/{oran_limit}")
else:
    st.success(f"✅ Uygun! Kiriş L/{oran_limit} şartını sağlıyor.")

st.info(f"Seçilen Limit: Kiriş boyunun {oran_limit}'de birinden fazla esnememesi gerekir.")
