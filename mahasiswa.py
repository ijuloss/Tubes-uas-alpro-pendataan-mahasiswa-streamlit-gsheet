import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Judul Tampilan dan Deskripsi
st.title("TUGAS BESAR UAS ALGORITMA DAN PEMROGRAMAN")
st.title("Pendataan Mahasiswa Teknik Elektro `23")

# Konstanta
AGAMA = [
    "ISLAM",
    "KRISTEN",
    "KATOLIK",
    "HINDU",
    "BUDHA",
    "KONGHUCU",
]

KELAS = [
    'EE-06-01',
    'EE-06-02',
]
KEGIATAN = [
    "Riset Dosen",
    "ORMAWA",
    "PKM",
    "UKM",
    "Lainnya",
]


# membuat koneksi ke Google Spreadsheet
koneksi = st.connection("gsheets", type=GSheetsConnection)

# Mengambil data Mahasiswa yang ada
kumpulan_data = koneksi.read(worksheet="Data mahasiswa", usecols=list(range(11)), ttl=5)
kumpulan_data = kumpulan_data.dropna(how="all")

aksi = st.selectbox(
    "Pilih Opsi Menu:",
    [
        "Tambah Data Mahasiswa",
        "Update Data Mahasiswa",
        "Lihat Semua Data Mahasiswa",
        "Hapus Data Mahasiswa",
    ],
)

if aksi == "Tambah Data Mahasiswa":
    st.markdown("Silahkan Lengkapi Data dibawah ini:")
    with st.form(key="Data mahasiswa"):
        nama_lengkap = st.text_input  (label="NAMA LENGKAP*")
        nim          = st.text_input  (label="NIM*")
        kelas        = st.selectbox   ("KELAS*", options = KELAS, index = None)
        ttl          = st.text_input  (label="Tempat Tanggal Lahir*")
        agama        = st.selectbox   ("AGAMA*", options = AGAMA, index = None)
        alamat       = st.text_area   (label="Alamat Lengkap*")
        pos          = st.text_input  (label="Kode Pos")
        nmr_wa       = st.text_input  (label="Nomor WhatsApp")
        sekolah      = st.text_input  (label="Asal sekolah")
        hobi         = st.text_input  (label="HOBI")
        kegiatan_mhs = st.multiselect ("Pilih kegiatan yang di ikuti (*bisa lebih dari satu)", options=KEGIATAN)

        st.markdown("**wajib di isi*")
        tombol_submit = st.form_submit_button (label="Submit Data")

        if tombol_submit:
            if not nama_lengkap or not nim:
                st.warning("Pastikan Semua Bidang Wajib diisi.")
            elif kumpulan_data["Nama Lengkap"].str.contains(nama_lengkap).any()  :
                st.warning("Data Mahasiswa Sudah Ada.")
            else  :
                data_mahasiswa = pd.DataFrame(
                    [
                        {
                            "Nama Lengkap"          : nama_lengkap,
                            "NIM"                   : nim,
                            "KELAS"                 : kelas,
                            "Tempat/Tgl. Lahir"     : ttl,
                            "AGAMA"                 : agama,
                            "Alamat Lengkap"        : alamat,
                            "Kode Pos"              : pos,
                            "Nomor WhatsApp"        : nmr_wa,
                            "Asal Sekolah"          : sekolah,
                            "HOBI"                  : hobi,
                            "Kegiatan Yang diikuti" : ", ".join(kegiatan_mhs),
                        }
                    ]
                )
                updated_df = pd.concat([kumpulan_data, data_mahasiswa], ignore_index=True)
                koneksi.update(worksheet="Data mahasiswa", data=updated_df)
                st.success("Berhasil Menambah Data Mahasiswa!")
                st.balloons()

