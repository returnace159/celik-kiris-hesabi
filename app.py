import streamlit as st

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Korkmaz Mühendislik v7", layout="centered")

# --- ŞİFRE MEKANİZMASI ---
if "authed" not in st.session_state:
    st.session_state["authed"] = False

if not st.session_state["authed"]:
    st.title("🔒 Korkmaz Analiz - Giriş")
    sifre_input = st.text_input("4 Haneli Giriş Şifresini Yazın:", type="password")
    if st.button("Sistemi Aç"):
        if sifre_input == "3685": # Senin istediğin yeni şifre
            st.session_state["authed"] = True
            st.rerun()
        else:
            st.error("❌ Şifre Yanlış! Erişim Reddedildi.")
    st.stop()

# --- PROGRAMIN ANA GÖVDESİ ---
st.title("🏗️ Korkmaz Akıllı Profil Analizi")
st.sidebar.success("Oturum Açıldı ✅")

# --- VERİTABANLARI (PDF'den Sadeleştirilmiş) ---
hea_db = {
    "HEA 100": 349.2, "HEA 120": 606.2, "HEA 140": 1033.0, "HEA 160": 1673.0,
    "HEA 180": 2510.0, "HEA 200": 3692.0, "HEA 240": 7763.0, "HEA 300": 18260.0,
    "HEA 400": 45070.0, "HEA 500": 86970.0, "HEA 600": 141200.0
}

ipe_db = {
    "IPE 100": 171.0, "IPE 120": 317.8, "IPE 140": 541.2, "IPE 160": 869.3,
    "IPE 180": 1317.0, "IPE 200": 1943.0, "IPE 220": 2772.0, "IPE 240": 3892.0,
    "IPE 270": 5790.0, "IPE 300": 8356.0, "IPE 330": 11770.0, "IPE 360": 16270.0,
    "IPE 400": 23130.0, "IPE 500": 48200.0, "IPE 600": 92080.0
}

# --- GİRDİLER ---
col1, col2 = st.columns(2)
with col1:
    L = st.number_input("Kiriş Boyu (metre):", value=6.0, step=0.5)
    P_kg = st.number_input("Yük (kg):", value=2000, step=100)
    oran_limit = st.selectbox("Sehim Limiti (L/X):", [300, 500, 900, 1000], index=1)

with col2:
    tip = st.radio("Profil Tipi:", ["HEA", "IPE"])
    current_db = hea_db if tip == "HEA" else ipe_db
    secilen_manuel = st.selectbox("Manuel Profil Seç (Okuma):", list(current_db.keys()), index=5)

# --- ANALİZ VE HESAPLAMA ---
if st.button("HESAPLA VE EN İYİSİNİ ÖNER 🔍"):
    L_mm = L * 1000
    P_N = P_kg * 9.81
    E = 210000
    hedef_limit = L_mm / oran_limit
    
    # 1. Akıllı Öneri (Küçükten büyüğe tarama)
    oneri_profil = None
    for ad, ix_cm4 in current_db.items():
        if ( (P_N * (L_mm**3)) / (48 * E * (ix_cm4 * 10000)) ) <= hedef_limit:
            oneri_profil = ad
            break
            
    # 2. Manuel Seçim Analizi
    ix_secilen = current_db[secilen_manuel] * 10000
    sehim_manuel = (P_N * (L_mm**3)) / (48 * E * ix_secilen)
    oran_manuel = L_mm / sehim_manuel if sehim_manuel > 0 else 0

    st.divider()

    # Öneri Kısmı
    if oneri_profil:
        st.info(f"💡 **AKILLI ÖNERİ:** Bu şartlarda en ekonomik kesit: **{oneri_profil}**")
    else:
        st.warning("⚠️ **DİKKAT:** Listedeki hiçbir profil bu yük/limit şartını sağlamıyor!")

    # Manuel Okuma Kısmı
    st.subheader(f"📊 Manuel Analiz: {secilen_manuel}")
    c1, c2, c3 = st.columns(3)
    c1.metric("Mevcut Sehim", f"{sehim_manuel:.2f} mm")
    c2.metric("Limit", f"{hedef_limit:.2f} mm")
    c3.metric("Mevcut Oran", f"L/{int(oran_manuel)}")

    if sehim_manuel <= hedef_limit:
        st.success(f"✅ {secilen_manuel} KURTARIYOR")
    else:
        st.error(f"❌ {secilen_manuel} YETERSİZ")

# --- ÇIKIŞ BUTONU ---
if st.sidebar.button("Güvenli Çıkış 🚪"):
    st.session_state["authed"] = False
    st.rerun()
