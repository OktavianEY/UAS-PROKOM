# UAS Pemograman Komputer
# NAMA : Oktavian Ezeddin Yusuf
# NIM : 12220144

import json

import pandas as pd
import plotly.express as px
import streamlit as st

#Sidebar
st.sidebar.text("Ujian Akhir Semester\nPemograman Komputer ITB 2021")
st.sidebar.caption("Menganalisa Data produk Minyak Mentah dari Seluruh Dunia")

st.sidebar.text('Nama : Oktavian Ezeddin Yusuf \nNIM : 12220144')

list_region = []
list_region2 = []
list_kodehuruf = []
list_organisasi = []
list_nama = []
list_angka = []

# data1
produksi = []
tahun = []

#data2
isi_frame2 = []

#data 3
sum_oil = []
frame3_details= []

#data4
frame4_angka = []
frame4_nama = []
frame4_region = []
frame4_subregion = []

f = open ("kode_negara_lengkap.json")
file_json = json.load(f)
df_csv = pd.read_csv("produksi_minyak_mentah.csv")
df_json = pd.DataFrame.from_dict(file_json,orient='columns')

for i in list(df_csv['kode_negara']):
    if i not in list_kodehuruf:
        list_kodehuruf.append(i)

for i in list_kodehuruf:
    if i not in list(df_json['alpha-3']):
        list_organisasi.append(i)

for i in list_organisasi:
    df_csv = df_csv[df_csv.kode_negara != i]
    if i in list_kodehuruf:
        list_kodehuruf.remove(i)

for i in range(len(list_kodehuruf)):
    for j in range(len(list(df_json['alpha-3']))):
        if list(df_json['alpha-3'])[j] == list_kodehuruf[i] and list(df_json['name'])[j] not in list_nama:
            list_nama.append(list(df_json['name'])[j])
            list_angka.append(list(df_json['country-code'])[j])
            list_region.append(list(df_json['region'])[j])
            list_region2.append(list(df_json['sub-region'])[j])

negara = pd.DataFrame(list(zip(list_nama, list_kodehuruf, list_angka, list_region, list_region2)), columns=[
                         'Negara', 'alpha-3', 'Kode_Negara', 'Region', 'Sub-Region'])

#Header
st.header('Data Produksi Minyak Mentah dari Seluruh Dunia')

#Data 1
st.subheader('Grafik Jumlah Produksi Minyak Mentah terhadap Waktu suatu Negara')
N = st.selectbox("Pilih Daftar Negara", list_nama)

for i in range(len(list_nama)):
    if list_nama[i] == N:
        kodenegarahuruf = list_kodehuruf[i]
        kodenegaraangka = list_angka[i]
        region = list_region[i]
        subregion = list_region2[i]

for i in range(len(list(df_csv['kode_negara']))):
    if kodenegarahuruf == list(df_csv['kode_negara'])[i]:
        produksi.append(list(df_csv['produksi'])[i])
        tahun.append(list(df_csv['tahun'])[i])

frame1 = df_csv.loc[df_csv['kode_negara']==N]

graph = px.line(x=tahun, y=produksi, labels={
              "x": "tahun", "y": "produksi"})
graph.update_traces(line_color='#ffffff')

st.plotly_chart(graph)

#Data 2
st.subheader('Grafik Jumlah Produksi Minyak Terbesar pada Suatu Tahun') 
T = st.selectbox("Pilih tahun", tahun)

frame2 = df_csv.loc[df_csv['tahun'] == T].sort_values(
    by=['produksi'], ascending=False)

for i in range(len(list(frame2['kode_negara']))):
    for j in range(len(list(negara['alpha-3']))):
        if list(frame2['kode_negara'])[i] == list(negara['alpha-3'])[j]:
            isi_frame2.append(list(negara['Negara'])[j])

frame2['negara'] = isi_frame2

choose1 = int(st.number_input("Pilih jumlah negara yang muncul", min_value=1, max_value=len(frame2)))

frame2 = frame2[:choose1]

graph2 = px.bar(frame2, x='negara', y='produksi')
graph2.update_traces(marker_color='#ffffff')
st.plotly_chart(graph2)

for i in list_kodehuruf:
    a = df_csv.loc[df_csv['kode_negara'] == i, 'produksi'].sum()
    sum_oil.append(a)


# Data 3
frame3 = pd.DataFrame(list(zip(list_kodehuruf, sum_oil)),
                   columns=['kode_negara', 'produksi_kumulatif']).sort_values(by=['produksi_kumulatif'], ascending=False)


for i in range(len(list(frame3['kode_negara']))):
    for j in range(len(list(negara['alpha-3']))):
        if list(frame3['kode_negara'])[i] == list(negara['alpha-3'])[j]:
            frame3_details.append(list(negara['Negara'])[j])

frame3['negara'] = frame3_details
st.subheader('Grafik Jumlah Produksi Kumulatif Minyak Terbesar') 

choose2 = int(st.number_input("Pilih jumlah negara yang muncul", min_value=1,
                           max_value=len(frame3), key="kumulatif"))

