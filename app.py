import streamlit as st
from data.user_question import pertanyaan
from data.engine import forward_chaining
from data.data_perawatan import perawatan
from data.data_gejala import gejala
from data.data_rules import rules

# ================== KONFIGURASI HALAMAN ==================
st.set_page_config(
    page_title="Sistem Pakar Jerawat",
    layout="centered"
)

st.title("SISTEM PAKAR IDENTIFIKASI JERAWAT")
st.subheader("Metode Forward Chaining")
st.write("Silakan pilih gejala yang sesuai dengan kondisi Anda.")

fakta = set()

# ================== STEP 1 ==================
st.header("1. Bentuk Jerawat")
opsi_bentuk = {kode: text for _, (text, kode) in pertanyaan["Bentuk Jerawat"].items()}
pilih_bentuk = st.multiselect(
    "Pilih bentuk jerawat:",
    opsi_bentuk.keys(),
    format_func=lambda x: opsi_bentuk[x]
)
fakta.update(pilih_bentuk)

# ================== STEP 2 ==================
st.header("2. Lokasi Jerawat")
opsi_lokasi = {kode: text for _, (text, kode) in pertanyaan["Lokasi"].items()}
pilih_lokasi = st.multiselect(
    "Pilih lokasi jerawat:",
    opsi_lokasi.keys(),
    format_func=lambda x: opsi_lokasi[x]
)
fakta.update(pilih_lokasi)

# ================== STEP 3 ==================
st.header("3. Keluhan Tambahan")
opsi_keluhan = {kode: text for _, (text, kode) in pertanyaan["Keluhan Tambahan"].items()}
pilih_keluhan = st.multiselect(
    "Pilih keluhan tambahan:",
    opsi_keluhan.keys(),
    format_func=lambda x: opsi_keluhan[x]
)
fakta.update(pilih_keluhan)

# ================== STEP 4 (RADIO – WAJIB) ==================
st.header("4. Usia / Gender")
opsi_usia = {kode: text for _, (text, kode) in pertanyaan["Usia / Gender"].items()}
pilih_usia = st.radio(
    "Pilih salah satu:",
    opsi_usia.keys(),
    format_func=lambda x: opsi_usia[x]
)
fakta.add(pilih_usia)

# ================== PROSES DIAGNOSA ==================
if st.button("Proses Diagnosa"):
    if len(fakta) < 2:
        st.warning("Silakan pilih gejala yang lebih spesifik.")
    else:
        # Threshold utama
        hasil = forward_chaining(fakta, threshold=30)

        # Fallback jika terlalu sedikit gejala kuat
        if not hasil:
            st.warning("Gejala belum cukup spesifik. Menampilkan kemungkinan terdekat.")
            hasil = forward_chaining(fakta, threshold=20)

        if not hasil:
            st.error("Tidak ditemukan indikasi penyakit jerawat.")
        else:
            hasil = hasil[:3]  # maksimal 3 hasil

            # ================== DIAGNOSA UTAMA ==================
            utama = hasil[0]
            st.success("Diagnosa Utama")
            st.subheader(utama["nama"])
            st.write(f"Tingkat Keyakinan: **{utama['persentase']} %**")

            gejala_utama = set(rules[utama["kode"]]) & fakta
            st.write("Gejala Pendukung:")
            for g in gejala_utama:
                st.write(f"- {gejala[g]}")

            st.write("Rekomendasi Perawatan:")
            st.info(perawatan[utama["kode"]])

            # ================== ALTERNATIF ==================
            if len(hasil) > 1:
                st.warning("Kemungkinan Alternatif")
                for alt in hasil[1:]:
                    st.write(f"- {alt['nama']} ({alt['persentase']} %)")