elif aksi == "Update Data Mahasiswa":
    st.markdown("Pilih Data yang Akan di Perbarui")

    update_mahasiswa = st.selectbox(
        "Pilih Nama yang Datanya akan di Perbarui", options = kumpulan_data["Nama Lengkap"].tolist()
    )
    data_mahasiswa = kumpulan_data[kumpulan_data["Nama Lengkap"] == update_mahasiswa].iloc[0]

    with st.form(key = "update_form"):
        nama_lengkap = st.text_input(
            label="Nama Lengkap*", value = data_mahasiswa["Nama Lengkap"]
        )
        nim = st.text_input(
            label="NIM*", value = data_mahasiswa["NIM"]
        )
        kelas = st.selectbox(
            'KELAS*',
            options=KELAS,
            index=KELAS.index(data_mahasiswa["KELAS"]),
        )
        ttl = st.text_input(
            label="Tempat/Tgl. Lahir*", value = data_mahasiswa["Tempat/Tgl. Lahir"]
        )
        agama = st.selectbox(
            "AGAMA*",
            options=AGAMA,
            index=AGAMA.index(data_mahasiswa["AGAMA"]),
        )
        alamat = st.text_area(
            label="Alamat Lengkap", value = data_mahasiswa["Alamat Lengkap"]
        )
        
        pos = st.text_input(
            label="Kode Pos", value = data_mahasiswa["Kode Pos"]
        )
        nmr_wa = st.text_input(
            label="Nomor WhatsApp*", value = data_mahasiswa["Nomor WhatsApp"]
        )
        sekolah = st.text_input(
            label="Asal Sekolah", value = data_mahasiswa["Asal Sekolah"]
        )
        hobi = st.text_input(
            label="HOBI", value = data_mahasiswa["HOBI"]
        )
        kegiatan_mhs = st.multiselect(
            "Pilih kegiatan yang di ikuti",
            options=KEGIATAN,
            default= data_mahasiswa["Kegiatan Yang diikuti"].split(", "),
        )
        

        st.markdown("**wajib di isi*")
        tombol_update = st.form_submit_button(label="Perbarui Data Mahasisiwa")

        if tombol_update:
            if not nama_lengkap or not nim:
                st.warning("Pastikan Semua Bidang Wajib diisi.")
            else:
                # Menghapus entri lama
                kumpulan_data.drop(
                    kumpulan_data[
                        kumpulan_data["Nama Lengkap"] == update_mahasiswa
                    ].index,
                    inplace = True,
                )
                # Membuat entri data yang diperbarui
                updated_data_mahasiswa = pd.DataFrame(
                    [
                        {
                            "Nama Lengkap"          : nama_lengkap,
                            "NIM"                   : nim,
                            "KELAS"                 : kelas,
                            "Tempat/Tgl. Lahir"     : ttl,
                            "AGAMA"                 : agama,
                            "Alamat Lengkap"        : alamat,
                            "Kode Pos"              : pos,
                            "Nomor WhatsApp"        : nmr_wa,
                            "Asal Sekolah"          : sekolah,
                            "HOBI"                  : hobi,
                            "Kegiatan Yang diikuti" : ", ".join(kegiatan_mhs),
                        }
                    ]
                )
                # Menambahkan data yang diperbarui ke Spreadsheet
                updated_df = pd.concat(
                    [kumpulan_data, updated_data_mahasiswa], ignore_index = True
                )
                koneksi.update(worksheet="Data mahasiswa", data = updated_df)
                st.success("Berhasil Perbarui Data Mahasiswa!")
                st.balloons()

# Melihat Semua Data Mahasiswa
elif aksi == "Lihat Semua Data Mahasiswa":
    st.dataframe(kumpulan_data)

# Menghapus Data Mahasiswa
elif aksi == "Hapus Data Mahasiswa":
    hapus_data = st.selectbox(
        "Pilih Nama Yang Datanya Akan dihapus", options = kumpulan_data["Nama Lengkap"].tolist()
    )

    if st.button("Hapus"):
        kumpulan_data.drop(
            kumpulan_data[kumpulan_data["Nama Lengkap"] == hapus_data].index,
            inplace = True,
        )
        koneksi.update(worksheet="Data mahasiswa", data = kumpulan_data)
        st.success("Data Berhasil di Hapus!")
        st.balloons()
