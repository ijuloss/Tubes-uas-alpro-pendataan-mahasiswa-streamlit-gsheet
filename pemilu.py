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
    "Tps-01",
    "Tps-02",
    "Tps-03",
    "Tps-04",
    "Tps-05",
    "Tps-06",
    "Tps-07",
    "Tps-08",
    "Tps-09",
    "Tps-10",
    "Tps-11",
    "Tps-12",
    "Tps-13",
    "Tps-14",
    "Tps-15",
    "Tps-16",
    "Tps-17",
    "Tps-18",
    "Tps-19",
    "Tps-20",
]


# membuat koneksi ke Google Spreadsheet
koneksi = st.connection("gsheets", type=GSheetsConnection)

# Mengambil Data tps01 yang ada
kumpulan_data = koneksi.read(worksheet="Pemilu", usecols=list(range(23)), ttl=5)
kumpulan_data = kumpulan_data.dropna(how="all")

aksi = st.selectbox(
    "Pilih Opsi Menu:",
    [
        # "Tambah Data Suara",
        "Perbarui Data",
        "Lihat Semua Data",
        # "Hapus Data",
    ]
)

if aksi == "Tambah Data Suara":
    st.markdown("Silahkan Lengkapi Data dibawah ini:")
    with st.form(key="suara"):
        # caleg  = st.number_inpu"Nama Capres/Caleg*")
        caleg  = st.selectbox   ("Pilih CAPRES/CALEG*", options = CALEG, index = None)
        tps01 = st.number_input("TPS-01", format="%d", step=1)
        tps02 = st.number_input("TPS-02", format="%d", step=1)
        tps03 = st.number_input("TPS-03", format="%d", step=1)
        tps04 = st.number_input("TPS-04", format="%d", step=1)
        tps05 = st.number_input("TPS-05", format="%d", step=1)
        tps06 = st.number_input("TPS-06", format="%d", step=1)
        tps07 = st.number_input("TPS-07", format="%d", step=1)
        tps08 = st.number_input("TPS-08", format="%d", step=1)
        tps09 = st.number_input("TPS-09", format="%d", step=1)
        tps10 = st.number_input("TPS-10", format="%d", step=1)
        tps11 = st.number_input("TPS-11", format="%d", step=1)
        tps12 = st.number_input("TPS-12", format="%d", step=1)
        tps13 = st.number_input("TPS-13", format="%d", step=1)
        tps14 = st.number_input("TPS-14", format="%d", step=1)
        tps15 = st.number_input("TPS-15", format="%d", step=1)
        tps16 = st.number_input("TPS-16", format="%d", step=1)
        tps17 = st.number_input("TPS-17", format="%d", step=1)
        tps18 = st.number_input("TPS-18", format="%d", step=1)
        tps19 = st.number_input("TPS-19", format="%d", step=1)
        tps20 = st.number_input("TPS-20", format="%d", step=1)
        total  = st.number_input("Masukkan total suara", format="%d", step=1)
        ket    = st.text_are("Keterangan")

        st.markdown("**wajib di isi*")
        tombol_submit = st.form_submit_button(label="Submit Data")

        if tombol_submit:
            if not caleg:
                st.warning("Pastikan Semua Bidang Wajib diisi.")
            # elif kumpulan_data["Nama"].str.contains(caleg).any()  :
            #     st.warning("Nama Anda Sudah Ada!.")
            else  :
                data_suara = pd.DataFrame(
                    [
                        {
                            "Nama Capres/Caleg" : caleg,
                            "TPS-01"            : tps01,
                            "TPS-02"            : tps02,
                            "TPS-03"            : tps03,
                            "TPS-04"            : tps04,
                            "TPS-05"            : tps05,
                            "TPS-06"            : tps06,
                            "TPS-07"            : tps07,
                            "TPS-08"            : tps08,
                            "TPS-09"            : tps09,
                            "TPS-10"            : tps10,
                            "TPS-11"            : tps11,
                            "TPS-12"            : tps12,
                            "TPS-13"            : tps13,
                            "TPS-14"            : tps14,
                            "TPS-15"            : tps15,
                            "TPS-16"            : tps16,
                            "TPS-17"            : tps17,
                            "TPS-18"            : tps18,
                            "TPS-19"            : tps19,
                            "TPS-20"            : tps20,
                            "Total"             : total,
                            "Keterangan"        : ket,
                        }
                    ]
                )
                updated_df = pd.concat([kumpulan_data, data_suara], ignore_index=True)
                koneksi.update(worksheet="Pemilu", data=updated_df)
                st.success("Berhasil Tambah Data Suara!")
                st.balloons()

