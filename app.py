import streamlit as st

st.title("🏗️ St 37 Kiriş Uygunluk Testi (HEA 300)")

# Kullanıcı sadece rakam girecek, Python görmeyecek
L = st.number_input("Kiriş Uzunluğu (Metre):", value=5.0)
P_kg = st.number_input("Merkezi Yük (kg):", value=2000)

if st.button("HESAPLA"):
    # Arka plandaki mühendislik hesabı
    Wx = 1260000 
    P_N = P_kg * 9.81
    M_max = (P_N * (L * 1000)) / 4
    gerilme = M_max / Wx
    
    if gerilme < 235:
        st.success(f"✅ UYGUN! Gerilme: {gerilme:.2f} MPa (Sınır: 235 MPa)")
    else:
        st.error(f"❌ TEHLİKE! Gerilme: {gerilme:.2f} MPa akma sınırını aştı!")
