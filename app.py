import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_gsheets import GSheetsConnection

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Monitoring LU | Dashboard", page_icon="📈", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .stApp { background-color: #FAFAFA; }
    
    .main-header {
        background: linear-gradient(90deg, #E53935 0%, #B71C1C 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(229, 57, 53, 0.2);
    }
    .stat-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #E53935;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        text-align: center;
    }
    .stButton>button {
        background-color: #E53935;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.6rem 2rem;
        font-weight: 600;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #B71C1C;
        box-shadow: 0 4px 12px rgba(229, 57, 53, 0.3);
    }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        background-color: white;
        border: 1px solid #E0E0E0;
        border-radius: 8px 8px 0 0;
        padding: 10px 20px;
        color: #616161;
    }
    .stTabs [aria-selected="true"] {
        background-color: #E53935 !important;
        color: white !important;
        border-color: #E53935 !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- KONEKSI DATA ---
conn = st.connection("gsheets", type=GSheetsConnection)
SHEET_NAMES = ["Video", "Artikel", "Infographics", "Audio", "Quiz"]

@st.cache_data(ttl=10)
def load_all_data():
    all_dfs = {}
    for sheet in SHEET_NAMES:
        try:
            df = conn.read(worksheet=sheet)
            all_dfs[sheet] = df.dropna(how='all')
        except:
            all_dfs[sheet] = pd.DataFrame()
    return all_dfs

st.markdown("""
    <div class="main-header">
        <h1 style="margin:0; color:white;">Project Monitoring Dashboard</h1>
        <p style="margin:0; opacity:0.9;">Real-time Tracking & Data Analytics Platform</p>
    </div>
""", unsafe_allow_html=True)

data_sheets = load_all_data()

if 'edited_data' not in st.session_state:
    st.session_state.edited_data = {s: df.copy() for s, df in data_sheets.items()}

# KALKULASI METRIK UTAMA (Update: Selesai + Under Review)
all_status = []
for sheet, df in st.session_state.edited_data.items():
    if 'Status' in df.columns:
        all_status.extend(df['Status'].fillna('Pending').tolist())

total_task = len(all_status)
# Update logika: hitung jika mengandung kata 'Selesai' ATAU 'Under Review'
selesai_count = len([x for x in all_status if 'selesai' in str(x).lower() or 'under review' in str(x).lower()])
persen_total = (selesai_count / total_task * 100) if total_task > 0 else 0

# --- TAB KONTEN UTAMA ---
tab_dash, tab_edit, tab_sync = st.tabs(["📊 Analytics Dashboard", "📝 Interactive Editor", "🔄 Sync Status"])

with tab_dash:
    # 1. Row Metrik
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f'<div class="stat-card"><p style="color:#757575;margin:0;">Total Task</p><h2 style="margin:0;">{total_task}</h2></div>', unsafe_allow_html=True)
    with m2:
        st.markdown(f'<div class="stat-card"><p style="color:#757575;margin:0;">Selesai / Review</p><h2 style="margin:0;color:#2E7D32;">{selesai_count}</h2></div>', unsafe_allow_html=True)
    with m3:
        st.markdown(f'<div class="stat-card"><p style="color:#757575;margin:0;">Completion Rate</p><h2 style="margin:0;color:#E53935;">{persen_total:.1f}%</h2></div>', unsafe_allow_html=True)
    with m4:
        st.markdown(f'<div class="stat-card"><p style="color:#757575;margin:0;">Kategori</p><h2 style="margin:0;">{len(SHEET_NAMES)}</h2></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 2. Row Pie & Bar Chart
    c1, c2 = st.columns([1, 1])
    
    with c1:
        st.subheader("Overall Status Distribution")
        if all_status: 
            fig_pie = px.pie(
                values=[all_status.count(s) for s in set(all_status)], 
                names=list(set(all_status)),
                hole=0.5,
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig_pie.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=300)
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("⚠️ Kolom 'Status' tidak ditemukan atau data kosong.")

    with c2:
        st.subheader("Progress per Category")
        cat_data = []
        for s, df in st.session_state.edited_data.items():
            if 'Status' in df.columns:
                # Update logika: mencari 'Selesai' ATAU 'Under Review'
                done = len(df[df['Status'].astype(str).str.contains('Selesai|Under Review', na=False, case=False, regex=True)])
                total = len(df)
                cat_data.append({"Category": s, "Done": done, "Total": total})
        
        df_cat = pd.DataFrame(cat_data)
        if not df_cat.empty:
            fig_bar = px.bar(df_cat, x="Category", y=["Done", "Total"], barmode="group",
                             color_discrete_map={"Done": "#E53935", "Total": "#E0E0E0"})
            fig_bar.update_layout(height=300, margin=dict(t=0, b=0))
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("⚠️ Data kategori belum tersedia untuk ditampilkan.")

    st.markdown("<hr>", unsafe_allow_html=True)
    
    # 3. Row Trend Harian 
    st.subheader("📈 Chart Penyelesaian Harian")
    
    daily_data = []
    # Mengumpulkan data tanggal dari semua sheet
    for s, df in st.session_state.edited_data.items():
        # Coba mencari kolom yang mengandung kata "Tanggal" (misal: Tanggal Selesai)
        date_col = next((col for col in df.columns if 'tanggal' in str(col).lower()), None)
        
        if 'Status' in df.columns and date_col:
            # Update logika: Saring task yang statusnya Selesai ATAU Under Review
            df_selesai = df[df['Status'].astype(str).str.contains('Selesai|Under Review', na=False, case=False, regex=True)]
            # Masukkan semua tanggal valid ke dalam list
            for val in df_selesai[date_col].dropna():
                daily_data.append({'Tanggal': val})
                
    if daily_data:
        df_daily = pd.DataFrame(daily_data)
        # Normalisasi format tanggal agar seragam
        df_daily['Tanggal'] = pd.to_datetime(df_daily['Tanggal'], errors='coerce').dt.date
        df_daily = df_daily.dropna() # Buang data yang bukan format tanggal
        
        if not df_daily.empty:
            # Hitung jumlah penyelesaian per hari
            df_trend = df_daily.groupby('Tanggal').size().reset_index(name='Jumlah Task')
            df_trend = df_trend.sort_values('Tanggal')
            
            # Buat grafik garis
            fig_trend = px.line(df_trend, x='Tanggal', y='Jumlah Task', markers=True,
                                color_discrete_sequence=["#E53935"])
            fig_trend.update_traces(line=dict(width=3), marker=dict(size=8))
            fig_trend.update_layout(height=300, margin=dict(t=10, b=0, l=0, r=0),
                                    xaxis_title="", yaxis_title="Task Selesai / Review")
            st.plotly_chart(fig_trend, use_container_width=True)
        else:
            st.info("⚠️ Belum ada format tanggal valid pada task yang selesai/review.")
    else:
        st.info("⚠️ Kolom yang memuat 'Tanggal' tidak ditemukan, atau belum ada task yang selesai/review.")

with tab_edit:
    st.subheader("Detail Data & Live Editor")
    sub_tabs = st.tabs(SHEET_NAMES)
    
    for i, sheet in enumerate(SHEET_NAMES):
        with sub_tabs[i]:
            df_to_edit = st.session_state.edited_data[sheet]
            
            if not df_to_edit.empty and 'Status' in df_to_edit.columns:
                col_t1, col_t2 = st.columns([2, 1])
                with col_t2:
                    status_counts = df_to_edit['Status'].value_counts().reset_index()
                    fig_mini = px.bar(status_counts, x='Status', y='count', color='Status', 
                                     title=f"Trend {sheet}", height=200)
                    fig_mini.update_layout(showlegend=False, margin=dict(t=30, b=0, l=0, r=0))
                    st.plotly_chart(fig_mini, use_container_width=True)
                
                with col_t1:
                    st.info(f"Mengedit {len(df_to_edit)} baris data di kategori {sheet}.")
            
            # Data Editor 
            edited_df = st.data_editor(
                df_to_edit,
                width="stretch", 
                num_rows="dynamic",
                hide_index=True,
                key=f"editor_v2_{sheet}"
            )
            st.session_state.edited_data[sheet] = edited_df

with tab_sync:
    st.markdown("""
        <div style="text-align:center; padding: 3rem; background:white; border-radius:15px; border: 1px dashed #E53935;">
            <h3 style="color:#E53935;">Finalisasi Data</h3>
            <p>Pastikan semua input sudah benar sebelum menekan tombol di bawah. <br>Data akan langsung diperbarui di Google Sheets pusat.</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚀 Push Changes to Cloud (Google Sheets)", width="stretch"):
        with st.spinner("Synchronizing data..."):
            try:
                for s in SHEET_NAMES:
                    conn.update(worksheet=s, data=st.session_state.edited_data[s])
                st.success("Sync Berhasil! Database telah diperbarui.")
                st.balloons()
                st.cache_data.clear()
            except Exception as e:
                st.error(f"Sync Gagal: {e}")

# --- SIDEBAR & SETTINGS ---
st.sidebar.image("https://img.icons8.com/fluency/96/000000/dashboard.png", width=80)
st.sidebar.title("App Settings")
st.sidebar.info("Gunakan Dashboard untuk melihat insight cepat dan Editor untuk mengubah data harian.")

if st.sidebar.button("Clear Cache", width="stretch"):
    st.cache_data.clear()
    st.rerun()

