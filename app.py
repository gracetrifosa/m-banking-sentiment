# ============================
# MOBILE BANKING SENTIMENT APP
# ============================

import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

st.set_page_config(page_title="Mobile Banking Sentiment", layout="wide")

# ============================
# CUSTOM CSS – Sidebar ala Splash (Navy Version)
# ============================

st.markdown("""
<style>

/* ==== SIDEBAR CONTAINER ==== */
[data-testid="stSidebar"] {
    background-color: #1E3A8A !important;
    padding: 40px 30px !important;
}

/* ==== SIDEBAR TITLE ==== */
.sidebar-title {
    font-size: 34px;
    font-weight: 900;
    color: white;
    margin-bottom: 35px;
}

/* === TEKS MENU RADIO DI SIDEBAR JADI PUTIH === */
[data-testid="stSidebar"] div[role="radiogroup"] * {
    color: white !important;
    fill: white !important;
}


div[role="radiogroup"] > label span {
    color: white !important;
}

/* Hilangkan warna hitam default yg nempel */
[data-testid="stSidebar"] label {
    color: white !important;
}



/* ==== RADIO BULLET ==== */
[data-testid="stSidebar"] input[type="radio"] {
    transform: scale(1.3);
    accent-color: #FACC15 !important; /* gold */
}

/* ==== SPACING ANTAR MENU ==== */
div[role="radiogroup"] > label {
    margin-bottom: 18px !important;
}

/* ==== GARIS PEMBATAS ==== */
.sidebar-line {
    height: 1px;
    background-color: rgba(255,255,255,0.3);
    margin: 30px 0;
}

.main {background-color: #F8FAFC;}

.title {
    color: white;
    padding: 20px;
    background-color:#1E3A8A;
    text-align:center;
    border-radius:10px;
    margin-bottom: 20px;
}

.card {
    background-color: white;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    margin-bottom: 20px;
}

</style>
""", unsafe_allow_html=True)

# ============================
# LOAD DATA
# ============================

@st.cache_data
def load_data():
    df = pd.read_csv("data.csv")

    df = df.rename(columns={
        "app_name": "platform",
        "review": "review",
        "label": "sentiment",
        "at": "date",
        "score": "score",
        "stemming": "stemming"
    })

    df["platform"] = df["platform"].replace({
        "BCA Mobile": "BCA Mobile",
        "BRImo": "BRImo",
        "brimo": "BRImo",
        "BRIMO": "BRImo"
    })

    df["sentiment"] = df["sentiment"].replace({
        "positif": "positive",
        "negatif": "negative",
        "Positif": "positive",
        "Negatif": "negative",
        "POSITIVE": "positive",
        "NEGATIVE": "negative"
    })

    df = df[df["sentiment"].isin(["positive", "negative"])]

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    return df

df = load_data()

# ============================
# SIDEBAR MENU
# ============================

st.sidebar.markdown("<div class='sidebar-title'>Menu</div>", unsafe_allow_html=True)

menu = st.sidebar.radio(
    "",
    ["Home", "Dashboard", "Data", "About"]
)

st.sidebar.markdown("<div class='sidebar-line'></div>", unsafe_allow_html=True)


# ============================
# HOME PAGE
# ============================

