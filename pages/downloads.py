import streamlit as st
import os

st.set_page_config(page_title="EpiClock Downloads", layout="wide")

st.title("EpiClock v4.0 - Dosya Indirme")

files = {
    "Makale_Orijinal.pdf": "Orijinal Makale (945 KB)",
    "EpiClock_v4_Sunum_20260126.pptx": "Guncel Sunum - 26 Ocak 2026 (97 KB)",
    "EpiClock_v4_Sunum_20251206.pptx": "Eski Sunum - 6 Aralik 2025 (85 KB)",
    "EpiClock_Dosyalar.zip": "Tum Dosyalar ZIP (649 KB)"
}

for filename, description in files.items():
    filepath = f"/home/runner/workspace/{filename}"
    if os.path.exists(filepath):
        with open(filepath, "rb") as f:
            st.download_button(
                label=f"Indir: {description}",
                data=f.read(),
                file_name=filename,
                mime="application/octet-stream"
            )
    else:
        st.warning(f"{filename} bulunamadi")
