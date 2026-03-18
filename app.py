import streamlit as st

st.set_page_config(page_title="Çelik Hesap Pro", page_icon="🏗️")
st.title("🏗️ Çelik Kiriş Analiz Asistanı")

# Profil Veritabanı (Wx değerleri cm3 cinsinden)
hea_profiller = {
    "HEA 100": 73, "HEA 120": 106, "HEA 140": 155, "HEA 160": 220,
    "HEA 180": 294, "HEA 200": 389, "HEA 220": 515, "HEA 240": 675,
    "HEA 260": 836, "HEA 280": 1010, "HEA 300": 1260, "HEA 320": 1480,
    "HEA 340": 1680, "HEA 360": 1890, "HEA 400": 2310
}

# --- YAN PANEL (Girdiler) ---
with st.sidebar:
    st.header("⚙️ Hesaplama Parametreleri")
    secilen_profil = st.selectbox("Elinizdeki Profil:", list(hea_profiller.keys()), index=10)
    L = st.number_input("Kiriş Uzunluğu (Metre):", min_value=0.1, value=5.0, step=0.1)
    P_kg = st.number_input("Merkezi Yük (kg):", min_value=1, value=2500, step=100)
    st.info("Malzeme: St 37 (Akma: 235 MPa)")

# --- HESAPLAMA MOTORU ---
def gerilme_hesapla(Wx_cm3, L_m, P_kg):
    Wx_mm3 = Wx_cm3 * 1000
    P_N = P_kg * 9.81
    L_mm = L_m * 1000
    M_max = (P_N * L_mm) / 4
    return M_max / Wx_mm3

current_gerilme = gerilme_hesapla(hea_profiller[secilen_profil], L, P_kg)

# --- SONUÇ EKRANI ---
st.subheader(f"📊 {secilen_profil} Analiz Sonucu")

if current_gerilme < 235:
    st.success(f"✅ UYGUN! Gerilme: {current_gerilme:.2f} MPa")
    st.progress(current_gerilme / 235)
else:
    st.error(f"❌ UYGUN DEĞİL! Gerilme: {current_gerilme:.2f} MPa (Sınır aşıldı)")
    
    # AKILLI ÖNERİ KISMI
    st.warning("🔍 **Sizin için uygun profil arıyorum...**")
    uygun_profil = None
    for ad, wx in hea_profiller.items():
        if gerilme_hesapla(wx, L, P_kg) < 235:
            uygun_profil = ad
            break
    
    if uygun_profil:
        st.info(f"💡 ÖNERİ: Bu yük için en az **{uygun_profil}** kullanmalısınız.")
    else:
        st.error("❗ UYARI: Listemizdeki en büyük profil (HEA 400) bile bu yükü kurtarmıyor!")
