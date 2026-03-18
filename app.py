import streamlit as st

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Korkmaz Mühendislik v12", layout="wide")

# --- GÜVENLİK ---
if "authed" not in st.session_state:
    st.session_state["authed"] = False

if not st.session_state["authed"]:
    st.title("🔒 Güvenli Giriş")
    sifre_input = st.text_input("Şifreyi Girin:", type="password")
    if st.button("Giriş Yap"):
        if sifre_input == "3685":
            st.session_state["authed"] = True
            st.rerun()
        else:
            st.error("Şifre Hatalı!")
    st.stop()

# --- VERİTABANI (Ağırlık kg/m, Ix cm4) ---
hea_db = {
    "HEA 100": [16.7, 349.2], "HEA 120": [19.9, 606.2], "HEA 140": [24.7, 1033.0],
    "HEA 160": [30.4, 1673.0], "HEA 180": [35.5, 2510.0], "HEA 200": [42.3, 3692.0],
    "HEA 220": [50.5, 5410.0], "HEA 240": [60.3, 7763.0], "HEA 260": [68.2, 10450.0],
    "HEA 280": [76.4, 13670.0], "HEA 300": [88.3, 18260.0], "HEA 400": [125.0, 45070.0],
    "HEA 500": [155.0, 86970.0], "HEA 600": [178.0, 141200.0]
}

ipe_db = {
    "IPE 100": [8.1, 171.0], "IPE 120": [10.4, 317.8], "IPE 140": [12.9, 541.2],
    "IPE 160": [15.8, 869.3], "IPE 180": [18.8, 1317.0], "IPE 200": [22.4, 1943.0],
    "IPE 220": [26.2, 2772.0], "IPE 240": [30.7, 3892.0], "IPE 270": [36.1, 5790.0],
    "IPE 300": [42.2, 8356.0], "IPE 330": [49.1, 11770.0], "IPE 360": [57.1, 16270.0],
    "IPE 400": [66.3, 23130.0], "IPE 450": [77.6, 33740.0], "IPE 500": [90.7, 48200.0],
    "IPE 600": [122.0, 92080.0]
}

st.title("🏗️ Korkmaz Akıllı Analiz Paneli")
st.info("Bu sürümde zaman sınırlaması yoktur. Zati ağırlık hesaba dahildir.")

# --- GİRDİLER ---
with st.container():
    c1, c2, c3 = st.columns(3)
    with c1:
        L = st.number_input("Kiriş Açıklığı (m):", value=6.0, step=1.0)
        P_kg = st.number_input("Üstteki Tekil Yük (kg):", value=1000, step=100)
    with c2:
        tip = st.radio("Profil Serisi:", ["IPE", "HEA"])
        current_db = ipe_db if tip == "IPE" else hea_db
        secilen = st.selectbox("Manuel Profil Seç:", list(current_db.keys()))
    with c3:
        limit_kat = st.selectbox("Sehim Limiti (L/X):", [200, 300, 500], index=1)

# --- HESAPLAMA ---
if st.button("ANALİZİ BAŞLAT"):
    E = 210000
    L_mm = L * 1000
    I_mm4 = current_db[secilen][1] * 10000
    q_N_mm = (current_db[secilen][0] * 9.81) / 1000
    P_N = P_kg * 9.81
    limit_mm = L_mm / limit_kat

    # Sehimler
    f_zati = (5 * q_N_mm * (L_mm**4)) / (384 * E * I_mm4)
    f_yuk = (P_N * (L_mm**3)) / (48 * E * I_mm4)
    toplam_f = f_zati + f_yuk

    # Sonuç Görselleştirme
    st.divider()
    res_c1, res_c2, res_c3 = st.columns(3)
    
    res_c1.metric("Kendi Ağırlık Sehimi", f"{f_zati:.2f} mm")
    res_c2.metric("Yük Sehimi", f"{f_yuk:.2f} mm")
    
    status = toplam_f <= limit_mm
    res_c3.metric("TOPLAM SEHİM", f"{toplam_f:.2f} mm", 
                  f"Limit: {limit_mm:.1f} mm", 
                  delta_color="normal" if status else "inverse")

    if status:
        st.success(f"✅ Seçilen {secilen} bu yükler altında UYGUNDUR.")
    else:
        st.error(f"❌ Seçilen {secilen} YETERSİZDİR!")

    # AKILLI ÖNERİ SİSTEMİ
    st.subheader("💡 Akıllı Öneri Listesi")
    oneri_bulundu = False
    
    # Tüm listeyi tara ve kurtaranları bul
    for ad, veri in current_db.items():
        temp_I = veri[1] * 10000
        temp_q = (veri[0] * 9.81) / 1000
        temp_f = ((5 * temp_q * (L_mm**4)) / (384 * E * temp_I)) + ((P_N * (L_mm**3)) / (48 * E * temp_I))
        
        if temp_f <= limit_mm:
            st.write(f"👉 **{ad}** kullanılabilir. (Toplam Sehim: {temp_f:.2f} mm)")
            oneri_bulundu = True
            break # Sadece en ekonomik (ilk kurtaranı) gösterip durur
            
    if not oneri_bulundu:
        st.warning("Bu açıklık ve yük için seçilen seride uygun profil bulunamadı!")

if st.sidebar.button("Güvenli Çıkış"):
    st.session_state["authed"] = False
    st.rerun()
