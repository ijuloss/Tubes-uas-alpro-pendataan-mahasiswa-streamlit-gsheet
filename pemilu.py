import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(
    page_title="PEMILU",
    page_icon="📦",
)
# Judul Tampilan dan Deskripsi
st.title("Pendataan Surat Suara")
st.markdown("##### Lengkapi data dibawah ini !!!")

# Konstanta
CALEG = [
    "AMIN (Capres)",
    "Bu Anna Mu'awwanah",
    "Bu Farida Hidayat",
    "Bpk. Muhammad Mughni",
    "Bpk. Fauzan Fuadi",
    "Bu Anjar Sulandari",
    "Bpk. Mustakim",
]
TPS = [
    "08",
    "10",
    "11",
    "12",
    "14",
    "19",
    "20",
]


# membuat koneksi ke Google Spreadsheet
koneksi = st.connection("gsheets", type=GSheetsConnection)

# Mengambil Data tps yang ada
kumpulan_data = koneksi.read(worksheet="Pemilu", usecols=list(range(4)), ttl=5)
kumpulan_data = kumpulan_data.dropna(how="all")

aksi = st.selectbox(
    "Pilih Opsi Menu:",
    [
        "Tambah Data Suara",
        "Lihat Semua Data",
        "Hapus Data",
    ]
)

if aksi == "Tambah Data Suara":
    st.markdown("Silahkan Lengkapi Data dibawah ini:")
    with st.form(key="suara"):
        # caleg  = st.text_input  (label="Nama Caleg*")
        caleg  = st.selectbox   ("Pilih CAPRES/CALEG*", options = CALEG, index = None)
        tps    = st.selectbox ("Pilih Nomor TPS*", options = TPS, index = None)
        jumlah = st.text_input  ("Masukkan jumlah suara*")
        ket    = st.text_area(label="Keterangan")

        st.markdown("**wajib di isi*")
        tombol_submit = st.form_submit_button (label="Submit Data")

        if tombol_submit:
            if not caleg or not tps:
                st.warning("Pastikan Semua Bidang Wajib diisi.")
            # elif kumpulan_data["Nama"].str.contains(caleg).any()  :
            #     st.warning("Nama Anda Sudah Ada!.")
            else  :
                data_suara = pd.DataFrame(
                    [
                        {
                            "Nama Capres/Caleg" : caleg,
                            "TPS"               : tps,
                            "Jumlah"            : jumlah,
                            "Keterangan"        : ket,
                        }
                    ]
                )
                updated_df = pd.concat([kumpulan_data, data_suara], ignore_index=True)
                koneksi.update(worksheet="Pemilu", data=updated_df)
                st.success("Berhasil Tambah Data Suara!")
                st.balloons()

# Melihat Semua tps
elif aksi == "Lihat Semua Data":
    st.dataframe(kumpulan_data)
                
elif aksi == "Hapus Data":
    hapus_data = st.selectbox(
        "Pilih Nama Yang Datanya Akan dihapus", options = kumpulan_data["Nama Capres/Caleg"].tolist(), index = None
    )

    if st.button("Hapus"):
        kumpulan_data.drop(
            kumpulan_data[kumpulan_data["Nama Capres/Caleg"] == hapus_data].index,
            inplace = True,
        )
        koneksi.update(worksheet="Pemilu", data = kumpulan_data)
        st.success("Data Berhasil di Hapus!")
        st.balloons()
