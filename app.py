import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from mplsoccer import Pitch
import plotly.express as px
import plotly.graph_objects as go
import os

# ==============================================================================
# PAGE CONFIGURATION & THEME
# ==============================================================================
st.set_page_config(
    page_title="Beşiktaş JK - Match Performance Analytics",
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Dark Mode Beşiktaş Styling (CSS)
st.markdown("""
<style>
    /* Main Background */
    .stApp {
        background-color: #0c0f14;
        color: #ffffff;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Header Banner */
    .bjk-header {
        background: linear-gradient(135deg, #11141a 0%, #1c202a 60%, #e30613 100%);
        padding: 22px 28px;
        border-radius: 12px;
        border-left: 6px solid #e30613;
        margin-bottom: 22px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    }
    .bjk-title {
        font-size: 2.1rem;
        font-weight: 800;
        color: #ffffff;
        margin: 0;
        letter-spacing: 0.5px;
    }
    .bjk-subtitle {
        font-size: 1.05rem;
        color: #d1d5db;
        margin-top: 5px;
        font-weight: 400;
    }
    
    /* Metric Cards */
    div[data-testid="stMetric"] {
        background: linear-gradient(145deg, #161922, #101218);
        border: 1px solid #272c3a;
        border-radius: 10px;
        padding: 14px 18px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.35);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        border-color: #e30613;
    }
    div[data-testid="stMetricLabel"] > div {
        color: #9ca3af !important;
        font-size: 0.9rem !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    div[data-testid="stMetricValue"] > div {
        color: #ffffff !important;
        font-size: 1.85rem !important;
        font-weight: 800 !important;
    }
    
    /* Sidebar Buttons */
    section[data-testid="stSidebar"] {
        background-color: #11141c;
        border-right: 1px solid #1f2430;
    }
    section[data-testid="stSidebar"] .stButton button {
        background-color: #171b24;
        color: #e5e7eb;
        border: 1px solid #252c3c;
        border-radius: 8px;
        padding: 8px 14px;
        font-weight: 600;
        text-align: left;
        transition: all 0.2s ease;
    }
    section[data-testid="stSidebar"] .stButton button:hover {
        background-color: #e30613 !important;
        color: #ffffff !important;
        border-color: #e30613 !important;
        transform: translateX(4px);
    }
</style>
""", unsafe_allow_html=True)


# ==============================================================================
# 1. SESSION STATE MANAGEMENT
# ==============================================================================
# Initialize selected player (Default: None -> Team View)
if "secilen_oyuncu" not in st.session_state:
    st.session_state.secilen_oyuncu = None


# ==============================================================================
# DATA LOADING
# ==============================================================================
@st.cache_data
def load_match_data():
    file_path = "besiktas_mac_verisi.csv"
    if not os.path.exists(file_path):
        st.error(f"File '{file_path}' not found! Please ensure data files are generated.")
        return pd.DataFrame()
    return pd.read_csv(file_path)

df_all = load_match_data()

if df_all.empty:
    st.stop()

# Beşiktaş Squad Definition (Starting XI & Substitutes)
STARTING_XI = [
    {"name": "Alexander Nübel", "pos": "GK", "no": 1},
    {"name": "Amir Murillo", "pos": "DF", "no": 62},
    {"name": "Tiago Djaló", "pos": "DF", "no": 3},
    {"name": "Emirhan Topçu", "pos": "DF", "no": 14},
    {"name": "Rıdvan Yılmaz", "pos": "DF", "no": 33},
    {"name": "Salih Özcan", "pos": "MF", "no": 6},
    {"name": "Junior Olaitan", "pos": "MF", "no": 10},
    {"name": "Orkun Kökçü", "pos": "MF", "no": 8},
    {"name": "Václav Černý", "pos": "MF", "no": 18},
    {"name": "Leandro Trossard", "pos": "FW", "no": 19},
    {"name": "Hyeon-gyu Oh", "pos": "FW", "no": 9}
]

SUBSTITUTES = [
    {"name": "İlhan Fakılı", "pos": "MF", "no": 29},
    {"name": "Amir Hadžiahmetović", "pos": "MF", "no": 88},
    {"name": "Dušan Vlahović", "pos": "FW", "no": 99},
    {"name": "Milot Rashica", "pos": "FW", "no": 7},
    {"name": "Kassoum Ouattara", "pos": "DF", "no": 24},
    {"name": "Doğan Alemdar", "pos": "GK", "no": 96},
    {"name": "Emmanuel Agbadou", "pos": "DF", "no": 5},
    {"name": "Taylan Bulut", "pos": "DF", "no": 2},
    {"name": "Yasin Özcan", "pos": "DF", "no": 27},
    {"name": "Wilfred Ndidi", "pos": "MF", "no": 25},
    {"name": "Semih Kılıçsoy", "pos": "FW", "no": 90}
]


# ==============================================================================
# 2. SIDEBAR (SQUAD NAVIGATION - STARTING XI & SUBS)
# ==============================================================================
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/2/20/Logo_of_Besiktas_JK.svg", width=80)
    st.markdown("## 🦅 **BEŞİKTAŞ JK**")
    st.caption("UEFA Europa League | 20 August 2026")
    
    # Return to Team Statistics Button
    if st.button("📊 🦅 **Team Overview & Stats**", use_container_width=True):
        st.session_state.secilen_oyuncu = None
        st.rerun()

    st.markdown("---")
    
    # Starting XI Buttons
    st.markdown("### ⚽ **Starting XI**")
    for player in STARTING_XI:
        p_name = player["name"]
        p_no = player["no"]
        p_pos = player["pos"]
        
        btn_label = f"#{p_no} {p_name} ({p_pos})"
        if st.session_state.secilen_oyuncu == p_name:
            btn_label = f"👉 🔴 {btn_label}"
            
        if st.button(btn_label, key=f"btn_xi_{p_name}", use_container_width=True):
            st.session_state.secilen_oyuncu = p_name
            st.rerun()

    st.markdown("---")
    
    # Substitutes Buttons
    st.markdown("### 🔄 **Substitutes**")
    for player in SUBSTITUTES:
        p_name = player["name"]
        p_no = player["no"]
        p_pos = player["pos"]
        
        btn_label = f"#{p_no} {p_name} ({p_pos})"
        if st.session_state.secilen_oyuncu == p_name:
            btn_label = f"👉 🔴 {btn_label}"
            
        if st.button(btn_label, key=f"btn_sub_{p_name}", use_container_width=True):
            st.session_state.secilen_oyuncu = p_name
            st.rerun()


# ==============================================================================
# 3. MAIN DASHBOARD AREA (DYNAMIC CONTENT)
# ==============================================================================

# ------------------------------------------------------------------------------
# CASE A: secilen_oyuncu is None (DEFAULT - OVERALL TEAM STATS & HEATMAP)
# ------------------------------------------------------------------------------
if st.session_state.secilen_oyuncu is None:
    st.markdown("""
    <div class="bjk-header">
        <h1 class="bjk-title">🦅 BEŞİKTAŞ JK - OVERALL MATCH PERFORMANCE</h1>
        <div class="bjk-subtitle">Beşiktaş JK <strong>3 - 0</strong> FK Kauno Žalgiris &nbsp;|&nbsp; <span>Tüpraş Stadium (Attendance: 31,494)</span></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Team KPI Metric Cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="⏱️ Possession", value="77%", delta="+54% Margin")
    with col2:
        st.metric(label="🎯 Total Shots", value="21", delta="6 On Target / 3 Goals")
    with col3:
        st.metric(label="⚽ Total Passes", value="620", delta="89% Accuracy")
    with col4:
        st.metric(label="🚩 Corners & Chances", value="15", delta="20+ Chances Created")
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Full Team Spatial Activity Heatmap (mplsoccer Pitch + KDE Plot)
    st.markdown("### 🏟️ Full Team Pitch Control & Spatial Pressure Heatmap")
    
    pitch = Pitch(
        pitch_type='statsbomb',
        pitch_color='#0c0f14',
        line_color='#e5e7eb',
        line_zorder=2,
        linewidth=1.5,
        goal_type='box'
    )
    
    fig, ax = pitch.draw(figsize=(12, 8))
    fig.patch.set_facecolor('#0c0f14')
    
    bjk_events = df_all[df_all["takim"] == "Beşiktaş JK"]
    x_all = bjk_events["x"].dropna()
    y_all = bjk_events["y"].dropna()
    
    if len(x_all) > 10:
        sns.kdeplot(
            x=x_all,
            y=y_all,
            ax=ax,
            fill=True,
            cmap='YlOrRd',
            levels=70,
            thresh=0.04,
            alpha=0.68,
            zorder=1
        )
        pitch.scatter(
            x_all, y_all,
            ax=ax,
            s=25,
            c='#ffffff',
            edgecolors='#e30613',
            alpha=0.45,
            zorder=3
        )
        
    ax.set_title(
        "Beşiktaş JK - 90-Minute Overall Spatial Activity & Territorial Dominance",
        fontsize=16,
        color='#ffffff',
        fontweight='bold',
        pad=15
    )
    
    p_col1, p_col2, p_col3 = st.columns([1, 10, 1])
    with p_col2:
        st.pyplot(fig, use_container_width=True)
    plt.close(fig)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Team Bottom Charts: Action Types Breakdown & Match Timeline
    g_col1, g_col2 = st.columns(2)
    with g_col1:
        st.markdown("#### 📊 Team Action Type Breakdown")
        team_action_counts = bjk_events["aksiyon_turu"].value_counts().reset_index()
        team_action_counts.columns = ["Action Type", "Count"]
        
        fig_team_bar = px.bar(
            team_action_counts,
            x="Action Type",
            y="Count",
            text="Count",
            color="Count",
            color_continuous_scale=["#2a2e39", "#555b6e", "#e30613", "#ff1e27"]
        )
        fig_team_bar.update_traces(
            textposition='outside',
            textfont_color='white',
            marker_line_color='#ffffff',
            marker_line_width=1
        )
        fig_team_bar.update_layout(
            plot_bgcolor="#141822",
            paper_bgcolor="#141822",
            font_color="#ffffff",
            xaxis=dict(showgrid=False, title=""),
            yaxis=dict(showgrid=True, gridcolor="#272c3a", title="Count"),
            coloraxis_showscale=False,
            margin=dict(l=20, r=20, t=30, b=20),
            height=340
        )
        st.plotly_chart(fig_team_bar, use_container_width=True)
        
    with g_col2:
        st.markdown("#### ⏱️ Match Key Events & Timeline")
        incidents_data = pd.DataFrame([
            {"Minute": "6'", "Event": "⚽ Goal: Hyeon-gyu Oh (Assist: Rıdvan Yılmaz)", "Score": "1-0"},
            {"Minute": "12'", "Event": "⚽ Goal: Amir Murillo (Assist: Rıdvan Yılmaz)", "Score": "2-0"},
            {"Minute": "46'", "Event": "🔄 Substitution: Václav Černý ➡️ İlhan Fakılı", "Score": "2-0"},
            {"Minute": "60'", "Event": "⚽ Goal: Orkun Kökçü (Penalty)", "Score": "3-0"},
            {"Minute": "61'", "Event": "🔄 Substitution: Hyeon-gyu Oh ➡️ Dušan Vlahović", "Score": "3-0"},
            {"Minute": "61'", "Event": "🔄 Substitution: Junior Olaitan ➡️ Amir Hadžiahmetović", "Score": "3-0"},
            {"Minute": "73'", "Event": "🔄 Substitution: Leandro Trossard ➡️ Milot Rashica", "Score": "3-0"},
            {"Minute": "82'", "Event": "🔄 Substitution: Rıdvan Yılmaz ➡️ Kassoum Ouattara", "Score": "3-0"},
            {"Minute": "90'", "Event": "🏁 Full Time: Beşiktaş JK 3 - 0 FK Kauno Žalgiris", "Score": "3-0"}
        ])
        st.dataframe(incidents_data, use_container_width=True, hide_index=True)


# ------------------------------------------------------------------------------
# CASE B: A PLAYER IS SELECTED (DETAIL VIEW - PLAYER EXCLUSIVE METRICS & HEATMAP)
# ------------------------------------------------------------------------------
else:
    secilen = st.session_state.secilen_oyuncu
    df_oyuncu = df_all[df_all["oyuncu_adi"] == secilen].copy()
    
    pos = df_oyuncu["mevki"].iloc[0] if not df_oyuncu.empty else "MF"
    opta_pts = df_oyuncu["opta_points"].iloc[0] if not df_oyuncu.empty else 6.00
    
    # Player Header Banner
    st.markdown(f"""
    <div class="bjk-header">
        <h1 class="bjk-title">🦅 {secilen}</h1>
        <div class="bjk-subtitle">Position: <strong>{pos}</strong> &nbsp;|&nbsp; <span>Beşiktaş JK</span> &nbsp;|&nbsp; <span style="color: #ffffff; text-decoration: underline;">Individual Match Performance</span></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Player Calculations
    passes = df_oyuncu[df_oyuncu["aksiyon_turu"].str.contains("Pass", case=False, na=False)]
    total_passes = len(passes)
    accurate_passes = int(passes["basarili_pas"].sum()) if "basarili_pas" in passes.columns else int(total_passes * 0.88)
    inaccurate_passes = max(0, total_passes - accurate_passes)
    pass_acc = (accurate_passes / total_passes * 100) if total_passes > 0 else 0.0
    
    total_actions = len(df_oyuncu)
    successful_actions = int((df_oyuncu["basarili"] == True).sum()) if "basarili" in df_oyuncu.columns else total_actions
    shots_count = len(df_oyuncu[df_oyuncu["aksiyon_turu"].str.contains("Shot", case=False, na=False)])
    defensive_count = len(df_oyuncu[df_oyuncu["aksiyon_turu"].str.contains("Tackle|Interception", case=False, na=False)])
    
    # Individual KPI Metric Cards
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    with kpi1:
        st.metric(
            label="⭐ Opta Rating / Points",
            value=f"{opta_pts:.2f}",
            delta="Match MVP" if opta_pts >= 9.5 else ("High Performance" if opta_pts >= 8.0 else None)
        )
    with kpi2:
        st.metric(
            label="🎯 Completed Passes / Total",
            value=f"{accurate_passes} / {total_passes}",
            delta=f"{pass_acc:.1f}% Accuracy" if total_passes > 0 else "No Passes"
        )
    with kpi3:
        st.metric(
            label="⚡ Successful Actions",
            value=f"{successful_actions}",
            delta=f"Total Actions: {total_actions}"
        )
    with kpi4:
        st.metric(
            label="🛡️ Defensive / Shots Contribution",
            value=f"{defensive_count} / {shots_count}",
            delta=f"{shots_count} Shots" if shots_count > 0 else f"{defensive_count} Defensive Actions"
        )
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Player Exclusive Heatmap (mplsoccer Pitch + KDE Plot)
    st.markdown(f"### 🏟️ {secilen} - Individual Pitch Activity & Heatmap")
    
    pitch = Pitch(
        pitch_type='statsbomb',
        pitch_color='#0c0f14',
        line_color='#e5e7eb',
        line_zorder=2,
        linewidth=1.5,
        goal_type='box'
    )
    
    fig, ax = pitch.draw(figsize=(12, 8))
    fig.patch.set_facecolor('#0c0f14')
    
    px_coords = df_oyuncu['x'].dropna()
    py_coords = df_oyuncu['y'].dropna()
    
    if len(px_coords) >= 4:
        sns.kdeplot(
            x=px_coords,
            y=py_coords,
            ax=ax,
            fill=True,
            cmap='YlOrRd',
            levels=60,
            thresh=0.05,
            alpha=0.68,
            zorder=1
        )
        pitch.scatter(
            px_coords, py_coords,
            ax=ax,
            s=45,
            c='#ffffff',
            edgecolors='#e30613',
            alpha=0.75,
            zorder=3,
            label='Action Points'
        )
    else:
        pitch.scatter(
            px_coords, py_coords,
            ax=ax,
            s=90,
            c='#e30613',
            edgecolors='#ffffff',
            alpha=0.9,
            zorder=3
        )
        
    ax.set_title(
        f"{secilen} ({pos}) - 90-Minute Ball Touches & Action Zones",
        fontsize=16,
        color='#ffffff',
        fontweight='bold',
        pad=15
    )
    
    p_col1, p_col2, p_col3 = st.columns([1, 10, 1])
    with p_col2:
        st.pyplot(fig, use_container_width=True)
    plt.close(fig)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Individual Bottom Charts: Bar Chart & Pie Chart
    p_graf1, p_graf2 = st.columns(2)
    
    # Left Column: Action Type Breakdown (Bar Chart)
    with p_graf1:
        st.markdown("#### 📊 Action Type Breakdown")
        p_act = df_oyuncu["aksiyon_turu"].value_counts().reset_index()
        p_act.columns = ["Action Type", "Count"]
        
        fig_bar = px.bar(
            p_act,
            x="Action Type",
            y="Count",
            text="Count",
            color="Count",
            color_continuous_scale=["#2a2e39", "#555b6e", "#e30613", "#ff1e27"]
        )
        fig_bar.update_traces(
            textposition='outside',
            textfont_color='white',
            marker_line_color='#ffffff',
            marker_line_width=1
        )
        fig_bar.update_layout(
            plot_bgcolor="#141822",
            paper_bgcolor="#141822",
            font_color="#ffffff",
            xaxis=dict(showgrid=False, title=""),
            yaxis=dict(showgrid=True, gridcolor="#272c3a", title="Count"),
            coloraxis_showscale=False,
            margin=dict(l=20, r=20, t=30, b=20),
            height=340
        )
        st.plotly_chart(fig_bar, use_container_width=True)
        
    # Right Column: Pass Accuracy (Pie Chart - Black & White Theme)
    with p_graf2:
        st.markdown("#### ⚽ Pass Accuracy & Completion Rate")
        if total_passes > 0:
            pas_pie_df = pd.DataFrame({
                "Status": ["Completed Passes", "Incompleted Passes"],
                "Count": [accurate_passes, inaccurate_passes]
            })
            
            fig_pie = px.pie(
                pas_pie_df,
                names="Status",
                values="Count",
                color="Status",
                color_discrete_map={
                    "Completed Passes": "#ffffff",
                    "Incompleted Passes": "#e30613"
                },
                hole=0.45
            )
            fig_pie.update_traces(
                textinfo='percent+label',
                textfont_size=14,
                textfont_color=['#000000', '#ffffff'],
                marker=dict(line=dict(color='#222222', width=2))
            )
            fig_pie.update_layout(
                plot_bgcolor="#141822",
                paper_bgcolor="#141822",
                font_color="#ffffff",
                legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5),
                margin=dict(l=20, r=20, t=30, b=20),
                height=340
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("No registered pass actions for this player in this match.")

    # Raw Data Expander
    with st.expander(f"📋 View Raw Action Records for {secilen}"):
        st.dataframe(
            df_oyuncu[["oyuncu_adi", "aksiyon_turu", "x", "y", "basarili", "opta_points"]],
            use_container_width=True,
            hide_index=True
        )

st.markdown("---")
st.caption("© 2026 Beşiktaş JK Analytics Dashboard | Powered by Streamlit & mplsoccer")
