import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_gsheets import GSheetsConnection

# 1. Konfigurasi Halaman
st.set_page_config(page_title="Monitoring LU | Dashboard", page_icon="📈", layout="wide")

# 2. CSS Kustom untuk Estetika Minimalis & Modern
st.markdown("""
    <style>
    /* Global Styles */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    
    .stApp { background-color: #FAFAFA; }
    
    /* Header Styling */
    .main-header {
        background: linear-gradient(90deg, #E53935 0%, #B71C1C 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(229, 57, 53, 0.2);
    }
    
    /* Card Styling */
    .stat-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #E53935;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        text-align: center;
    }
    
    /* Button Styling */
    .stButton>button {
        background-color: #E53935;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.6rem 2rem;
        font-weight: 600;
        transition: 0.3s;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #B71C1C;
        box-shadow: 0 4px 12px rgba(229, 57, 53, 0.3);
    }
    
    /* Custom Tabs */
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

# 3. Koneksi Google Sheets
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

# Header UI
st.markdown("""
    <div class="main-header">
        <h1 style="margin:0; color:white;">Project Monitoring Dashboard</h1>
        <p style="margin:0; opacity:0.9;">Real-time Tracking & Data Analytics Platform</p>
    </div>
""", unsafe_allow_html=True)

data_sheets = load_all_data()

# Initialize Session State
if 'edited_data' not in st.session_state:
    st.session_state.edited_data = {s: df.copy() for s, df in data_sheets.items()}

# --- LOGIC PERHITUNGAN PROGRESS ---
all_status = []
for sheet, df in st.session_state.edited_data.items():
    if 'Status' in df.columns:
        all_status.extend(df['Status'].fillna('Pending').tolist())

total_task = len(all_status)
selesai_count = len([x for x in all_status if 'Selesai' in str(x)])
persen_total = (selesai_count / total_task * 100) if total_task > 0 else 0

# --- TAMPILAN DASHBOARD ---
tab_dash, tab_edit, tab_sync = st.tabs(["📊 Analytics Dashboard", "📝 Interactive Editor", "🔄 Sync Status"])

with tab_dash:
    # Row 1: Key Metrics
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f'<div class="stat-card"><p style="color:#757575;margin:0;">Total Task</p><h2 style="margin:0;">{total_task}</h2></div>', unsafe_allow_html=True)
    with m2:
        st.markdown(f'<div class="stat-card"><p style="color:#757575;margin:0;">Selesai</p><h2 style="margin:0;color:#2E7D32;">{selesai_count}</h2></div>', unsafe_allow_html=True)
    with m3:
        st.markdown(f'<div class="stat-card"><p style="color:#757575;margin:0;">Completion Rate</p><h2 style="margin:0;color:#E53935;">{persen_total:.1f}%</h2></div>', unsafe_allow_html=True)
    with m4:
        st.markdown(f'<div class="stat-card"><p style="color:#757575;margin:0;">Kategori</p><h2 style="margin:0;">{len(SHEET_NAMES)}</h2></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Row 2: Charts
    c1, c2 = st.columns([1, 1])
    
    with c1:
        st.subheader("Overall Status Distribution")
        if all_status: # Cek jika list status tidak kosong
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
            # Pastikan kolom "Status" benar-benar ada (Case-sensitive)
            if 'Status' in df.columns:
                done = len(df[df['Status'].astype(str).str.contains('Selesai', na=False, case=False)])
                total = len(df)
                cat_data.append({"Category": s, "Done": done, "Total": total})
        
        df_cat = pd.DataFrame(cat_data)
        
        # Cek apakah dataframe berhasil terbentuk sebelum membuat grafik
        if not df_cat.empty:
            fig_bar = px.bar(df_cat, x="Category", y=["Done", "Total"], barmode="group",
                             color_discrete_map={"Done": "#E53935", "Total": "#E0E0E0"})
            fig_bar.update_layout(height=300, margin=dict(t=0, b=0))
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("⚠️ Data kategori belum tersedia untuk ditampilkan.")

with tab_edit:
    st.subheader("Detail Data & Live Editor")
    sub_tabs = st.tabs(SHEET_NAMES)
    
    for i, sheet in enumerate(SHEET_NAMES):
        with sub_tabs[i]:
            df_to_edit = st.session_state.edited_data[sheet]
            
            # Tambahkan visualisasi mini per sheet
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
    if st.button("🚀 Push Changes to Cloud (Google Sheets)"):
        with st.spinner("Synchronizing data..."):
            try:
                for s in SHEET_NAMES:
                    conn.update(worksheet=s, data=st.session_state.edited_data[s])
                st.success("Sync Berhasil! Database telah diperbarui.")
                st.balloons()
                st.cache_data.clear()
            except Exception as e:
                st.error(f"Sync Gagal: {e}")

# Sidebar info
st.sidebar.image("https://img.icons8.com/fluency/96/000000/dashboard.png", width=80)
st.sidebar.title("App Settings")
st.sidebar.info("Gunakan Dashboard untuk melihat insight cepat dan Editor untuk mengubah data harian.")
if st.sidebar.button("Clear Cache"):
    st.cache_data.clear()
    st.rerun()
