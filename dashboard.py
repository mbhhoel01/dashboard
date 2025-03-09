import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Set style for seaborn
sns.set(style='darkgrid')

# Helper functions
def create_daily_pm25_df(df):
    daily_pm25_df = df.resample(rule='D', on='datetime').agg({
        "PM2.5": "mean"
    })
    daily_pm25_df = daily_pm25_df.reset_index()
    daily_pm25_df.rename(columns={"PM2.5": "average_pm25"}, inplace=True)
    return daily_pm25_df

def create_monthly_pm25_df(df):
    monthly_pm25_df = df.groupby(df['datetime'].dt.month)['PM2.5'].mean().reset_index()
    monthly_pm25_df.rename(columns={'PM2.5': 'average_pm25', 'datetime': 'month'}, inplace=True)
    return monthly_pm25_df

def create_wind_pm25_correlation(df):
    correlation = df[['WSPM', 'PM2.5']].corr().iloc[0, 1]
    return correlation

# Load cleaned data
air_quality_df = pd.read_csv("main_data.csv")
air_quality_df['datetime'] = pd.to_datetime(air_quality_df['datetime'])

# Filter data for the years 2013 to 2017
air_quality_df = air_quality_df[(air_quality_df['datetime'] >= '2013-01-01') & 
                                 (air_quality_df['datetime'] <= '2017-12-31')]

# Sidebar for logo and date selection
with st.sidebar:
    st.image("logo.png")  # Ganti dengan path logo Anda
    
    # Mengambil start_date & end_date dari date_input
    start_date = st.date_input(
        label='Tanggal Mulai',
        value=pd.to_datetime('2013-01-01')
    )
    end_date = st.date_input(
        label='Tanggal Selesai',
        value=pd.to_datetime('2017-12-31')
    )

# Filter main data based on selected dates
main_df = air_quality_df[(air_quality_df['datetime'] >= str(start_date)) & 
                          (air_quality_df['datetime'] <= str(end_date))]

# Prepare dataframes
daily_pm25_df = create_daily_pm25_df(main_df)
monthly_pm25_df = create_monthly_pm25_df(main_df)
wind_pm25_correlation = create_wind_pm25_correlation(main_df)

# Dashboard Title
st.header('Dashboard Kualitas Udara di Distrik Aotizhongxin Beijing :sparkles:')

# Daily PM2.5 Orders
st.subheader('Rata-rata PM2.5 Harian')

col1, col2 = st.columns(2)

with col1:
    total_days = daily_pm25_df.shape[0]
    st.metric("Total Hari", value=total_days)

with col2:
    avg_pm25 = round(daily_pm25_df['average_pm25'].mean(), 2)
    st.metric("Rata-rata PM2.5", value=avg_pm25)

# Visualisasi Tren PM2.5
st.subheader("Tren Rata-rata PM2.5 (2013 - 2017)")
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_pm25_df["datetime"],
    daily_pm25_df["average_pm25"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.set_title("Tren Rata-rata PM2.5 di distrik Aotizhongxin Beijing", fontsize=20)
ax.set_ylabel("PM2.5 (µg/m³)", fontsize=15)
ax.set_xlabel("Tanggal", fontsize=15)
ax.tick_params(axis='y', labelsize=12)
ax.tick_params(axis='x', labelsize=12)
ax.grid(True)

st.pyplot(fig)

# Menentukan periode dengan tingkat polusi tertinggi
highest_pm25_date = daily_pm25_df.loc[daily_pm25_df['average_pm25'].idxmax(), 'datetime']
highest_pm25_value = daily_pm25_df['average_pm25'].max()
st.write(f"Tingkat polusi PM2.5 tertinggi terjadi pada {highest_pm25_date.date()} dengan nilai {highest_pm25_value} µg/m³.")

# Monthly PM2.5 Performance
st.subheader("Rata-rata PM2.5 Bulanan (2013 - 2017)")

fig, ax = plt.subplots(figsize=(20, 10))
sns.barplot(
    x="month", 
    y="average_pm25", 
    data=monthly_pm25_df,
    palette="coolwarm",
    ax=ax
)
ax.set_title("Rata-rata PM2.5 per Bulan di distrik Aotizhongxin Beijing", fontsize=20)
ax.set_ylabel("Rata-rata PM2.5 (µg/m³)", fontsize=15)
ax.set_xlabel("Bulan", fontsize=15)
ax.tick_params(axis='y', labelsize=12)
ax.tick_params(axis='x', labelsize=12)

st.pyplot(fig)

# Hubungan antara Kecepatan Angin dan PM2.5
st.subheader("Hubungan antara Kecepatan Angin dan PM2.5")

# Visualisasi hubungan kecepatan angin dan PM2.5
plt.figure(figsize=(10, 6))
sns.scatterplot(x=main_df["WSPM"], y=main_df["PM2.5"], alpha=0.3, color="blue")
plt.title("Hubungan Kecepatan Angin dan PM2.5 di distrik Aotizhongxin Beijing", fontsize=20)
plt.xlabel("Kecepatan Angin (m/s)", fontsize=15)
plt.ylabel("PM2.5 (µg/m³)", fontsize=15)
plt.grid(True)
st.pyplot(plt)

# Korelasi antara Kecepatan Angin dan PM2.5
st.subheader("Korelasi antara Kecepatan Angin dan PM2.5")
st.write(f"Korelasi antara kecepatan angin dan PM2.5 adalah: {round(wind_pm25_correlation, 2)}")

st.caption('Copyright © Hoel.id 2025')