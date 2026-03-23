import streamlit as st
import pandas as pd
from fpdf import FPDF
import io

# --- 1. PDF OLUŞTURMA FONKSİYONU (Türkçe Karakter Destekli) ---
def create_pdf(data):
    # Türkçe karakterleri standart PDF fontlarına (Arial/Helvetica) uygun hale getiren yardımcı
    def tr_fix(text):
        chars = {
            "İ": "I", "ı": "i", "Ş": "S", "ş": "s", "Ğ": "G", "ğ": "g",
            "Ü": "U", "ü": "u", "Ö": "O", "ö": "o", "Ç": "C", "ç": "c"
        }
        for tr, en in chars.items():
            text = str(text).replace(tr, en)
        return text

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    
    # Başlık
    pdf.cell(200, 10, tr_fix("KORKMAZ MUHENDISLIK - ANALIZ RAPORU"), ln=True, align='C')
    pdf.ln(10)
    
    # Verileri tablo gibi alt alta yazdır
    pdf.set_font("Arial", size=12)
    for key, value in data.items():
        line = f"{key}: {value}"
        pdf.cell(200, 10, tr_fix(line), ln=True)
    
    pdf.ln(20)
    pdf.set_font("Arial", 'I', 10)
    pdf.cell(200, 10, tr_fix("Bu rapor sistem tarafından otomatik oluşturulmuştur."), ln=True)
    
    # PDF'i hafızada (buffer) tut ve döndür
    return pdf.output(dest='S').encode('latin-1')

# --- 2. ŞİFRE KONTROLÜ ---
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.title("🔐 Korkmaz Mühendislik Portal")
    password = st.text_input("Giriş Şifresi", type="password")
    if st.button("Giriş Yap"):
        if password == "3685":
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("Hatalı Şifre!")
    st.stop()

# --- 3. ANA UYGULAMA (HESAPLAMA MODÜLÜ) ---
st.title("🏗️ Çelik Kiriş Sehim Analizi")
st.write("Profil seçin ve yük değerlerini girerek kontrol sağlayın.")

col1, col2 = st.columns(2)

with col1:
    profil_tipi = st.selectbox("Profil Tipi", ["IPE", "HEA"])
    span = st.number_input("Açıklık (L) - mm", value=5000)
    load = st.number_input("Toplam Yük (q) - kg/m", value=500)

with col2:
    limit_secimi = st.selectbox("Sehim Limiti", ["L/500", "L/900", "L/1000"])
    # Limit sayısal değeri
    limit_val = int(limit_secimi.split("/")[1])

# Örnek IPE/HEA Atalet Momentleri (Sadeleştirilmiş Veritabanı)
atalet_data = {
    "IPE 100": 171, "IPE 200": 1943, "IPE 300": 8356,
    "HEA 100": 349, "HEA 200": 3692, "HEA 300": 18260
}

secili_profil = st.selectbox("Profil Boyutu", list(atalet_data.keys()))
I_degeri = atalet_data[secili_profil]

if st.button("Hesapla"):
    # Basit sehim formülü: (5 * q * L^4) / (384 * E * I)
    # E = 210.000 N/mm2 (Çelik)
    E = 210000
    q_n_mm = (load * 9.81) / 1000 # kg/m -> N/mm
    sehim = (5 * q_n_mm * (span**4)) / (384 * E * (I_degeri * 10000))
    
    izin_verilen = span / limit_val
    
    st.divider()
    st.subheader("📊 Analiz Sonucu")
    
    res_col1, res_col2 = st.columns(2)
    res_col1.metric("Hesaplanan Sehim", f"{sehim:.2f} mm")
    res_col2.metric("Limit Değer", f"{izin_verilen:.2f} mm")

    if sehim <= izin_verilen:
        st.success("✅ KESİT UYGUN")
        durum = "UYGUN"
    else:
        st.error("❌ KESİT YETERSİZ")
        durum = "YETERSIZ"

    # PDF Raporu için veri hazırlığı
    report_data = {
        "Profil": secili_profil,
        "Aciklik": f"{span} mm",
        "Yuk": f"{load} kg/m",
        "Secilen Limit": limit_secimi,
        "Hesaplanan Sehim": f"{sehim:.2f} mm",
        "Limit Deger": f"{izin_verilen:.2f} mm",
        "Sonuc": durum
    }

    pdf_output = create_pdf(report_data)
    
    st.download_button(
        label="📄 PDF Raporu İndir",
        data=pdf_output,
        file_name="analiz_raporu.pdf",
        mime="application/pdf"
    )
