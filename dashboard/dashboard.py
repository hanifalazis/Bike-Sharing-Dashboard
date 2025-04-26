import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

# Konfigurasi gaya visualisasi
sns.set(style="darkgrid")

# Load data
main_data = pd.read_csv("dashboard/main_data.csv")

# Konversi kolom tanggal menjadi tipe datetime
main_data["dteday"] = pd.to_datetime(main_data["dteday"], format="%Y-%m-%d")

# Filter tanggal minimum dan maksimum
min_date = main_data["dteday"].min()
max_date = main_data["dteday"].max()

# Sidebar untuk filter
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("img/sepeda.png")

    # Opsi untuk menggunakan filter atau tidak
    use_filter = st.checkbox("Gunakan Filter Rentang Waktu", value=False)

    # Menampilkan filter rentang waktu hanya jika opsi diaktifkan
    if use_filter:
        start_date, end_date = st.date_input(
            label="Rentang Waktu",
            min_value=min_date,
            max_value=max_date,
            value=[min_date, max_date],
        )
    else:
        start_date, end_date = min_date, max_date

# Filter data berdasarkan rentang waktu (jika filter diaktifkan)
filtered_data = main_data[(main_data["dteday"] >= pd.Timestamp(start_date)) & 
                          (main_data["dteday"] <= pd.Timestamp(end_date))]

# Header
st.header('Bike Sharing Dashboard :sparkles:')

# Subheader 1: Tren Penyewa Sepeda Berdasarkan Bulan-Tahun
st.subheader('Tren Penyewa Sepeda Berdasarkan Bulan-Tahun')

# Ekstrak bulan dan tahun
filtered_data['month'] = filtered_data['dteday'].dt.month
filtered_data['year'] = filtered_data['dteday'].dt.year
filtered_data['month_year'] = filtered_data['year'].astype(str) + '-' + filtered_data['month'].astype(str).str.zfill(2)

# Grouping data berdasarkan Bulan-Tahun
monthly_yearly_counts = filtered_data.groupby('month_year')['cnt'].sum().reset_index()

# Membuat line chart
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(x='month_year', y='cnt', data=monthly_yearly_counts, marker='o', ax=ax)
ax.set_xlabel('Bulan-Tahun')
ax.set_ylabel('Jumlah Penyewa')
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
plt.tight_layout()

# Menampilkan plot di Streamlit
st.pyplot(fig)

# Subheader 2: Jumlah Penyewaan Sepeda Berdasarkan Musim
st.subheader('Jumlah Penyewaan Sepeda Berdasarkan Musim')

# Menghitung jumlah penyewaan berdasarkan musim
season_counts = filtered_data.groupby('season')['cnt'].sum().reset_index()

# Membuat bar chart
fig, ax = plt.subplots(figsize=(8, 6))
sns.barplot(x='season', y='cnt', data=season_counts, order=['Spring', 'Summer', 'Fall', 'Winter'], palette='viridis', ax=ax)
ax.set_xlabel('Musim')
ax.set_ylabel('Jumlah Penyewaan')
plt.tight_layout()

# Menampilkan plot di Streamlit
st.pyplot(fig)

# Subheader 3: Clustering Bike Rentals berdasarkan Temperature dan Jumlah Penyewaan
st.subheader('Clustering Bike Rentals berdasarkan Temperature dan Jumlah Penyewaan')

# Membuat cluster berdasarkan suhu dan jumlah penyewaan
temp_bins = [0, 0.5, 0.8, 1.0]
cnt_bins = [0, 4000, 6000, 8000]

# Menambahkan kolom cluster
filtered_data['cluster'] = (
    pd.cut(filtered_data['temp'], bins=temp_bins, labels=False, include_lowest=True) * len(cnt_bins) + 
    pd.cut(filtered_data['cnt'], bins=cnt_bins, labels=False, include_lowest=True)
)

# Membuat scatter plot
fig, ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(x='temp', y='cnt', hue='cluster', data=filtered_data, palette='viridis', ax=ax)
ax.set_xlabel('Temperature')
ax.set_ylabel('Jumlah Penyewaan')
plt.tight_layout()

# Menampilkan plot di Streamlit
st.pyplot(fig)