if menu == "Home":
    st.markdown("<h1 class='title'>Analisis Sentimen BCA Mobile & BRImo</h1>", unsafe_allow_html=True)

    st.markdown("""
    <div class='card'>
        <h3>📱 Deskripsi Aplikasi</h3>
        Website ini menyajikan hasil analisis sentimen pengguna terhadap aplikasi 
        <b>BCA Mobile</b> dan <b>BRImo</b>. Visualisasi mencakup distribusi sentimen, 
        perbandingan performa aplikasi, dan insight penting lainnya.
    </div>
    """, unsafe_allow_html=True)

    total = len(df)
    bca = len(df[df.platform == "BCA Mobile"])
    bri = len(df[df.platform == "BRImo"])

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Review", total)
    c2.metric("BCA Mobile", bca)
    c3.metric("BRImo", bri)

    st.subheader("Perbandingan Sentimen BCA Mobile vs BRImo")

    pie = px.pie(
        df,
        names="platform",
        title="Perbandingan Sentimen",
        color="platform",
        color_discrete_map={"BCA Mobile": "#1E3A8A", "BRImo": "#3B82F6"}
    )

    pie.update_layout(
        title_font=dict(size=20),
        legend=dict(x=0.8, y=0.5),
        title_x=0.1
    )

    st.plotly_chart(pie, use_container_width=True)

    st.markdown("""
    <div class='card'>
        <h3>🎯 Tujuan Penelitian</h3>
        <ul>
            <li>Menganalisis persepsi pengguna mobile banking</li>
            <li>Membandingkan sentimen BCA Mobile & BRImo</li>
            <li>Menyediakan insight berbasis data</li>
            <li>Dashboard interaktif untuk laporan</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)



# ============================
# DASHBOARD PAGE
# ============================

elif menu == "Dashboard":
    st.markdown("<h1 class='title'>Sentiment Dashboard</h1>", unsafe_allow_html=True)

    col1, col2 = st.columns([1,1])
    pilih_app = col1.selectbox("Pilih Aplikasi", ["All", "BCA Mobile", "BRImo"])
    pilih_sentimen = col2.selectbox("Pilih Sentimen", ["All", "positive", "negative"])

    data_dash = df.copy()
    if pilih_app != "All":
        data_dash = data_dash[data_dash.platform == pilih_app]
    if pilih_sentimen != "All":
        data_dash = data_dash[data_dash.sentiment == pilih_sentimen]

    st.markdown("### 📊 Sentiment Summary")
    c1, c2 = st.columns(2)
    c1.metric("Positive", len(data_dash[data_dash.sentiment == "positive"]))
    c2.metric("Negative", len(data_dash[data_dash.sentiment == "negative"]))

    st.markdown("### 🥧 Sentiment Distribution")
    if len(data_dash) > 0:
        pie = px.pie(
            data_dash,
            names="sentiment",
            color="sentiment",
            color_discrete_map={"positive": "#1E3A8A", "negative": "#3B82F6"}
        )

        pie.update_layout(
        legend=dict(
            x=0.75,   # geser kiri/kanan
            y=0.5,    # geser atas/bawah
            font=dict(size=14),
        )
    )

        st.plotly_chart(pie, use_container_width=True)
    else:
        st.info("Tidak ada data untuk ditampilkan.")
        

    st.markdown("### ✏ Comment Length Distribution")
    if len(data_dash) > 0:
        data_dash["length"] = data_dash["review"].astype(str).apply(len)
        fig = px.histogram(
            data_dash,
            x="length",
            nbins=50,
            color="sentiment",
            color_discrete_map={"positive": "#1E3A8A", "negative": "#3B82F6"}
        )

        fig.update_layout(
        legend=dict(
            x=0.92,   # kiri–kanan
            y=0.95,   # atas–bawah
            font=dict(size=14),
        )
    )

        st.plotly_chart(fig, use_container_width=True)


# ============================
# DATA PAGE
# ============================

elif menu == "Data":
    st.markdown("<h1 class='title'>Sentiment Data</h1>", unsafe_allow_html=True)
    st.markdown("### 📄 View Data")

    table = df[["platform", "review", "sentiment", "stemming"]]
    table = table.rename(columns={
        "platform": "Aplikasi",
        "review": "Review",
        "sentiment": "Sentimen",
        "stemming": "Cleaned Text"
    })

    st.dataframe(table, use_container_width=True, height=600)



# ============================
# ABOUT PAGE
# ============================

elif menu == "About":
    st.markdown("<h1 class='title'>Tentang Aplikasi</h1>", unsafe_allow_html=True)

    st.markdown("""
    <div class='card' style='font-size:16px; line-height:1.7;'>
       <h3>📘 Deskripsi Aplikasi</h3>
<p>
Aplikasi ini dirancang untuk menganalisis sentimen publik terhadap layanan mobile banking 
<b>BCA Mobile</b> dan <b>BRImo</b>, berdasarkan ulasan pengguna dan ditampilkan dalam bentuk visualisasi grafik yang mudah dipahami.
</p>

<h3>✨ Fitur Utama</h3>
<ul>
    <li>Analisis komentar positif & negatif</li>
    <li>Perbandingan sentimen antar aplikasi</li>
    <li>Visualisasi grafik interaktif</li>
    <li>Tampilan data komentar yang telah diproses</li>
</ul>

<h3>👩‍💻 Pengembang</h3>
<p>
Aplikasi ini dikembangkan oleh <b>Grace Trifosa Sagala</b> (NIM 825220125) sebagai bagian dari 
Tugas Akhir di <b>Universitas Tarumanagara</b>. Tujuannya adalah memberikan pemahaman yang lebih 
mendalam mengenai opini pengguna terhadap layanan mobile banking melalui analisis sentimen 
yang terstruktur dan mudah dipahami.
</p>

<h3>📩 Kontak</h3>
<p>
Jika Anda memiliki pertanyaan, saran, atau masukan, silakan hubungi melalui email: 📧 grace.825220125@stu.untar.ac.id</b>
</p>

    """, unsafe_allow_html=True)
