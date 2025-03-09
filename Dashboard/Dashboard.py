import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# Title & Subtitle
st.title("📊 Dashboard Analisis Penyewaan Sepeda 🚲")
st.caption("Dataset Source: https://www.kaggle.com/datasets/lakshmi25npathi/bike-sharing-dataset")
st.write("###### Author: Fitri Fatma Dewi (MC004D5X1425)")
st.caption("Email: fitriworkspace12@gmail.com | Linkedln:https://www.linkedin.com/in/fitri-fatma-dewi")

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("Dashboard/hour_cleaned_data.csv")
    df["date"] = pd.to_datetime(df["date"])  # Konversi date ke datetime
    return df

df = load_data()

# Tab Navigasi
tabs = st.tabs(["📌 Cuaca & Penyewaan", "⏳ Kapan Waktu Terbaik?", "🔍 Insight Tambahan"])

# ---- Tab 1: Cuaca & Penyewaan ----
with tabs[0]:
    st.subheader("Total Penyewaan Sepeda Berdasarkan Kondisi Cuaca")
    date_range = st.date_input("📅 Pilih Rentang Waktu", [df["date"].min(), df["date"].max()])
    filtered_df = df[(df["date"] >= pd.to_datetime(date_range[0])) & (df["date"] <= pd.to_datetime(date_range[1]))]
    
    if not filtered_df.empty:
        # Bar Chart
        # Hitung total penyewaan per kondisi cuaca
        weather_count = filtered_df.groupby("weathersit")["count"].sum().reset_index()

        # Highlight bar tertinggi
        max_value = weather_count["count"].max()
        weather_count["color"] = weather_count["count"].apply(lambda x: "#8B4513" if x == max_value else "#D2B48C")

        # Buat Bar Chart
        fig = px.bar(weather_count, x="count", y="weathersit", orientation='h',
                    title="Total Penyewaan Sepeda Berdasarkan Kondisi Cuaca",
                    color="color", color_discrete_map="identity",
                    labels={"weathersit": "Kondisi Cuaca", "count": "Total Penyewaan"}
                    )

        # Tambahkan chart ke Streamlit
        st.plotly_chart(fig)

        
        # Pie Chart
        st.subheader("Proporsi Penyewaan Sepeda Berdasarkan Kondisi Cuaca")
        weather_rental = filtered_df.groupby("weathersit")["count"].sum().reset_index()
        fig_pie = px.pie(weather_rental, names="weathersit", values="count",
                         title="Proporsi Penyewaan Sepeda Berdasarkan Cuaca",
                         color_discrete_sequence=["#8B4513", "#A0522D", "#CD853F", "#D2B48C"])
        st.plotly_chart(fig_pie)
        
        # Tambahkan legenda sebagai keterangan di bawah chart
        st.markdown("""
        **Keterangan Kondisi Cuaca:**
        - **1**: Clear, Few clouds, Partly cloudy
        - **2**: Mist + Cloudy, Mist + Broken clouds, Mist + Few clouds, Mist
        - **3**: Light Snow, Light Rain + Thunderstorm + Scattered clouds, Light Rain + Scattered clouds
        - **4**: Heavy Rain + Ice Pallets + Thunderstorm + Mist, Snow + Fog
        """)
        
    else:
        st.warning("Tidak ada data yang tersedia untuk visualisasi.")
        

# ---- Tab 2: Kapan Waktu Terbaik? ----
with tabs[1]:
    st.subheader("Tren Penyewaan Sepeda per Jam")

    # Pilih Hari dalam Bahasa Indonesia
    selected_days = st.multiselect("📅 Pilih Hari", df["weekday"].unique(), df["weekday"].unique())
    filtered_df = df[df["weekday"].isin(selected_days)]

    if not filtered_df.empty:
        # Hitung jumlah penyewaan per jam
        hourly_rentals = filtered_df.groupby("hour")["count"].sum().reset_index()

        # Buat Line Chart dengan label bahasa Indonesia
        fig = px.line(hourly_rentals, x="hour", y="count", markers=True,
                      title="Tren Penyewaan Sepeda per Jam",
                      color_discrete_sequence=["#8B4513"],
                      labels={"hour": "Jam", "count": "Jumlah Penyewaan"}
                     )
        st.plotly_chart(fig)
    
        # Heatmap Penyewaan
        st.subheader("Heatmap Penyewaan Sepeda Berdasarkan Waktu")

        # Urutan hari dari Minggu (0) hingga Sabtu (6)
        weekday_order = [0, 1, 2, 3, 4, 5, 6]
        weekday_labels = {0: "Minggu", 1: "Senin", 2: "Selasa", 3: "Rabu", 
                          4: "Kamis", 5: "Jumat", 6: "Sabtu"}

        # Buat pivot table dengan urutan weekday yang benar
        pivot_table = filtered_df.pivot_table(values="count", index="weekday", columns="hour", aggfunc="sum", fill_value=0)
        pivot_table = pivot_table.reindex(weekday_order)  # Pastikan urutan sesuai

        # Plot heatmap
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(pivot_table, cmap="copper", annot=False, fmt=".0f", linewidths=0.5, ax=ax)

        # Ganti label sumbu Y dengan nama hari dalam bahasa Indonesia
        ax.set_yticks(range(len(weekday_order)))
        ax.set_yticklabels([weekday_labels[i] for i in weekday_order], rotation=0)

        ax.set_xlabel("Jam")
        ax.set_ylabel("Hari")
        st.pyplot(fig)
    else:
        st.warning("Tidak ada data yang tersedia untuk visualisasi.")


# ---- Tab 3: Insight Tambahan ----
with tabs[2]:
        st.subheader("Distribusi Penyewaan Sepeda Berdasarkan Kategori Penggunaan")
        selected_category = st.multiselect("📊 Pilih Kategori Penggunaan", df["Usage_Category"].unique(), df["Usage_Category"].unique())
        filtered_df = df[df["Usage_Category"].isin(selected_category)]

        if not filtered_df.empty:
            # Hitung jumlah penyewaan per kategori
            category_count = filtered_df["Usage_Category"].value_counts().reset_index()
            category_count.columns = ["Kategori Penggunaan", "Jumlah Penyewaan"]
            
            # Warna untuk highlight
            max_value = category_count["Jumlah Penyewaan"].max()
            category_count["color"] = category_count["Jumlah Penyewaan"].apply(lambda x: "#8B4513" if x == max_value else "#D2B48C")

            # Buat Bar Chart dengan label bahasa Indonesia
            fig = px.bar(category_count, x="Kategori Penggunaan", y="Jumlah Penyewaan",
                        title="Distribusi Penyewaan Sepeda Berdasarkan Kategori Penggunaan",
                        color="color", color_discrete_map="identity",
                        labels={"Kategori Penggunaan": "Kategori Penggunaan", "Jumlah Penyewaan": "Jumlah Penyewaan"}
                        )
            
            st.plotly_chart(fig)
        else:
            st.warning("Tidak ada data yang tersedia untuk visualisasi.")

