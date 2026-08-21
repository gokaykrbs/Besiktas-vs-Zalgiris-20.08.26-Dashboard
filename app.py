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
# PAGE CONFIGURATION
# ==============================================================================
st.set_page_config(
    page_title="Beşiktaş JK - Match Performance Analytics",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# STADIUM BROADCAST THEME (CSS) - CLEAN, ULTRA-RESPONSIVE & MOBILE-OPTIMIZED
# ==============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800;900&family=Teko:wght@500;600;700&display=swap');

    /* Global Atmosphere & Horizontal Overflow Prevention */
    html, body {
        overflow-x: hidden !important;
        max-width: 100vw;
    }
    
    .stApp {
        background: radial-gradient(circle at 50% 8%, #11261b 0%, #09130d 50%, #040806 100%);
        color: #ffffff;
        font-family: 'Montserrat', sans-serif;
        overflow-x: hidden !important;
    }
    
    /* Clean Container Padding for Both Desktop and Mobile */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2.5rem !important;
        max-width: 1300px;
    }

    /* Prevent Column Blowout on Mobile */
    div[data-testid="column"] {
        min-width: 0 !important;
    }
    
    /* Clean Broadcast Scoreboard Card */
    .scoreboard-box {
        background: linear-gradient(135deg, rgba(16, 38, 27, 0.95) 0%, rgba(18, 22, 28, 0.95) 50%, rgba(160, 10, 24, 0.88) 100%);
        border: 1px solid rgba(46, 213, 115, 0.3);
        border-radius: 16px;
        padding: 20px 24px;
        margin-bottom: 20px;
        box-shadow: 0 12px 35px rgba(0, 0, 0, 0.65), inset 0 1px 0 rgba(255, 255, 255, 0.2);
    }
    
    .league-badge {
        display: inline-block;
        background: linear-gradient(90deg, #e30613, #ff4757);
        color: #ffffff;
        font-size: 0.78rem;
        font-weight: 800;
        padding: 5px 16px;
        border-radius: 20px;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        box-shadow: 0 0 14px rgba(227, 6, 19, 0.5);
        margin-bottom: 12px;
    }

    .scoreboard-grid {
        display: grid;
        grid-template-columns: 1fr auto 1fr;
        align-items: center;
        gap: 16px;
    }
    
    .team-col-left {
        text-align: left;
    }
    
    .team-col-right {
        text-align: right;
    }
    
    .team-title-text {
        font-family: 'Teko', sans-serif;
        font-size: 2.3rem;
        font-weight: 700;
        line-height: 1.1;
        letter-spacing: 0.5px;
        color: #ffffff;
        margin: 0;
        text-shadow: 0 2px 10px rgba(0,0,0,0.5);
        word-break: break-word;
    }
    
    .team-scorers {
        color: #7bed9f;
        font-size: 0.85rem;
        font-weight: 600;
        margin-top: 4px;
        line-height: 1.3;
    }
    
    .score-center-badge {
        font-family: 'Teko', sans-serif;
        font-size: 3rem;
        font-weight: 700;
        color: #ffffff;
        background: rgba(0, 0, 0, 0.7);
        padding: 6px 22px;
        border-radius: 14px;
        border: 2px solid #e30613;
        box-shadow: 0 0 25px rgba(227, 6, 19, 0.55);
        letter-spacing: 4px;
        line-height: 1;
        text-align: center;
        min-width: 120px;
        display: inline-block;
    }

    .match-venue-footer {
        border-top: 1px solid rgba(255, 255, 255, 0.12);
        margin-top: 14px;
        padding-top: 10px;
        color: #a2b89b;
        font-size: 0.82rem;
        font-weight: 500;
        display: flex;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 8px;
    }
    
    /* Holographic Metric Cards */
    div[data-testid="stMetric"] {
        background: linear-gradient(145deg, rgba(20, 42, 30, 0.88), rgba(10, 18, 14, 0.95));
        border: 1px solid rgba(46, 213, 115, 0.28);
        border-radius: 12px;
        padding: 12px 14px;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4), inset 0 0 15px rgba(46, 213, 115, 0.05);
        transition: all 0.25s ease;
        margin-bottom: 8px;
    }
    
    div[data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        border-color: #ff4757;
        box-shadow: 0 8px 24px rgba(227, 6, 19, 0.35);
    }
    
    div[data-testid="stMetricLabel"] > div {
        color: #7bed9f !important;
        font-size: 0.78rem !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 0.6px;
        white-space: normal !important;
        line-height: 1.2 !important;
    }
    
    div[data-testid="stMetricValue"] > div {
        color: #ffffff !important;
        font-size: 1.8rem !important;
        font-weight: 800 !important;
        font-family: 'Teko', sans-serif;
        letter-spacing: 0.5px;
        line-height: 1.1;
        white-space: nowrap !important;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    
    div[data-testid="stMetricDelta"] > div {
        font-size: 0.78rem !important;
        font-weight: 600 !important;
        white-space: normal !important;
        line-height: 1.2 !important;
    }
    
    /* Sidebar Navigation */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d1e15 0%, #060d09 100%);
        border-right: 1px solid rgba(46, 213, 115, 0.2);
    }
    
    section[data-testid="stSidebar"] .stButton button {
        background: linear-gradient(90deg, #13281c 0%, #1a3324 100%);
        color: #e2f0d9;
        border: 1px solid rgba(46, 213, 115, 0.22);
        border-radius: 9px;
        padding: 8px 12px;
        font-weight: 600;
        text-align: left;
        font-size: 0.85rem;
        transition: all 0.2s ease;
        margin-bottom: 2px;
    }
    
    section[data-testid="stSidebar"] .stButton button:hover {
        background: linear-gradient(90deg, #e30613 0%, #ff4757 100%) !important;
        color: #ffffff !important;
        border-color: #ff6b81 !important;
        transform: translateX(3px);
        box-shadow: 0 0 14px rgba(227, 6, 19, 0.5) !important;
    }
    
    .sidebar-heading {
        color: #7bed9f;
        font-size: 0.9rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 12px;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    .attack-dir-banner {
        background: rgba(16, 38, 27, 0.7);
        border: 1px solid rgba(46, 213, 115, 0.25);
        border-radius: 8px;
        padding: 7px 14px;
        text-align: center;
        color: #7bed9f;
        font-size: 0.82rem;
        font-weight: 700;
        letter-spacing: 0.8px;
        margin-top: 6px;
        margin-bottom: 14px;
    }

    /* Tabs Layout */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        flex-wrap: wrap;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #13241b;
        border: 1px solid rgba(46, 213, 115, 0.2);
        border-radius: 8px;
        color: #d1d5db;
        padding: 7px 14px;
        font-weight: 700;
        font-size: 0.84rem;
        white-space: normal;
        text-align: center;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #e30613, #ff4757) !important;
        color: #ffffff !important;
        border-color: #ff4757 !important;
    }

    /* Ensure Dataframe Tables Scroll Horizontally on Mobile Without Page Breaking */
    div[data-testid="stDataFrame"] {
        width: 100% !important;
        overflow-x: auto !important;
    }

    /* =========================================================================
       RESPONSIVE MEDIA QUERIES (MOBILE OPTIMIZATIONS)
       ========================================================================= */
    @media screen and (max-width: 768px) {
        .block-container {
            padding-top: 1.2rem !important;
            padding-bottom: 1.5rem !important;
            padding-left: 0.6rem !important;
            padding-right: 0.6rem !important;
        }

        .scoreboard-box {
            padding: 14px 12px;
            border-radius: 14px;
            margin-bottom: 14px;
            text-align: center;
        }

        .scoreboard-grid {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 10px;
        }

        .team-col-left, .team-col-right {
            text-align: center;
            width: 100%;
        }

        .team-title-text {
            font-size: 1.65rem;
            line-height: 1.1;
            text-align: center;
        }

        .team-scorers {
            font-size: 0.76rem;
            margin-top: 3px;
            text-align: center;
        }

        .score-center-badge {
            font-size: 2.2rem;
            padding: 4px 18px;
            letter-spacing: 3px;
            min-width: 100px;
            margin: 4px 0;
        }

        .league-badge {
            font-size: 0.68rem;
            padding: 4px 12px;
            margin-bottom: 8px;
            letter-spacing: 1px;
            display: inline-block;
        }

        .match-venue-footer {
            flex-direction: column;
            align-items: center;
            text-align: center;
            font-size: 0.74rem;
            gap: 4px;
            margin-top: 10px;
            padding-top: 8px;
        }

        div[data-testid="stMetric"] {
            padding: 10px 10px;
            border-radius: 10px;
            margin-bottom: 6px;
        }

        div[data-testid="stMetricLabel"] > div {
            font-size: 0.7rem !important;
            letter-spacing: 0.3px;
        }

        div[data-testid="stMetricValue"] > div {
            font-size: 1.45rem !important;
        }

        div[data-testid="stMetricDelta"] > div {
            font-size: 0.7rem !important;
        }

        .attack-dir-banner {
            font-size: 0.72rem;
            padding: 5px 8px;
            margin-bottom: 10px;
            letter-spacing: 0.4px;
        }

        .stTabs [data-baseweb="tab"] {
            font-size: 0.76rem;
            padding: 6px 10px;
            flex: 1 1 auto;
        }
    }

    @media screen and (max-width: 480px) {
        .team-title-text {
            font-size: 1.45rem;
        }
        
        .score-center-badge {
            font-size: 1.9rem;
            padding: 3px 14px;
            letter-spacing: 2px;
        }

        div[data-testid="stMetricValue"] > div {
            font-size: 1.3rem !important;
        }
    }
</style>
""", unsafe_allow_html=True)


# ==============================================================================
# 1. SESSION STATE MANAGEMENT
# ==============================================================================
if "secilen_oyuncu" not in st.session_state:
    st.session_state.secilen_oyuncu = None


# ==============================================================================
# ROBUST DATA LOADING & NORMALIZATION (SAFE FROM KEYERRORS)
# ==============================================================================
def load_match_data():
    file_path = "besiktas_mac_verisi.csv"
    if not os.path.exists(file_path):
        st.error(f"Data file '{file_path}' not found!")
        return pd.DataFrame()
    
    df = pd.read_csv(file_path)
    
    # Safe normalization mapping
    if "player_name" not in df.columns and "oyuncu_adi" in df.columns:
        df["player_name"] = df["oyuncu_adi"]
    elif "oyuncu_adi" not in df.columns and "player_name" in df.columns:
        df["oyuncu_adi"] = df["player_name"]
        
    if "action_type" not in df.columns and "aksiyon_turu" in df.columns:
        df["action_type"] = df["aksiyon_turu"]
    elif "aksiyon_turu" not in df.columns and "action_type" in df.columns:
        df["aksiyon_turu"] = df["action_type"]
        
    if "jersey_number" not in df.columns and "forma_no" in df.columns:
        df["jersey_number"] = df["forma_no"]
    elif "forma_no" not in df.columns and "jersey_number" in df.columns:
        df["forma_no"] = df["jersey_number"]

    if "position" not in df.columns and "mevki" in df.columns:
        df["position"] = df["mevki"]
    elif "mevki" not in df.columns and "position" in df.columns:
        df["mevki"] = df["position"]

    if "team" not in df.columns and "takim" in df.columns:
        df["team"] = df["takim"]
    elif "takim" not in df.columns and "team" in df.columns:
        df["takim"] = df["team"]

    if "is_successful" not in df.columns:
        if "basarili" in df.columns:
            df["is_successful"] = df["basarili"]
        elif "basarili_pas" in df.columns:
            df["is_successful"] = df["basarili_pas"].apply(lambda x: True if x == 1 else False)
        else:
            df["is_successful"] = True

    if "basarili" not in df.columns:
        df["basarili"] = df["is_successful"]
        
    if "basarili_pas" not in df.columns:
        df["basarili_pas"] = df["is_successful"].apply(lambda x: 1 if x else 0)

    if "end_x" not in df.columns:
        df["end_x"] = df["x"] + 15
    if "end_y" not in df.columns:
        df["end_y"] = df["y"]

    if "minutes_played" not in df.columns:
        df["minutes_played"] = 90
        
    if "outcome" not in df.columns:
        df["outcome"] = df["is_successful"].apply(lambda x: "Completed" if x else "Incompleted")

    return df

df_all = load_match_data()
if df_all.empty:
    st.stop()

# Official Beşiktaş Matchday Squad with Exact Jersey Numbers
STARTING_XI = [
    {"name": "Alexander Nübel", "pos": "GK", "no": 1, "minutes": 90, "sub_info": "Starter (Full 90')"},
    {"name": "Amir Murillo", "pos": "DF", "no": 62, "minutes": 90, "sub_info": "Starter (Full 90') ⚽ (12')"},
    {"name": "Tiago Djaló", "pos": "DF", "no": 35, "minutes": 90, "sub_info": "Starter (Full 90')"},
    {"name": "Emirhan Topçu", "pos": "DF", "no": 53, "minutes": 90, "sub_info": "Starter (Full 90') ⭐ (9.54)"},
    {"name": "Rıdvan Yılmaz", "pos": "DF", "no": 33, "minutes": 81, "sub_info": "Starter (Sub off 82') 🅰️🅰️ (2 Ast)"},
    {"name": "Salih Özcan", "pos": "MF", "no": 6, "minutes": 90, "sub_info": "Starter (Full 90')"},
    {"name": "Junior Olaitan", "pos": "MF", "no": 15, "minutes": 60, "sub_info": "Starter (Sub off 61')"},
    {"name": "Orkun Kökçü", "pos": "MF", "no": 10, "minutes": 90, "sub_info": "Starter (Full 90') ⚽ (60') 🌟 MVP"},
    {"name": "Václav Černý", "pos": "MF", "no": 18, "minutes": 45, "sub_info": "Starter (Sub off 46')"},
    {"name": "Leandro Trossard", "pos": "FW", "no": 19, "minutes": 72, "sub_info": "Starter (Sub off 73')"},
    {"name": "Hyeon-gyu Oh", "pos": "FW", "no": 9, "minutes": 60, "sub_info": "Starter (Sub off 61') ⚽ (6')"}
]

SUBSTITUTES_PLAYED = [
    {"name": "İlhan Fakılı", "pos": "MF", "no": 29, "minutes": 45, "sub_info": "Sub (46' in)"},
    {"name": "Amir Hadžiahmetović", "pos": "MF", "no": 5, "minutes": 30, "sub_info": "Sub (61' in)"},
    {"name": "Dušan Vlahović", "pos": "FW", "no": 24, "minutes": 30, "sub_info": "Sub (61' in)"},
    {"name": "Milot Rashica", "pos": "FW", "no": 7, "minutes": 18, "sub_info": "Sub (73' in)"},
    {"name": "Kassoum Ouattara", "pos": "DF", "no": 11, "minutes": 9, "sub_info": "Sub (82' in)"}
]

SUBSTITUTES_UNUSED = [
    {"name": "Doğan Alemdar", "pos": "GK", "no": 80, "minutes": 0, "sub_info": "Unused Sub (0')"},
    {"name": "Emmanuel Agbadou", "pos": "DF", "no": 12, "minutes": 0, "sub_info": "Unused Sub (0')"},
    {"name": "Taylan Bulut", "pos": "DF", "no": 22, "minutes": 0, "sub_info": "Unused Sub (0')"},
    {"name": "Yasin Özcan", "pos": "DF", "no": 58, "minutes": 0, "sub_info": "Unused Sub (0')"},
    {"name": "Wilfred Ndidi", "pos": "MF", "no": 4, "minutes": 0, "sub_info": "Unused Sub (0')"},
    {"name": "Kartal Kayra Yılmaz", "pos": "MF", "no": 8, "minutes": 0, "sub_info": "Unused Sub (0')"},
    {"name": "Semih Kılıçsoy", "pos": "FW", "no": 90, "minutes": 0, "sub_info": "Unused Sub (0')"}
]

SUBSTITUTES = SUBSTITUTES_PLAYED + SUBSTITUTES_UNUSED
ALL_SQUAD = STARTING_XI + SUBSTITUTES


# ==============================================================================
# 2. SIDEBAR - SQUAD NAVIGATION
# ==============================================================================
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/2/20/Logo_of_Besiktas_JK.svg", width=80)
    st.markdown("## 🦅 **BEŞİKTAŞ JK**")
    st.caption("UEFA Europa League • 20 August 2026")
    
    # Return to Full Team Stats Button
    if st.button("🏟️ 🦅 **FULL TEAM OVERVIEW**", use_container_width=True):
        st.session_state.secilen_oyuncu = None
        st.rerun()

    st.markdown("---")
    
    # Starting XI
    st.markdown("<div class='sidebar-heading'>⚡ STARTING XI</div>", unsafe_allow_html=True)
    for player in STARTING_XI:
        p_name = player["name"]
        p_no = player["no"]
        p_pos = player["pos"]
        
        btn_label = f"#{p_no} {p_name} ({p_pos})"
        if st.session_state.secilen_oyuncu == p_name:
            btn_label = f"🔥 🔴 #{p_no} {p_name}"
            
        if st.button(btn_label, key=f"btn_xi_{p_name}", use_container_width=True):
            st.session_state.secilen_oyuncu = p_name
            st.rerun()

    st.markdown("---")
    
    # Substitutes who played
    st.markdown("<div class='sidebar-heading'>🔄 SUBSTITUTES (SUBBED IN)</div>", unsafe_allow_html=True)
    for player in SUBSTITUTES_PLAYED:
        p_name = player["name"]
        p_no = player["no"]
        p_pos = player["pos"]
        p_min = player["minutes"]
        
        btn_label = f"#{p_no} {p_name} ({p_pos} • {p_min}')"
        if st.session_state.secilen_oyuncu == p_name:
            btn_label = f"🔥 🔴 #{p_no} {p_name}"
            
        if st.button(btn_label, key=f"btn_sub_in_{p_name}", use_container_width=True):
            st.session_state.secilen_oyuncu = p_name
            st.rerun()

    st.markdown("---")
    
    # Unused Substitutes (Bench)
    st.markdown("<div class='sidebar-heading'>🪑 UNUSED SUBS (BENCH)</div>", unsafe_allow_html=True)
    for player in SUBSTITUTES_UNUSED:
        p_name = player["name"]
        p_no = player["no"]
        p_pos = player["pos"]
        
        btn_label = f"#{p_no} {p_name} ({p_pos} • 0')"
        if st.session_state.secilen_oyuncu == p_name:
            btn_label = f"⚪ #{p_no} {p_name} (0')"
            
        if st.button(btn_label, key=f"btn_sub_un_{p_name}", use_container_width=True):
            st.session_state.secilen_oyuncu = p_name
            st.rerun()


# ==============================================================================
# 3. MAIN DASHBOARD CONTENT
# ==============================================================================

# ------------------------------------------------------------------------------
# CASE A: TEAM OVERVIEW (secilen_oyuncu is None)
# ------------------------------------------------------------------------------
if st.session_state.secilen_oyuncu is None:
    st.markdown("""
    <div class="scoreboard-box">
        <div class="league-badge">🏆 UEFA Europa League • Full Time</div>
        <div class="scoreboard-grid">
            <div class="team-col-left">
                <div class="team-title-text">🦅 BEŞİKTAŞ JK</div>
                <div class="team-scorers">⚽ H. Oh 6' • ⚽ A. Murillo 12' • ⚽ O. Kökçü (P) 60'</div>
            </div>
            <div>
                <div class="score-center-badge">3 - 0</div>
            </div>
            <div class="team-col-right">
                <div class="team-title-text" style="color: #cbd5e1;">FK KAUNO ŽALGIRIS</div>
                <div class="team-scorers" style="color: #94a3b8;">Clean Sheet Victory</div>
            </div>
        </div>
        <div class="match-venue-footer">
            <span>🏟️ <strong>Tüpraş Stadium</strong>, Istanbul</span>
            <span>👥 Attendance: <strong>31,494</strong></span>
            <span>⚖️ Referee: <strong>Tobias Stieler</strong></span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Team KPI Metric Cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="⏱️ BALL POSSESSION", value="77%", delta="+54% Dominance")
    with col2:
        st.metric(label="🎯 TOTAL SHOTS", value="21", delta="6 On Target • 3 Goals")
    with col3:
        st.metric(label="⚽ TOTAL PASSES", value="620", delta="89% Accuracy")
    with col4:
        st.metric(label="🚩 CORNER KICKS", value="15", delta="20+ Key Chances")
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Team Pitch Control Tabs: Heatmap, Passing Network, and Shot Map
    st.markdown("### 🏟️ Match Dominance & Tactical Visualizations")
    team_tab1, team_tab2, team_tab3 = st.tabs([
        "🔥 Spatial Heatmap & Pressure Zones",
        "🎯 Team Passing Flow & Vectors",
        "⚽ Shot Map & Goal Trajectories"
    ])
    
    bjk_events = df_all[df_all["takim"] == "Beşiktaş JK"] if "takim" in df_all.columns else df_all[df_all["team"] == "Beşiktaş JK"]
    
    # TAB 1: Heatmap
    with team_tab1:
        st.markdown("<div class='attack-dir-banner'>⚔️ ATTACKING DIRECTION &nbsp; ➡️ &nbsp; OPPONENT GOAL</div>", unsafe_allow_html=True)
        pitch = Pitch(
            pitch_type='statsbomb',
            pitch_color='#0f3622',
            line_color='#ffffff',
            line_zorder=2,
            linewidth=1.8,
            goal_type='box'
        )
        fig, ax = pitch.draw(figsize=(10, 6.5))
        fig.patch.set_facecolor('#09160f')
        
        x_all = bjk_events["x"].dropna()
        y_all = bjk_events["y"].dropna()
        
        if len(x_all) > 10:
            sns.kdeplot(
                x=x_all,
                y=y_all,
                ax=ax,
                fill=True,
                cmap='YlOrRd',
                levels=75,
                thresh=0.03,
                alpha=0.72,
                zorder=1
            )
            pitch.scatter(
                x_all, y_all,
                ax=ax,
                s=32,
                c='#ffffff',
                edgecolors='#e30613',
                alpha=0.55,
                zorder=3
            )
            
        ax.set_title(
            "Beşiktaş JK - 90-Minute Spatial Pressure & Territorial Control",
            fontsize=13,
            color='#ffffff',
            fontweight='bold',
            pad=10
        )
        fig.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

    # TAB 2: Passing Flow
    with team_tab2:
        st.markdown("<div class='attack-dir-banner'>⚔️ ATTACKING DIRECTION &nbsp; ➡️ &nbsp; OPPONENT GOAL</div>", unsafe_allow_html=True)
        pitch_pass = Pitch(
            pitch_type='statsbomb',
            pitch_color='#0f3622',
            line_color='#ffffff',
            line_zorder=2,
            linewidth=1.8,
            goal_type='box'
        )
        fig_pass, ax_pass = pitch_pass.draw(figsize=(10, 6.5))
        fig_pass.patch.set_facecolor('#09160f')
        
        act_col = "action_type" if "action_type" in bjk_events.columns else "aksiyon_turu"
        passes_df = bjk_events[bjk_events[act_col].str.contains("Pass", case=False, na=False)]
        
        succ_col = "is_successful" if "is_successful" in passes_df.columns else "basarili"
        comp_passes = passes_df[passes_df[succ_col] == True]
        incomp_passes = passes_df[passes_df[succ_col] == False]
        
        if not incomp_passes.empty and "end_x" in incomp_passes.columns:
            pitch_pass.arrows(
                incomp_passes["x"], incomp_passes["y"],
                incomp_passes["end_x"], incomp_passes["end_y"],
                ax=ax_pass,
                color='#ff4757',
                width=1.5,
                headwidth=3.5,
                headlength=3.5,
                alpha=0.45,
                label=f'Incompleted ({len(incomp_passes)})',
                zorder=2
            )
            
        if not comp_passes.empty and "end_x" in comp_passes.columns:
            pitch_pass.arrows(
                comp_passes["x"], comp_passes["y"],
                comp_passes["end_x"], comp_passes["end_y"],
                ax=ax_pass,
                color='#2ed573',
                width=2.0,
                headwidth=4.0,
                headlength=4.0,
                alpha=0.75,
                label=f'Completed ({len(comp_passes)})',
                zorder=3
            )
            
        ax_pass.set_title(
            f"Beşiktaş JK - Match Passing Flow ({len(comp_passes)} Completed / {len(passes_df)} Total • 89% Precision)",
            fontsize=13,
            color='#ffffff',
            fontweight='bold',
            pad=10
        )
        ax_pass.legend(facecolor='#0d1e15', edgecolor='#2ed573', labelcolor='white', loc='upper left', fontsize=9)
        fig_pass.tight_layout()
        st.pyplot(fig_pass, use_container_width=True)
        plt.close(fig_pass)
        
    # TAB 3: Team Shot Map & Goal Trajectories
    with team_tab3:
        st.markdown("<div class='attack-dir-banner'>⚔️ ATTACKING DIRECTION &nbsp; ➡️ &nbsp; OPPONENT GOAL</div>", unsafe_allow_html=True)
        pitch_shot = Pitch(
            pitch_type='statsbomb',
            pitch_color='#0f3622',
            line_color='#ffffff',
            line_zorder=2,
            linewidth=1.8,
            goal_type='box'
        )
        fig_shot, ax_shot = pitch_shot.draw(figsize=(10, 6.5))
        fig_shot.patch.set_facecolor('#09160f')
        
        act_col_shot = "action_type" if "action_type" in bjk_events.columns else "aksiyon_turu"
        shots_df = bjk_events[bjk_events[act_col_shot].str.contains("Shot", case=False, na=False)].copy()
        
        goals_df = shots_df[shots_df["outcome"].str.contains("Goal", case=False, na=False)]
        on_target_df = shots_df[shots_df["outcome"].str.contains("Target", case=False, na=False) & ~shots_df["outcome"].str.contains("Goal", case=False, na=False)]
        blocked_df = shots_df[shots_df["outcome"].str.contains("Blocked", case=False, na=False)]
        off_target_df = shots_df[shots_df["outcome"].str.contains("Off", case=False, na=False)]
        
        # Draw Shot Trajectory Lines
        for _, s_row in shots_df.iterrows():
            is_goal = "Goal" in str(s_row.get("outcome", ""))
            is_target = "Target" in str(s_row.get("outcome", "")) and not is_goal
            line_color = '#ffd700' if is_goal else ('#2ed573' if is_target else '#ff4757')
            line_width = 2.5 if is_goal else 1.5
            pitch_shot.lines(
                s_row["x"], s_row["y"], s_row["end_x"], s_row["end_y"],
                ax=ax_shot,
                color=line_color,
                lw=line_width,
                alpha=0.85 if is_goal else 0.45,
                zorder=2
            )
            
        # Draw Shot Outcome Markers
        if not off_target_df.empty:
            pitch_shot.scatter(
                off_target_df["x"], off_target_df["y"],
                ax=ax_shot,
                s=100,
                c='#ff4757',
                marker='x',
                linewidths=2.2,
                label=f'Shot Off Target ({len(off_target_df)})',
                zorder=3
            )
        if not blocked_df.empty:
            pitch_shot.scatter(
                blocked_df["x"], blocked_df["y"],
                ax=ax_shot,
                s=90,
                c='#a855f7',
                marker='s',
                edgecolors='#ffffff',
                linewidths=1.2,
                label=f'Blocked Shot ({len(blocked_df)})',
                zorder=3
            )
        if not on_target_df.empty:
            pitch_shot.scatter(
                on_target_df["x"], on_target_df["y"],
                ax=ax_shot,
                s=120,
                c='#2ed573',
                marker='o',
                edgecolors='#ffffff',
                linewidths=1.5,
                label=f'Shot On Target / Saved ({len(on_target_df)})',
                zorder=4
            )
        if not goals_df.empty:
            pitch_shot.scatter(
                goals_df["x"], goals_df["y"],
                ax=ax_shot,
                s=260,
                c='#ffd700',
                marker='*',
                edgecolors='#e30613',
                linewidths=2.0,
                label=f'GOAL ⚽ ({len(goals_df)})',
                zorder=5
            )
            for _, g_row in goals_df.iterrows():
                p_name_short = str(g_row.get("player_name", "")).split(" ")[-1]
                ax_shot.text(
                    g_row["x"], g_row["y"] - 3.2,
                    f"⚽ {p_name_short}",
                    color='#ffd700',
                    fontsize=9.5,
                    fontweight='bold',
                    ha='center',
                    zorder=6
                )
            
        ax_shot.set_title(
            f"Beşiktaş JK - Match Shot Map ({len(goals_df)} Goals • {len(on_target_df) + len(goals_df)} On Target / {len(shots_df)} Total Shots)",
            fontsize=13,
            color='#ffffff',
            fontweight='bold',
            pad=10
        )
        ax_shot.legend(facecolor='#0d1e15', edgecolor='#ffd700', labelcolor='white', loc='upper left', fontsize=9)
        fig_shot.tight_layout()
        st.pyplot(fig_shot, use_container_width=True)
        plt.close(fig_shot)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Team Bottom Visualizations
    g_col1, g_col2 = st.columns(2)
    with g_col1:
        st.markdown("#### ⚡ Team Action Breakdown")
        act_c = "action_type" if "action_type" in bjk_events.columns else "aksiyon_turu"
        team_action_counts = bjk_events[act_c].value_counts().reset_index()
        team_action_counts.columns = ["Action Type", "Count"]
        max_action = team_action_counts["Count"].max() if not team_action_counts.empty else 100
        
        fig_team_bar = px.bar(
            team_action_counts,
            x="Action Type",
            y="Count",
            text="Count",
            color="Count",
            color_continuous_scale=["#164e33", "#2ed573", "#ff4757", "#e30613"]
        )
        fig_team_bar.update_traces(
            textposition='outside',
            textfont_color='white',
            marker_line_color='#ffffff',
            marker_line_width=1.2
        )
        fig_team_bar.update_layout(
            autosize=True,
            plot_bgcolor="rgba(16, 38, 27, 0.75)",
            paper_bgcolor="rgba(16, 38, 27, 0.75)",
            font_color="#ffffff",
            xaxis=dict(showgrid=False, title="", tickfont=dict(size=11)),
            yaxis=dict(showgrid=True, gridcolor="rgba(46, 213, 115, 0.15)", title="Actions", range=[0, max_action * 1.25], tickfont=dict(size=11)),
            coloraxis_showscale=False,
            margin=dict(l=15, r=15, t=25, b=15),
            height=320
        )
        st.plotly_chart(fig_team_bar, use_container_width=True, config={'displayModeBar': False, 'responsive': True})
        
    with g_col2:
        st.markdown("#### ⏱️ Match Timeline & Key Moments")
        incidents_data = pd.DataFrame([
            {"Min": "6'", "Key Moment": "⚽ GOAL: Hyeon-gyu Oh (Assist: Rıdvan Yılmaz)", "Score": "1 - 0"},
            {"Min": "12'", "Key Moment": "⚽ GOAL: Amir Murillo (Assist: Rıdvan Yılmaz)", "Score": "2 - 0"},
            {"Min": "46'", "Key Moment": "🔄 Tactical Sub: Václav Černý ➡️ İlhan Fakılı", "Score": "2 - 0"},
            {"Min": "60'", "Key Moment": "⚽ GOAL: Orkun Kökçü (Ice-Cold Penalty)", "Score": "3 - 0"},
            {"Min": "61'", "Key Moment": "🔄 Tactical Sub: Hyeon-gyu Oh ➡️ Dušan Vlahović", "Score": "3 - 0"},
            {"Min": "61'", "Key Moment": "🔄 Tactical Sub: Junior Olaitan ➡️ Amir Hadžiahmetović", "Score": "3 - 0"},
            {"Min": "73'", "Key Moment": "🔄 Tactical Sub: Leandro Trossard ➡️ Milot Rashica", "Score": "3 - 0"},
            {"Min": "82'", "Key Moment": "?? Tactical Sub: R?dvan Y?lmaz ?? Kassoum Ouattara", "Score": "3 - 0"},
            {"Min": "90'", "Key Moment": "?? FULL TIME: Dominant 3-0 Victory", "Score": "3 - 0"}
        ])
        st.dataframe(
            incidents_data,
            use_container_width=True,
            hide_index=True
        )


# ------------------------------------------------------------------------------
# CASE B: PLAYER DETAIL VIEW (secilen_oyuncu is not None)
# ------------------------------------------------------------------------------
else:
    secilen = st.session_state.secilen_oyuncu
    
    # Safe player subset filtering
    name_col = "player_name" if "player_name" in df_all.columns else "oyuncu_adi"
    df_oyuncu = df_all[df_all[name_col] == secilen].copy()
    if df_oyuncu.empty and "oyuncu_adi" in df_all.columns:
        df_oyuncu = df_all[df_all["oyuncu_adi"] == secilen].copy()
    if df_oyuncu.empty and "player_name" in df_all.columns:
        df_oyuncu = df_all[df_all["player_name"] == secilen].copy()
    
    # Find metadata in ALL_SQUAD
    roster_info = next((p for p in ALL_SQUAD if p["name"] == secilen), {})
    pos = roster_info.get("pos", df_oyuncu["position"].iloc[0] if ("position" in df_oyuncu.columns and not df_oyuncu.empty) else "MF")
    jersey_no = roster_info.get("no", df_oyuncu["jersey_number"].iloc[0] if ("jersey_number" in df_oyuncu.columns and not df_oyuncu.empty) else "")
    
    # Check minutes played
    if "minutes" in roster_info:
        mins_played = int(roster_info["minutes"])
    elif "minutes_played" in df_oyuncu.columns and not df_oyuncu.empty and pd.notna(df_oyuncu["minutes_played"].iloc[0]):
        mins_played = int(df_oyuncu["minutes_played"].iloc[0])
    else:
        mins_played = 0

    sub_status = roster_info.get("sub_info", df_oyuncu["sub_info"].iloc[0] if ("sub_info" in df_oyuncu.columns and not df_oyuncu.empty) else ("Unused Sub (0')" if mins_played == 0 else f"Sub ({mins_played}' played)"))
    
    # Filter active on-pitch actions (exclude 'Did Not Play' or NaN coordinates)
    act_c = "action_type" if "action_type" in df_oyuncu.columns else "aksiyon_turu"
    df_active_actions = df_oyuncu[~df_oyuncu[act_c].isin(["Did Not Play", "none", "None", np.nan]) & df_oyuncu['x'].notna()] if not df_oyuncu.empty else pd.DataFrame()
    
    has_played = (mins_played > 0) and (not df_active_actions.empty)

    # Opta Points calculation
    if has_played and "opta_points" in df_oyuncu.columns and not df_oyuncu.empty and pd.notna(df_oyuncu["opta_points"].iloc[0]):
        try:
            opta_pts = float(df_oyuncu["opta_points"].iloc[0])
        except (ValueError, TypeError):
            opta_pts = None
    else:
        opta_pts = None

    opta_str = f"{opta_pts:.2f}" if (opta_pts is not None and pd.notna(opta_pts)) else "—"

    # 1. Player Spotlight Scoreboard Box
    if has_played:
        st.markdown(f"""
        <div class="scoreboard-box">
            <div class="league-badge">⭐ Player Spotlight • Match Performance</div>
            <div class="scoreboard-grid">
                <div class="team-col-left">
                    <div class="team-title-text">#{jersey_no} {secilen.upper()}</div>
                    <div class="team-scorers">Position: <strong>{pos}</strong> &nbsp;•&nbsp; ⏱️ <strong>{mins_played} Minutes Played</strong> ({sub_status})</div>
                </div>
                <div>
                    <div class="score-center-badge" style="border-color: #2ed573; box-shadow: 0 0 25px rgba(46, 213, 115, 0.45);">
                        {opta_str} <span style="font-size: 1rem; color: #7bed9f;">PTS</span>
                    </div>
                </div>
                <div class="team-col-right">
                    <div class="team-title-text" style="color: #cbd5e1;">🦅 BEŞİKTAŞ JK</div>
                    <div class="team-scorers" style="color: #94a3b8;">Match Duration: <strong>{mins_played}'</strong></div>
                </div>
            </div>
            <div class="match-venue-footer">
                <span>🏟️ <strong>Tüpraş Stadium</strong>, Istanbul</span>
                <span>⏱️ Match Duration: <strong>{mins_played} Minutes</strong></span>
                <span>🏆 UEFA Europa League (Beşiktaş 3 - 0 Zalgiris)</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 2. Player Metrics Calculations
        passes = df_active_actions[df_active_actions[act_c].str.contains("Pass", case=False, na=False)]
        total_passes = len(passes)
        
        succ_c = "is_successful" if "is_successful" in passes.columns else ("basarili" if "basarili" in passes.columns else "basarili_pas")
        if succ_c in passes.columns:
            accurate_passes = int((passes[succ_c] == True).sum() if passes[succ_c].dtype == bool else (passes[succ_c] == 1).sum())
        else:
            accurate_passes = int(total_passes * 0.89)
            
        inaccurate_passes = max(0, total_passes - accurate_passes)
        pass_acc = (accurate_passes / total_passes * 100) if total_passes > 0 else 0.0
        
        total_actions = len(df_active_actions)
        player_shots = df_active_actions[df_active_actions[act_c].str.contains("Shot", case=False, na=False)]
        shots_count = len(player_shots)
        goals_count = len(player_shots[player_shots["outcome"].str.contains("Goal", case=False, na=False)]) if not player_shots.empty else 0
        on_target_shots = len(player_shots[player_shots["outcome"].str.contains("Target", case=False, na=False)]) if not player_shots.empty else 0
        
        defensive_count = len(df_active_actions[df_active_actions[act_c].str.contains("Tackle|Interception", case=False, na=False)])
        chances_count = len(df_active_actions[df_active_actions[act_c].str.contains("Chance", case=False, na=False)])

        # Individual KPI Cards (Played)
        kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
        with kpi1:
            st.metric(
                label="⭐ OPTA RATING",
                value=opta_str,
                delta="🌟 MVP" if (opta_pts and opta_pts >= 9.5) else ("🔥 Masterclass" if (opta_pts and opta_pts >= 8.0) else "Solid")
            )
        with kpi2:
            st.metric(
                label="⏱️ MINUTES PLAYED",
                value=f"{mins_played}'",
                delta=sub_status
            )
        with kpi3:
            st.metric(
                label="🎯 PASS ACCURACY",
                value=f"{accurate_passes} / {total_passes}",
                delta=f"{pass_acc:.1f}% Precision" if total_passes > 0 else "No Passes"
            )
        with kpi4:
            st.metric(
                label="⚽ SHOTS / GOALS",
                value=f"{shots_count} Shots",
                delta=f"⚽ {goals_count} Goal(s)" if goals_count > 0 else (f"{on_target_shots} On Target" if on_target_shots > 0 else "Attacking Attempts")
            )
        with kpi5:
            st.metric(
                label="🛡️ DEFENSE / CHANCES",
                value=f"{defensive_count} / {chances_count}",
                delta=f"{chances_count} Key Chances" if chances_count > 0 else f"{defensive_count} Recoveries"
            )

        st.markdown("<br>", unsafe_allow_html=True)
        
        # 3. Player Visualizations: Heatmap, Passing Map, and Shot Map
        st.markdown(f"### 🏟️ #{jersey_no} {secilen} - Tactical Spatial Maps")
        tab_p1, tab_p2, tab_p3 = st.tabs([
            "🔥 Spatial Activity & Touch Heatmap",
            "🎯 Accurate Passing Map & Vectors",
            "⚽ Individual Shot Map & Trajectories"
        ])
        
        # TAB P1: Heatmap
        with tab_p1:
            st.markdown("<div class='attack-dir-banner'>⚔️ ATTACKING DIRECTION &nbsp; ➡️ &nbsp; OPPONENT GOAL</div>", unsafe_allow_html=True)
            pitch_indiv = Pitch(
                pitch_type='statsbomb',
                pitch_color='#0f3622',
                line_color='#ffffff',
                line_zorder=2,
                linewidth=1.8,
                goal_type='box'
            )
            fig_indiv, ax_indiv = pitch_indiv.draw(figsize=(10, 6.5))
            fig_indiv.patch.set_facecolor('#09160f')
            
            px_coords = df_active_actions['x'].dropna()
            py_coords = df_active_actions['y'].dropna()
            
            if len(px_coords) >= 4:
                sns.kdeplot(
                    x=px_coords,
                    y=py_coords,
                    ax=ax_indiv,
                    fill=True,
                    cmap='YlOrRd',
                    levels=65,
                    thresh=0.04,
                    alpha=0.75,
                    zorder=1
                )
                pitch_indiv.scatter(
                    px_coords, py_coords,
                    ax=ax_indiv,
                    s=55,
                    c='#ffffff',
                    edgecolors='#e30613',
                    alpha=0.8,
                    zorder=3,
                    label='Action Point'
                )
            else:
                pitch_indiv.scatter(
                    px_coords, py_coords,
                    ax=ax_indiv,
                    s=95,
                    c='#ff4757',
                    edgecolors='#ffffff',
                    alpha=0.9,
                    zorder=3
                )
                
            ax_indiv.set_title(
                f"#{jersey_no} {secilen} ({pos}) - Ball Contact Heatmap & Influence Zones ({mins_played}' Played)",
                fontsize=13,
                color='#ffffff',
                fontweight='bold',
                pad=10
            )
            fig_indiv.tight_layout()
            st.pyplot(fig_indiv, use_container_width=True)
            plt.close(fig_indiv)

        # TAB P2: Passing Map
        with tab_p2:
            st.markdown("<div class='attack-dir-banner'>⚔️ ATTACKING DIRECTION &nbsp; ➡️ &nbsp; OPPONENT GOAL</div>", unsafe_allow_html=True)
            pitch_p_pass = Pitch(
                pitch_type='statsbomb',
                pitch_color='#0f3622',
                line_color='#ffffff',
                line_zorder=2,
                linewidth=1.8,
                goal_type='box'
            )
            fig_p_pass, ax_p_pass = pitch_p_pass.draw(figsize=(10, 6.5))
            fig_p_pass.patch.set_facecolor('#09160f')
            
            succ_p = "is_successful" if "is_successful" in passes.columns else "basarili"
            p_comp = passes[passes[succ_p] == True]
            p_incomp = passes[passes[succ_p] == False]
            
            if not p_incomp.empty and "end_x" in p_incomp.columns:
                pitch_p_pass.arrows(
                    p_incomp["x"], p_incomp["y"],
                    p_incomp["end_x"], p_incomp["end_y"],
                    ax=ax_p_pass,
                    color='#ff4757',
                    width=1.6,
                    headwidth=3.8,
                    headlength=3.8,
                    alpha=0.45,
                    label=f'Incompleted ({len(p_incomp)})',
                    zorder=2
                )
                
            if not p_comp.empty and "end_x" in p_comp.columns:
                pitch_p_pass.arrows(
                    p_comp["x"], p_comp["y"],
                    p_comp["end_x"], p_comp["end_y"],
                    ax=ax_p_pass,
                    color='#2ed573',
                    width=2.2,
                    headwidth=4.2,
                    headlength=4.2,
                    alpha=0.82,
                    label=f'Completed ({len(p_comp)})',
                    zorder=3
                )
                
            ax_p_pass.set_title(
                f"#{jersey_no} {secilen} - Accurate Passing Map ({accurate_passes} Completed / {total_passes} Total • {pass_acc:.1f}% Accuracy)",
                fontsize=13,
                color='#ffffff',
                fontweight='bold',
                pad=10
            )
            ax_p_pass.legend(facecolor='#0d1e15', edgecolor='#2ed573', labelcolor='white', loc='upper left', fontsize=9)
            fig_p_pass.tight_layout()
            st.pyplot(fig_p_pass, use_container_width=True)
            plt.close(fig_p_pass)

        # TAB P3: Individual Shot Map
        with tab_p3:
            st.markdown("<div class='attack-dir-banner'>⚔️ ATTACKING DIRECTION &nbsp; ➡️ &nbsp; OPPONENT GOAL</div>", unsafe_allow_html=True)
            pitch_p_shot = Pitch(
                pitch_type='statsbomb',
                pitch_color='#0f3622',
                line_color='#ffffff',
                line_zorder=2,
                linewidth=1.8,
                goal_type='box'
            )
            fig_p_shot, ax_p_shot = pitch_p_shot.draw(figsize=(10, 6.5))
            fig_p_shot.patch.set_facecolor('#09160f')
            
            if not player_shots.empty:
                p_goals = player_shots[player_shots["outcome"].str.contains("Goal", case=False, na=False)]
                p_on_target = player_shots[player_shots["outcome"].str.contains("Target", case=False, na=False) & ~player_shots["outcome"].str.contains("Goal", case=False, na=False)]
                p_blocked = player_shots[player_shots["outcome"].str.contains("Blocked", case=False, na=False)]
                p_off_target = player_shots[player_shots["outcome"].str.contains("Off", case=False, na=False)]
                
                # Shot Lines
                for _, s_row in player_shots.iterrows():
                    is_g = "Goal" in str(s_row.get("outcome", ""))
                    is_ont = "Target" in str(s_row.get("outcome", "")) and not is_g
                    c_line = '#ffd700' if is_g else ('#2ed573' if is_ont else '#ff4757')
                    w_line = 3.0 if is_g else 1.8
                    pitch_p_shot.lines(
                        s_row["x"], s_row["y"], s_row["end_x"], s_row["end_y"],
                        ax=ax_p_shot,
                        color=c_line,
                        lw=w_line,
                        alpha=0.9 if is_g else 0.55,
                        zorder=2
                    )
                    
                if not p_off_target.empty:
                    pitch_p_shot.scatter(
                        p_off_target["x"], p_off_target["y"],
                        ax=ax_p_shot,
                        s=110,
                        c='#ff4757',
                        marker='x',
                        linewidths=2.2,
                        label=f'Off Target ({len(p_off_target)})',
                        zorder=3
                    )
                if not p_blocked.empty:
                    pitch_p_shot.scatter(
                        p_blocked["x"], p_blocked["y"],
                        ax=ax_p_shot,
                        s=100,
                        c='#a855f7',
                        marker='s',
                        edgecolors='#ffffff',
                        linewidths=1.2,
                        label=f'Blocked ({len(p_blocked)})',
                        zorder=3
                    )
                if not p_on_target.empty:
                    pitch_p_shot.scatter(
                        p_on_target["x"], p_on_target["y"],
                        ax=ax_p_shot,
                        s=120,
                        c='#2ed573',
                        marker='o',
                        edgecolors='#ffffff',
                        linewidths=1.5,
                        label=f'On Target / Saved ({len(p_on_target)})',
                        zorder=4
                    )
                if not p_goals.empty:
                    pitch_p_shot.scatter(
                        p_goals["x"], p_goals["y"],
                        ax=ax_p_shot,
                        s=280,
                        c='#ffd700',
                        marker='*',
                        edgecolors='#e30613',
                        linewidths=2.0,
                        label=f'GOAL ⚽ ({len(p_goals)})',
                        zorder=5
                    )
                    for _, g_row in p_goals.iterrows():
                        ax_p_shot.text(
                            g_row["x"], g_row["y"] - 3.2,
                            f"⚽ {g_row.get('outcome', 'Goal')}",
                            color='#ffd700',
                            fontsize=10,
                            fontweight='bold',
                            ha='center',
                            zorder=6
                        )
                        
                ax_p_shot.set_title(
                    f"#{jersey_no} {secilen} - Individual Shot Map ({goals_count} Goals • {shots_count} Total Shots)",
                    fontsize=13,
                    color='#ffffff',
                    fontweight='bold',
                    pad=10
                )
                ax_p_shot.legend(facecolor='#0d1e15', edgecolor='#ffd700', labelcolor='white', loc='upper left', fontsize=9)
            else:
                ax_p_shot.text(
                    60, 40,
                    f"No shot attempts recorded for #{jersey_no} {secilen} in this match.",
                    color='#94a3b8',
                    fontsize=12,
                    fontweight='bold',
                    ha='center',
                    va='center'
                )
                ax_p_shot.set_title(
                    f"#{jersey_no} {secilen} - Shot Map (0 Shots)",
                    fontsize=13,
                    color='#ffffff',
                    fontweight='bold',
                    pad=10
                )
                
            fig_p_shot.tight_layout()
            st.pyplot(fig_p_shot, use_container_width=True)
            plt.close(fig_p_shot)
            
        st.markdown("<br>", unsafe_allow_html=True)
    
        # 4. Individual Charts
        p_graf1, p_graf2 = st.columns(2)
        
        with p_graf1:
            st.markdown("#### 📊 Action Distribution")
            act_cl = "action_type" if "action_type" in df_active_actions.columns else "aksiyon_turu"
            p_act = df_active_actions[act_cl].value_counts().reset_index()
            p_act.columns = ["Action Type", "Count"]
            max_p_act = max(10, int(p_act["Count"].max())) if not p_act.empty else 10
            
            fig_bar = px.bar(
                p_act,
                x="Action Type",
                y="Count",
                text="Count",
                color="Count",
                color_continuous_scale=["#164e33", "#2ed573", "#ff4757", "#e30613"]
            )
            fig_bar.update_traces(
                textposition='outside',
                textfont_color='white',
                marker_line_color='#ffffff',
                marker_line_width=1.2
            )
            fig_bar.update_layout(
                autosize=True,
                plot_bgcolor="rgba(16, 38, 27, 0.75)",
                paper_bgcolor="rgba(16, 38, 27, 0.75)",
                font_color="#ffffff",
                xaxis=dict(showgrid=False, title="", tickfont=dict(size=11)),
                yaxis=dict(showgrid=True, gridcolor="rgba(46, 213, 115, 0.15)", title="Count", range=[0, max_p_act * 1.25], tickfont=dict(size=11)),
                coloraxis_showscale=False,
                margin=dict(l=15, r=15, t=25, b=15),
                height=320
            )
            st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False, 'responsive': True})
            
        with p_graf2:
            st.markdown("#### ⚽ Pass Completion Rate")
            if total_passes > 0:
                pas_pie_df = pd.DataFrame({
                    "Status": ["Accurate Passes", "Incompleted Passes"],
                    "Count": [accurate_passes, inaccurate_passes]
                })
                
                fig_pie = px.pie(
                    pas_pie_df,
                    names="Status",
                    values="Count",
                    color="Status",
                    color_discrete_map={
                        "Accurate Passes": "#2ed573",
                        "Incompleted Passes": "#ff4757"
                    },
                    hole=0.5
                )
                fig_pie.update_traces(
                    textinfo='percent+label',
                    textfont_size=12,
                    textfont_color='white',
                    marker=dict(line=dict(color='#0d1a13', width=2))
                )
                fig_pie.update_layout(
                    autosize=True,
                    plot_bgcolor="rgba(16, 38, 27, 0.75)",
                    paper_bgcolor="rgba(16, 38, 27, 0.75)",
                    font_color="#ffffff",
                    legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5, font=dict(size=11)),
                    margin=dict(l=15, r=15, t=25, b=25),
                    height=320
                )
                st.plotly_chart(fig_pie, use_container_width=True, config={'displayModeBar': False, 'responsive': True})
            else:
                st.info("Bu oyuncuya ait kayıtlı pas verisi bulunmamaktadır.")
    
        # 5. Detailed Event Logs Expander
        with st.expander(f"📋 Detailed Event Logs for #{jersey_no} {secilen} ({mins_played} Minutes Played)"):
            table_df = df_active_actions.copy()
            
            display_cols = {
                "player_name": "Player Name",
                "jersey_number": "Jersey #",
                "position": "Position",
                "minutes_played": "Minutes Played",
                "action_type": "Action Type",
                "outcome": "Outcome",
                "shot_detail": "Event Detail",
                "x": "Pitch Start X",
                "y": "Pitch Start Y",
                "end_x": "Pitch End X",
                "end_y": "Pitch End Y",
                "opta_points": "Opta Rating"
            }
            
            for c in display_cols.keys():
                if c not in table_df.columns:
                    if c == "player_name":
                        table_df["player_name"] = secilen
                    elif c == "jersey_number":
                        table_df["jersey_number"] = jersey_no
                    elif c == "position":
                        table_df["position"] = pos
                    elif c == "minutes_played":
                        table_df["minutes_played"] = mins_played
                    elif c == "action_type" and "aksiyon_turu" in table_df.columns:
                        table_df["action_type"] = table_df["aksiyon_turu"]
                    elif c == "outcome" and "basarili" in table_df.columns:
                        table_df["outcome"] = table_df["basarili"].apply(lambda x: "Completed" if x else "Incompleted")
                    elif c == "shot_detail":
                        table_df["shot_detail"] = table_df["action_type"]
                    elif c == "end_x":
                        table_df["end_x"] = table_df["x"] + 10
                    elif c == "end_y":
                        table_df["end_y"] = table_df["y"]
                    elif c == "opta_points":
                        table_df["opta_points"] = opta_str
    
            present_cols = [c for c in display_cols.keys() if c in table_df.columns]
            english_table = table_df[present_cols].rename(columns=display_cols)
            
            st.dataframe(
                english_table,
                use_container_width=True,
                hide_index=True
            )
    
    else:
        # CASE: UNUSED SUBSTITUTE (SÜRE ALMAYAN OYUNCU)
        st.markdown(f"""
        <div class="scoreboard-box">
            <div class="league-badge" style="background: linear-gradient(90deg, #475569, #64748b); box-shadow: 0 0 14px rgba(100, 116, 139, 0.4);">🪑 Kadroda / Süre Almadı • Yedek Kulübesi</div>
            <div class="scoreboard-grid">
                <div class="team-col-left">
                    <div class="team-title-text">#{jersey_no} {secilen.upper()}</div>
                    <div class="team-scorers" style="color: #cbd5e1;">Mevki: <strong>{pos}</strong> &nbsp;•&nbsp; ⏱️ <strong>Süre Almadı (0 Dakika)</strong></div>
                </div>
                <div>
                    <div class="score-center-badge" style="border-color: #64748b; box-shadow: 0 0 20px rgba(100, 116, 139, 0.25); color: #94a3b8; font-size: 2.1rem;">
                        — <span style="font-size: 0.85rem; color: #64748b;">N/A</span>
                    </div>
                </div>
                <div class="team-col-right">
                    <div class="team-title-text" style="color: #cbd5e1;">🦅 BEŞİKTAŞ JK</div>
                    <div class="team-scorers" style="color: #94a3b8;">Maç Durumu: <strong>Yedek (Unused Sub)</strong></div>
                </div>
            </div>
            <div class="match-venue-footer">
                <span>🏟️ <strong>Tüpraş Stadyumu</strong>, İstanbul</span>
                <span>⏱️ Oynanan Süre: <strong>0 Dakika</strong></span>
                <span>🏆 UEFA Europa League (Beşiktaş 3 - 0 Zalgiris)</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.info(f"ℹ️ **#{jersey_no} {secilen}** ({pos}) bu karşılaşmada yedek kulübesinde yer almış olup süre almamıştır. Bu nedenle oyuncuya ait kayıtlı maç istatistiği, pas, şut veya temas verisi bulunmamaktadır.")
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748b; font-size: 0.8rem; padding: 10px 0 20px 0; line-height: 1.6;">
    ⚽ <strong>2026 Beşiktaş JK Matchday Performance Intelligence</strong> • Powered by <strong>Streamlit</strong> & <strong>mplsoccer</strong><br>
    ⚖️ <em>Disclaimer: This application is strictly developed for educational, research, and non-commercial portfolio demonstration purposes. All team names, crests, and trademarks belong to their respective owners.</em>
</div>
""", unsafe_allow_html=True)