elif aksi == "Perbarui Data":
    st.markdown("Pilih Data yang Akan di Perbarui")

    update_data_suara = st.selectbox(
        "Pilih Nama yang Datanya akan di Perbarui", options = kumpulan_data["Nama Capres/Caleg"].tolist()
    )
    data_suara = kumpulan_data[kumpulan_data["Nama Capres/Caleg"] == update_data_suara].iloc[0]

    with st.form(key = "update_form"):
        caleg = st.text_input("Nama Capres/Caleg*", value = data_suara["Nama Capres/Caleg"])
        
        tps01 = st.number_input("TPS-01", format="%d", step=1, value= int(data_suara["TPS-01"]))
        tps02 = st.number_input("TPS-02", format="%d", step=1, value= int(data_suara["TPS-02"]))
        tps03 = st.number_input("TPS-03", format="%d", step=1, value= int(data_suara["TPS-03"]))
        tps04 = st.number_input("TPS-04", format="%d", step=1, value= int(data_suara["TPS-04"]))
        tps05 = st.number_input("TPS-05", format="%d", step=1, value= int(data_suara["TPS-05"]))
        tps06 = st.number_input("TPS-06", format="%d", step=1, value= int(data_suara["TPS-06"]))
        tps07 = st.number_input("TPS-07", format="%d", step=1, value= int(data_suara["TPS-07"]))
        tps08 = st.number_input("TPS-08", format="%d", step=1, value= int(data_suara["TPS-08"]))
        tps09 = st.number_input("TPS-09", format="%d", step=1, value= int(data_suara["TPS-09"]))
        tps10 = st.number_input("TPS-10", format="%d", step=1, value= int(data_suara["TPS-10"]))
        tps11 = st.number_input("TPS-11", format="%d", step=1, value= int(data_suara["TPS-11"]))
        tps12 = st.number_input("TPS-12", format="%d", step=1, value= int(data_suara["TPS-12"]))
        tps13 = st.number_input("TPS-13", format="%d", step=1, value= int(data_suara["TPS-13"]))
        tps14 = st.number_input("TPS-14", format="%d", step=1, value= int(data_suara["TPS-14"]))
        tps15 = st.number_input("TPS-15", format="%d", step=1, value= int(data_suara["TPS-15"]))
        tps16 = st.number_input("TPS-16", format="%d", step=1, value= int(data_suara["TPS-16"]))
        tps17 = st.number_input("TPS-17", format="%d", step=1, value= int(data_suara["TPS-17"]))
        tps18 = st.number_input("TPS-18", format="%d", step=1, value= int(data_suara["TPS-18"]))
        tps19 = st.number_input("TPS-19", format="%d", step=1, value= int(data_suara["TPS-19"]))
        tps20 = st.number_input("TPS-20", format="%d", step=1, value= int(data_suara["TPS-20"]))
        
        total = st.number_input("Total", format="%d", step=1, value = int(data_suara["Total"]))
        ket   = st.text_area("Keterangan", value=data_suara["Keterangan"])
        
        st.markdown("**wajib di isi*")
        tombol_update = st.form_submit_button(label="Perbarui Data Suara")

        if tombol_update:
            if not caleg:
                st.warning("Pastikan Semua Bidang Wajib diisi.")
            else:
                # Menghapus entri lama
                kumpulan_data.drop(
                    kumpulan_data[
                        kumpulan_data["Nama Capres/Caleg"] == update_data_suara
                    ].index,
                    inplace = True,
                )
                # Membuat entri data yang diperbarui
                update_suara = pd.DataFrame(
                    [
                        {
                            "Nama Capres/Caleg" : caleg,
                            "TPS-01"            : tps01,
                            "TPS-02"            : tps02,
                            "TPS-03"            : tps03,
                            "TPS-04"            : tps04,
                            "TPS-05"            : tps05,
                            "TPS-06"            : tps06,
                            "TPS-07"            : tps07,
                            "TPS-08"            : tps08,
                            "TPS-09"            : tps09,
                            "TPS-10"            : tps10,
                            "TPS-11"            : tps11,
                            "TPS-12"            : tps12,
                            "TPS-13"            : tps13,
                            "TPS-14"            : tps14,
                            "TPS-15"            : tps15,
                            "TPS-16"            : tps16,
                            "TPS-17"            : tps17,
                            "TPS-18"            : tps18,
                            "TPS-19"            : tps19,
                            "TPS-20"            : tps20,
                            "Total"             : total,
                            "Keterangan"        : ket,
                        }
                    ]
                )
                # Menambahkan data yang diperbarui ke Spreadsheet
                updated_df = pd.concat(
                    [kumpulan_data, update_suara], ignore_index = True
                )
                koneksi.update(worksheet="Pemilu", data = updated_df)
                st.success("Berhasil Perbarui Data Suara!")
                st.balloons()

# Melihat Semua tps01
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
