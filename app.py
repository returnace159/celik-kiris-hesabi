import streamlit as st

st.set_page_config(page_title="Çelik Analiz Pro v8", page_icon="🏗️", layout="wide")
st.title("🏗️ Çelik Kiriş Analiz Asistanı (Buton Kontrollü)")
st.caption("Merkezi Yük + Zati Ağırlık + Gerilme + L/500, L/900, L/1000 Sehim")

# --- VERİTABANI (Senin Tablandan Veriler) ---
hea_data = {
    "HEA 100": [72.8, 16.7, 349.2],    "HEA 120": [106.3, 19.9, 606.2],
    "HEA 140": [155.4, 24.7, 1033],    "HEA 160": [220.1, 30.4, 1673],
    "HEA 180": [293.6, 35.5, 2510],    "HEA 200": [388.6, 42.3, 3692],
    "HEA 220": [515.2, 50.5, 5410],    "HEA 240": [675.1, 60.3, 7763],
    "HEA 260": [836.4, 68.2, 10450],   "HEA 280": [1013, 76.4, 13670],
    "HEA 300": [1260, 88.3, 18260],    "HEA 320": [1479, 97.6, 22930],
    "HEA 340": [1678, 105.0, 27690],   "HEA 360": [1888, 112.0, 33090],
    "HEA 400": [2311, 125.0, 45070],   "HEA 450": [2896, 140.0, 63720],
    "HEA 500": [3550, 155.0, 86970],   "HEA 550": [4146, 166.0, 111900],
    "HEA 600": [4702, 178.0, 141200],  "HEA 700": [5764, 204.0, 215300],
    "HEA 800": [6891, 224.0, 303400],  "HEA 900": [8013, 252.0, 422100],
    "HEA 1000": [9485, 272.0, 553800]
}

# --- YAN PANEL ---
with st.sidebar:
    st.header("⚙️ Girdiler")
    secilen = st.selectbox("Profil Seçin:", list(hea_data.keys()), index=10)
    L = st.number_input("Açıklık (Metre):", min_value=0.1, value=6.0, step=0.5)
    P_kg = st.number_input("Merkezi Yük (kg):", min_value=0, value=3000, step=100)
    sehim_secimi = st.selectbox("Sehim Sınırı:", ["L/500", "L/900", "L/1000"], index=0)
    
    st.write("---")
    # --- İŞTE O BUTON ---
    hesapla = st.button("🚀 HESAPLA", use_container_width=True, type="primary")
    st.write("---")
    st.info("Çelik: S235 (St 37)\nE = 210.000 MPa")

# --- HESAPLAMA FONKSİYONU ---
def analiz(p_adi, L_m, p_kg):
    wx_mm3 = hea_data[p_adi][0] * 1000
    g_kg_m = hea_data[p_adi][1]
    ix_mm4 = hea_data[p_adi][2] * 10000 
    L_mm = L_m * 1000
    P_N = p_kg * 9.81
    q_N_mm = (g_kg_m * 9.81) / 1000
    E = 210000
    
    M_t = (P_N * L_mm) / 4
    M_z = (q_N_mm * (L_mm**2)) / 8
    gerilme = (M_t + M_z) / wx_mm3
    
    s_p = (P_N * (L_mm**3)) / (48 * E * ix_mm4)
    s_g = (5 * q_N_mm * (L_mm**4)) / (384 * E * ix_mm4)
    return gerilme, (s_p + s_g)

# --- ANA EKRAN KONTROLÜ ---
if hesapla:
    g, s = analiz(secilen, L, P_kg)
    denomin = int(sehim_secimi.split("/")[1])
    limit_mm = (L * 1000) / denomin

    c1, c2 = st.columns(2)
    with c1:
        st.metric("Gerilme Analizi", f"{g:.2f} MPa")
        if g < 235: st.success("✅ Gerilme Uygun")
        else: st.error("❌ Akma Sınırı AŞILDI!")

    with c2:
        st.metric(f"Sehim Analizi ({sehim_secimi})", f"{s:.1f} mm")
        if s < limit_mm: st.success(f"✅ Sehim Uygun (<{limit_mm:.1f} mm)")
        else: st.error(f"❌ Esneme Fazla! (>{limit_mm:.1f} mm)")

    st.divider()
    if g >= 235 or s >= limit_mm:
        st.warning(f"⚠️ **{secilen}** yetersiz. Uygun profil aranıyor...")
        for ad in hea_data.keys():
            g_k, s_k = analiz(ad, L, P_kg)
            if g_k < 235 and s_k < limit_mm:
                st.info(f"💡 **ÇÖZÜM:** Minimum **{ad}** kullanmalısınız.")
                break
    else:
        st.balloons()
        st.success(f"Mükemmel! **{secilen}** tüm kriterleri sağlıyor.")
else:
    st.info("👈 Lütfen sol taraftaki değerleri kontrol edin ve 'HESAPLA' butonuna basın.")
    st.image("https://img.icons8.com/clouds/200/engineering.png", width=200) # Tatlı bir ikon
