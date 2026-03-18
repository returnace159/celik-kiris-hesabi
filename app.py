import streamlit as st

st.set_page_config(page_title="Çelik Hesap Pro v3", page_icon="🏗️")
st.title("🏗️ Profesyonel Kiriş Analiz Asistanı")
st.caption("Hesaplama: Merkezi Tekil Yük + Kiriş Zati Ağırlığı (St 37)")

# --- VERİTABANI (Tablandan okunan Wx ve G ağırlık değerleri) ---
# Format: "Profil Adı": [Wx (cm3), G (kg/m)]
hea_data = {
    "HEA 100": [72.8, 16.7],   "HEA 120": [106.3, 19.9],  "HEA 140": [155.4, 24.7],
    "HEA 160": [220.1, 30.4],  "HEA 180": [293.6, 35.5],  "HEA 200": [388.6, 42.3],
    "HEA 220": [515.2, 50.5],  "HEA 240": [675.1, 60.3],  "HEA 260": [836.4, 68.2],
    "HEA 280": [1013, 76.4],   "HEA 300": [1260, 88.3],   "HEA 320": [1479, 97.6],
    "HEA 340": [1678, 105.0],  "HEA 360": [1888, 112.0],  "HEA 400": [2311, 125.0],
    "HEA 450": [2896, 140.0],  "HEA 500": [3550, 155.0],  "HEA 550": [4146, 166.0],
    "HEA 600": [4702, 178.0],  "HEA 700": [5764, 204.0],  "HEA 800": [6891, 224.0],
    "HEA 900": [8013, 252.0],  "HEA 1000": [9485, 272.0]
}

# --- YAN PANEL ---
with st.sidebar:
    st.header("⚙️ Parametreler")
    secilen = st.selectbox("Profil Seçin:", list(hea_data.keys()), index=10)
    L = st.number_input("Kiriş Boyu (Metre):", min_value=0.1, value=6.0, step=0.5)
    P_kg = st.number_input("Merkezi Yük (kg):", min_value=0, value=3000, step=100)
    st.write("---")
    st.write(f"**Profil Verisi ({secilen}):**")
    st.write(f"Wx: {hea_data[secilen][0]} cm³")
    st.write(f"Birim Ağırlık: {hea_data[secilen][1]} kg/m")

# --- HESAPLAMA FONKSİYONU ---
def detayli_analiz(profil_adi, L_m, P_kg):
    Wx_mm3 = hea_data[profil_adi][0] * 1000
    G_kg_m = hea_data[profil_adi][1]
    g = 9.81
    
    L_mm = L_m * 1000
    P_N = P_kg * g
    q_N_mm = (G_kg_m * g) / 1000  # kg/m'den N/mm'ye dönüşüm
    
    # Momentler (Nmm)
    M_tekil = (P_N * L_mm) / 4
    M_zati = (q_N_mm * (L_mm**2)) / 8
    M_toplam = M_tekil + M_zati
    
    gerilme = M_toplam / Wx_mm3
    return gerilme, M_tekil, M_zati

res_gerilme, m_t, m_z = detayli_analiz(secilen, L, P_kg)

# --- SONUÇLAR ---
st.subheader(f"📊 {secilen} Analiz Özeti")

col1, col2, col3 = st.columns(3)
col1.metric("Toplam Gerilme", f"{res_gerilme:.2f} MPa")
col2.metric("Zati Moment Payı", f"{(m_z/(m_t+m_z))*100:.1f}%")
col3.metric("Limit", "235 MPa")

if res_gerilme < 235:
    st.success(f"✅ UYGUN. Kapasite Kullanımı: %{(res_gerilme/235)*100:.1f}")
else:
    st.error(f"❌ UYGUN DEĞİL! Akma sınırı aşıldı.")
    
    # AKILLI ÖNERİ SİSTEMİ
    st.divider()
    st.write("🔍 **Otomatik Profil Önerisi:**")
    for ad in hea_data.keys():
        g_kontrol, _, _ = detayli_analiz(ad, L, P_kg)
        if g_kontrol < 235:
            st.info(f"💡 Bu yükleme için minimum **{ad}** profili kullanılmalıdır.")
            break
