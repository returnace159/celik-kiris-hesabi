import streamlit as st

st.set_page_config(page_title="Korkmaz Mühendislik v5", layout="centered")

st.title("🏗️ Korkmaz Akıllı Analiz Sistemi")
st.write("Profilinizi seçin veya bırakın sistem size en iyisini önersin.")

# --- VERİTABANLARI ---
hea_db = {
    "HEA 100": 349.2, "HEA 120": 606.2, "HEA 140": 1033.0, "HEA 160": 1673.0,
    "HEA 180": 2510.0, "HEA 200": 3692.0, "HEA 220": 5410.0, "HEA 240": 7763.0,
    "HEA 260": 10450.0, "HEA 280": 13670.0, "HEA 300": 18260.0, "HEA 400": 45070.0,
    "HEA 500": 86970.0, "HEA 600": 141200.0
}

ipe_db = {
    "IPE 100": 171.0, "IPE 120": 317.8, "IPE 140": 541.2, "IPE 160": 869.3,
    "IPE 180": 1317.0, "IPE 200": 1943.0, "IPE 220": 2772.0, "IPE 240": 3892.0,
    "IPE 270": 5790.0, "IPE 300": 8356.0, "IPE 330": 11770.0, "IPE 360": 16270.0,
    "IPE 400": 23130.0, "IPE 450": 33740.0, "IPE 500": 48200.0, "IPE 600": 92080.0
}

# --- GİRDİLER ---
col1, col2 = st.columns(2)

with col1:
    L = st.number_input("Kiriş Boyu (metre):", value=6.0)
    P_kg = st.number_input("Yük (kg):", value=2000)
    oran_limit = st.selectbox("Sehim Limiti (L/X):", [300, 500, 900, 1000], index=1)

with col2:
    tip = st.radio("Profil Tipi:", ["HEA", "IPE"])
    db = hea_db if tip == "HEA" else ipe_db
    profil_listesi = list(db.keys())
    secilen_profil = st.selectbox("Kendi Seçimin (Manuel):", profil_listesi, index=5)

# --- HESAPLAMA ---
if st.button("ANALİZ ET VE ÖNER 🔍"):
    L_mm = L * 1000
    P_N = P_kg * 9.81
    E = 210000
    hedef_limit = L_mm / oran_limit
    
    # 1. Manuel Seçilen Profilin Hesabı
    ix_manuel = db[secilen_profil] * 10000
    sehim_manuel = (P_N * (L_mm**3)) / (48 * E * ix_manuel)
    oran_manuel = L_mm / sehim_manuel
    
    # 2. Akıllı Öneri Bulma (En küçük uygun profil)
    oneri_profil = None
    for ad, ix_cm4 in db.items():
        if ( (P_N * (L_mm**3)) / (48 * E * (ix_cm4 * 10000)) ) <= hedef_limit:
            oneri_profil = ad
            break
    
    st.divider()

    # --- KÜÇÜK ÖNERİ EKRANI ---
    if oneri_profil:
        st.info(f"💡 **AKILLI ÖNERİ:** Bu yük için en ideal ekonomik profil: **{oneri_profil}**")
    else:
        st.warning("⚠️ **DİKKAT:** Listedeki hiçbir profil bu limiti kurtarmıyor!")

    # --- MANUEL SEÇİM SONUCU ---
    st.subheader(f"📊 Senin Seçtiğin: {secilen_profil}")
    c1, c2, c3 = st.columns(3)
    c1.metric("Sehim", f"{sehim_manuel:.2f} mm")
    c2.metric("Limit", f"{hedef_limit:.2f} mm")
    c3.metric("Oran", f"L/{int(oran_manuel)}")

    if sehim_manuel <= hedef_limit:
        st.success(f"✅ {secilen_profil} şartları sağlıyor.")
    else:
        st.error(f"❌ {secilen_profil} YETERSİZ!")