frame3 = frame3[:choose2]

graph3 = px.bar(frame3, x='negara', y='produksi_kumulatif')
graph3.update_traces(marker_color='#ffffff')

st.plotly_chart(graph3, use_container_width=True)

#Data 4
st.subheader('Informasi Produksi Minyak Negara')
pilih_tahun = int(st.selectbox("Pilih tahun", tahun, key="Tahun"))

frame4 = df_csv.loc[df_csv['tahun'] == pilih_tahun]
frame4 = frame4.drop(['tahun'], axis=1)
frame4 = frame4.rename(columns={
                 'produksi': 'produksi_tahun-{}'.format(pilih_tahun), 'kode_negara': 'kode_negara_huruf'})

for i in range(len(list(frame4['kode_negara_huruf']))):
    for j in range(len(list(negara['alpha-3']))):
        if list(frame4['kode_negara_huruf'])[i] == list(negara['alpha-3'])[j]:
            frame4_angka.append(list(negara['Kode_Negara'])[j])
            frame4_nama.append(list(negara['Negara'])[j])
            frame4_region.append(list(negara['Region'])[j])
            frame4_subregion.append(list(negara['Sub-Region'])[j])

frame4['kode_negara_angka'] = frame4_angka
frame4['nama'] = frame4_nama
frame4['region'] = frame4_region
frame4['sub-region'] = frame4_subregion

frame4 = frame4[['nama', 'kode_negara_huruf', 'kode_negara_angka', 'region',
           'sub-region', 'produksi_tahun-{}'.format(pilih_tahun)]].sort_values(by=['produksi_tahun-{}'.format(pilih_tahun)], ascending=False)

frame5 = pd.DataFrame(list(zip(list_kodehuruf, sum_oil)),
                   columns=['kode_negara_huruf', 'produksi_kumulatif'])

frame5['nama'] = list(negara['Negara'])
frame5['region'] = list(negara['Region'])
frame5['sub-region'] = list(negara['Sub-Region'])
frame5['kode_negara_angka'] = list(negara['Kode_Negara'])

frame5 = frame5[['nama', 'kode_negara_huruf', 'kode_negara_angka', 'region',
           'sub-region', 'produksi_kumulatif']].sort_values(by=['produksi_kumulatif'], ascending=False)

df_nol = frame4[frame4['produksi_tahun-{}'.format(pilih_tahun)] != 0].sort_values(
    by=['produksi_tahun-{}'.format(pilih_tahun)], ascending=True)

minpro_kumulatif = frame5[frame5['produksi_kumulatif'.format(pilih_tahun)] != 0].sort_values(
    by=['produksi_kumulatif'], ascending=True)

#Expander
with st.expander("Jumlah Produksi Minyak Terbesar"):
    st.metric("Jumlah Produksi Minyak Terbesar Tahun {}".format(
        pilih_tahun), df_nol.iloc[0]['produksi_tahun-{}'.format(pilih_tahun)])
    
    st.caption("{} | {} {} | {} | {}".format(
        df_nol.iloc[0]['nama'], df_nol.iloc[0]['kode_negara_huruf'], df_nol.iloc[0]['kode_negara_angka'], df_nol.iloc[0]['region'], df_nol.iloc[0]['sub-region']))

with st.expander("Jumlah Produksi Minyak Kumulatif Terbesar"):
    st.metric("Jumlah Produksi Minyak Kumulatif Terbesar",
              round(frame5.iloc[0]['produksi_kumulatif'], 3))
    
    st.caption("{} | {} {} | {} | {}".format(
        frame5.iloc[0]['nama'], frame5.iloc[0]['kode_negara_huruf'], frame5.iloc[0]['kode_negara_angka'], frame5.iloc[0]['region'], frame5.iloc[0]['sub-region']))

with st.expander("Jumlah Produksi Minyak Terkecil"):
        st.metric("Jumlah Produksi Minyak Terkecil Tahun {}".format(
            (pilih_tahun)), df_nol.iloc[0]['produksi_tahun-{}'.format(pilih_tahun)])

        st.caption("{} | {} {} | {} | {}".format(
            df_nol.iloc[0]['nama'], df_nol.iloc[0]['kode_negara_huruf'], df_nol.iloc[0]['kode_negara_angka'], df_nol.iloc[0]['region'], df_nol.iloc[0]['sub-region']))
    
with st.expander("Jumlah Produksi Minyak Kumulatif Terkecil"):
        st.metric("Jumlah Produksi Minyak Kumulatif Terkecil",
              minpro_kumulatif.iloc[0]['produksi_kumulatif'])
       
        st.caption("{} | {} {} | {} | {}".format(minpro_kumulatif.iloc[0]['nama'], minpro_kumulatif.iloc[0][
            'kode_negara_huruf'], minpro_kumulatif.iloc[0]['kode_negara_angka'], minpro_kumulatif.iloc[0]['region'], minpro_kumulatif.iloc[0]['sub-region']))
