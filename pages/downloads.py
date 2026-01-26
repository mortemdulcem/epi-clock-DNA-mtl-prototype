import streamlit as st
import os

st.set_page_config(page_title="EpiClock Downloads", layout="wide")

st.markdown("""
<style>
    * {
        font-size: 10pt !important;
    }
    h1 {
        font-size: 14pt !important;
    }
    .stDownloadButton button {
        font-size: 10pt !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("EpiClock v4.0 - Dosya Indirme")
st.markdown("---")

files = {
    "DNA_Metilasyon_EpiClock_v4_Guncel_Makale.pdf": "Q1 MAKALE - v4.0 Guncel (11 Standart, 6 sayfa, 22 KB)",
    "Makale_Orijinal.pdf": "Orijinal Makale (945 KB, 29 sayfa)",
    "EpiClock_Sunum_97_Slayt.pptx": "Kapsamli Sunum (29 MB, 97 slayt)",
    "EpiClock_v4_Sunum_20260126.pptx": "Guncel Sunum - 26 Ocak 2026 (97 KB, 51 slayt)",
    "EpiClock_v4_Sunum_20251206.pptx": "Eski Sunum - 6 Aralik 2025 (85 KB)"
}

for filename, description in files.items():
    filepath = f"/home/runner/workspace/{filename}"
    if os.path.exists(filepath):
        with open(filepath, "rb") as f:
            st.download_button(
                label=f"Indir: {description}",
                data=f.read(),
                file_name=filename,
                mime="application/octet-stream",
                key=filename
            )
    else:
        st.warning(f"{filename} bulunamadi")

st.markdown("---")
st.info("Dosyalari indirmek icin yukardaki butonlara tiklayin.")
