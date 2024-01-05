import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd


# Judul Tampilan dan Deskripsi
st.title("SELAMAT DATANG DI IJUL PRINT")
st.title("Silahkan isi formulir ini jika mau print")

# Konstanta
KELOMPOK = [
    "KELOMPOK 1",
    "KELOMPOK 2",
    "KELOMPOK 3",
    "KELOMPOK 4",
    "KELOMPOK 5",
    "KELOMPOK 6",
]
PRINT = [
    "Cover Laporan Resmi",
    "Kata Pengantar",
    "Penutup",
    "LAINNYA",
]


# membuat koneksi ke Google Spreadsheet
koneksi = st.connection("gsheets", type=GSheetsConnection)

# Mengambil Data Print yang ada
kumpulan_data = koneksi.read(worksheet="print", usecols=list(range(4)), ttl=5)
kumpulan_data = kumpulan_data.dropna(how="all")

aksi = st.selectbox(
    "Pilih Opsi Menu:",
    [
        "Tambah Data Print",
        "Lihat Semua Data Print",
    ],
)

if aksi == "Tambah Data Print":
    st.markdown("Silahkan Lengkapi Data dibawah ini:")
    with st.form(key="print"):
        nama = st.text_input  (label="NAMA*")
        kelompok        = st.selectbox   ("KELOMPOK*", options = KELOMPOK, index = None)
        print = st.multiselect ("Pilih print apa saja (*bisa lebih dari satu)", options=PRINT)
        Catatan = st.text_area(label="Catatan untuk saya")

        st.markdown("**wajib di isi*")
        tombol_submit = st.form_submit_button (label="Submit Data")

        if tombol_submit:
            if not nama or not print:
                st.warning("Pastikan Semua Bidang Wajib diisi.")
            elif kumpulan_data["Nama"].str.contains(nama).any()  :
                st.warning("Nama Anda Sudah Ada!.")
            else  :
                data_print = pd.DataFrame(
                    [
                        {
                            "Nama"              : nama,
                            "KELOMPOK"          : kelompok,
                            "Print apa saja"    : ", ".join(print),
                            "Catatan"           : Catatan,
                        }
                    ]
                )
                updated_df = pd.concat([kumpulan_data, data_print], ignore_index=True)
                koneksi.update(worksheet="print", data=updated_df)
                st.success("Berhasil Tambah Data Print!")
                st.balloons()

# Melihat Semua print
elif aksi == "Lihat Semua Data Print":
    st.dataframe(kumpulan_data)
