import streamlit as st
import time

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Korkmaz Mühendislik v11", layout="centered")

# --- GÜVENLİK VE ŞİFRE ---
if "authed" not in st.session_state:
    st.session_state["authed"] = False

if not st.session_state["authed"]:
    st.title("🔒 Güvenli Giriş")
    sifre_input = st.text_input("4 Haneli Şifreyi Girin:", type="password")
    if st.button("Sistemi Aç"):
        if sifre_input == "3685":
            st.session_state["authed"] = True
            st.session_state["start_time"] = time.time()
            st.rerun()
        else:
            st.error("❌ Hatalı Şifre!")
    st.stop()

# --- 2 DAKİKA ZAMAN SINIRI ---
gecen = time.time() - st.session_state["start_time"]
kalan = int(120 - gecen)

if kalan <= 0:
    st.session_state["authed"] = False
    st.error("⌛ Süre bitti! Güvenlik için çıkış yapıldı.")
    st.stop()

st.sidebar.markdown(f"### ⏳ Kalan Süre: {kalan} sn")

# --- VERİTABANI (Ağırlık ve Atalet Değerleri) ---
# [Ağırlık kg/m, Ix cm4]
ipe_db = {
    "IPE 100": [8.1, 171.0], "IPE 140": [12.9, 541.2], "IPE 200": [22.4, 1943.0],
    "IPE 240": [30.7, 3892.0], "IPE 300": [42.2, 8356.0], "IPE 400": [66.3, 23130.0],
    "IPE 500": [90.7, 48200.0], "IPE 600": [122.0, 92080.0]
}

st.title("🏗️ Zati Ağırlık Dahil Toplam Sehim")
st.write("Kirişin kendi ağırlığı ve üzerindeki yük birlikte hesaplanır.")

# --- GİRDİLER ---
col1, col2 = st.columns(2)
with col1:
    L = st.number_input("Kiriş Açıklığı (m):", value=40.0)
    P_kg = st.number_input("Üzerindeki Tekil Yük (kg):", value=10.0)
with col2:
    limit_kat = st.selectbox("Sehim Limiti (L/X):", [300, 500, 1000], index=1)
    secilen = st.selectbox("Profil Seç:", list(ipe_db.keys()), index=len(ipe_db)-1)

# --- HESAPLAMA MOTORU ---
if st.button("HESAPLA VE CHECK ET 🔍"):
    # Sabitler ve Dönüşümler
    E = 210000 # N/mm2
    L_mm = L * 1000
    I_mm4 = ipe_db[secilen][1] * 10000
    q_kg_m = ipe_db[secilen][0]
    q_N_mm = (q_kg_m * 9.81) / 1000 # kg/m -> N/mm çevrimi
    P_N = P_kg * 9.81
    limit_mm = L_mm / limit_kat

    # 1. Zati Ağırlık Sehimi (Yayılı Yük Formülü: 5qL^4 / 384EI)
    f_zati = (5 * q_N_mm * (L_mm**4)) / (384 * E * I_mm4)
    
    # 2. Üzerindeki Yük Sehimi (Tekil Yük Formülü: PL^3 / 48EI)
    f_yuk = (P_N * (L_mm**3)) / (48 * E * I_mm4)
    
    # 3. Toplam Sehim
    toplam_f = f_zati + f_yuk

    # --- SONUÇ EKRANI ---
    st.divider()
    
    # Anti-SS Filigranı (Psikolojik Baskı)
    st.markdown(f"<p style='color:grey; opacity:0.3;'>LISANSLI HESAP - {secilen} - {L}m</p>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Kendi Ağırlığı", f"{f_zati:.2f} mm")
    c2.metric("Üstteki Yük", f"{f_yuk:.2f} mm")
    
    is_safe = toplam_f <= limit_mm
    c3.metric("TOPLAM SEHİM", f"{toplam_f:.2f} mm", 
              delta=f"Limit: {limit_mm:.1f} mm", 
              delta_color="normal" if is_safe else "inverse")

    if is_safe:
        st.success(f"✅ UYGUN: Toplam sehim L/{limit_kat} sınırının altında.")
    else:
        st.error(f"❌ YETERSİZ: Kiriş zati ağırlıktan dolayı çöker! ({toplam_f:.1f} mm > {limit_mm:.1f} mm)")

    # Akıllı Öneri (Yine de en uygununu ara)
    oneri = None
    for ad, veri in ipe_db.items():
        temp_I = veri[1] * 10000
        temp_q = (veri[0] * 9.81) / 1000
        temp_f = ((5 * temp_q * (L_mm**4)) / (384 * E * temp_I)) + ((P_N * (L_mm**3)) / (48 * E * temp_I))
        if temp_f <= limit_mm:
            oneri = ad
            break
    
    if oneri:
        st.info(f"💡 Tavsiye: Bu yükü kurtaran en küçük profil: **{oneri}**")

# Saniye sayacı için otomatik yenileme
time.sleep(1)
st.rerun()
