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
# STADIUM BROADCAST THEME (CSS) - CLEAN & RESPONSIVE
# ==============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800;900&family=Teko:wght@500;600;700&display=swap');

    /* Global Atmosphere */
    .stApp {
        background: radial-gradient(circle at 50% 8%, #11261b 0%, #09130d 50%, #040806 100%);
        color: #ffffff;
        font-family: 'Montserrat', sans-serif;
    }
    
    /* Clean Broadcast Scoreboard Card (CSS Grid) */
    .scoreboard-box {
        background: linear-gradient(135deg, rgba(16, 38, 27, 0.95) 0%, rgba(18, 22, 28, 0.95) 50%, rgba(160, 10, 24, 0.88) 100%);
        border: 1px solid rgba(46, 213, 115, 0.3);
        border-radius: 18px;
        padding: 24px 30px;
        margin-bottom: 24px;
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
        margin-bottom: 14px;
    }

    .scoreboard-grid {
        display: grid;
        grid-template-columns: 1fr auto 1fr;
        align-items: center;
        gap: 20px;
    }
    
    .team-col-left {
        text-align: left;
    }
    
    .team-col-right {
        text-align: right;
    }
    
    .team-title-text {
        font-family: 'Teko', sans-serif;
        font-size: 2.5rem;
        font-weight: 700;
        line-height: 1.1;
        letter-spacing: 0.5px;
        color: #ffffff;
        margin: 0;
        text-shadow: 0 2px 10px rgba(0,0,0,0.5);
    }
    
    .team-scorers {
        color: #7bed9f;
        font-size: 0.88rem;
        font-weight: 600;
        margin-top: 6px;
        line-height: 1.4;
    }
    
    .score-center-badge {
        font-family: 'Teko', sans-serif;
        font-size: 3.2rem;
        font-weight: 700;
        color: #ffffff;
        background: rgba(0, 0, 0, 0.7);
        padding: 6px 26px;
        border-radius: 14px;
        border: 2px solid #e30613;
        box-shadow: 0 0 25px rgba(227, 6, 19, 0.55);
        letter-spacing: 6px;
        line-height: 1;
        text-align: center;
        min-width: 140px;
    }

    .match-venue-footer {
        border-top: 1px solid rgba(255, 255, 255, 0.12);
        margin-top: 16px;
        padding-top: 12px;
        color: #a2b89b;
        font-size: 0.88rem;
        font-weight: 500;
        display: flex;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 10px;
    }
    
    /* Holographic Metric Cards */
    div[data-testid="stMetric"] {
        background: linear-gradient(145deg, rgba(20, 42, 30, 0.88), rgba(10, 18, 14, 0.95));
        border: 1px solid rgba(46, 213, 115, 0.28);
        border-radius: 14px;
        padding: 14px 18px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4), inset 0 0 15px rgba(46, 213, 115, 0.05);
        transition: all 0.25s ease;
    }
    
    div[data-testid="stMetric"]:hover {
        transform: translateY(-3px);
        border-color: #ff4757;
        box-shadow: 0 10px 28px rgba(227, 6, 19, 0.35);
    }
    
    div[data-testid="stMetricLabel"] > div {
        color: #7bed9f !important;
        font-size: 0.82rem !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }
    
    div[data-testid="stMetricValue"] > div {
        color: #ffffff !important;
        font-size: 2rem !important;
        font-weight: 800 !important;
        font-family: 'Teko', sans-serif;
        letter-spacing: 0.5px;
        line-height: 1.2;
    }
    
    div[data-testid="stMetricDelta"] > div {
        font-size: 0.85rem !important;
        font-weight: 600 !important;
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
        font-size: 0.86rem;
        transition: all 0.2s ease;
        margin-bottom: 2px;
    }
    
    section[data-testid="stSidebar"] .stButton button:hover {
        background: linear-gradient(90deg, #e30613 0%, #ff4757 100%) !important;
        color: #ffffff !important;
        border-color: #ff6b81 !important;
        transform: translateX(4px);
        box-shadow: 0 0 14px rgba(227, 6, 19, 0.5) !important;
    }
    
    .sidebar-heading {
        color: #7bed9f;
        font-size: 0.95rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 14px;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    .attack-dir-banner {
        background: rgba(16, 38, 27, 0.7);
        border: 1px solid rgba(46, 213, 115, 0.25);
        border-radius: 8px;
        padding: 8px 16px;
        text-align: center;
        color: #7bed9f;
        font-size: 0.88rem;
        font-weight: 700;
        letter-spacing: 1px;
        margin-top: 8px;
        margin-bottom: 18px;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #13241b;
        border: 1px solid rgba(46, 213, 115, 0.2);
        border-radius: 8px;
        color: #d1d5db;
        padding: 8px 18px;
        font-weight: 700;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #e30613, #ff4757) !important;
        color: #ffffff !important;
        border-color: #ff4757 !important;
    }
</style>
""", unsafe_allow_html=True)


# ==============================================================================
# 1. SESSION STATE MANAGEMENT
# ==============================================================================
if "secilen_oyuncu" not in st.session_state:
    st.session_state.secilen_oyuncu = None


# ==============================================================================
# DATA LOADING
# ==============================================================================
@st.cache_data
def load_match_data():
    file_path = "besiktas_mac_verisi.csv"
    if not os.path.exists(file_path):
        st.error(f"Data file '{file_path}' not found!")
        return pd.DataFrame()
    return pd.read_csv(file_path)

df_all = load_match_data()
if df_all.empty:
    st.stop()

# Official Beşiktaş Matchday Squad with Exact Jersey Numbers
STARTING_XI = [
    {"name": "Alexander Nübel", "pos": "GK", "no": 1},
    {"name": "Amir Murillo", "pos": "DF", "no": 62},
    {"name": "Tiago Djaló", "pos": "DF", "no": 35},
    {"name": "Emirhan Topçu", "pos": "DF", "no": 53},
    {"name": "Rıdvan Yılmaz", "pos": "DF", "no": 33},
    {"name": "Salih Özcan", "pos": "MF", "no": 6},
    {"name": "Junior Olaitan", "pos": "MF", "no": 15},
    {"name": "Orkun Kökçü", "pos": "MF", "no": 10},
    {"name": "Václav Černý", "pos": "MF", "no": 18},
    {"name": "Leandro Trossard", "pos": "FW", "no": 19},
    {"name": "Hyeon-gyu Oh", "pos": "FW", "no": 9}
]

SUBSTITUTES = [
    {"name": "İlhan Fakılı", "pos": "MF", "no": 29},
    {"name": "Amir Hadžiahmetović", "pos": "MF", "no": 5},
    {"name": "Dušan Vlahović", "pos": "FW", "no": 24},
    {"name": "Milot Rashica", "pos": "FW", "no": 7},
    {"name": "Kassoum Ouattara", "pos": "DF", "no": 11},
    {"name": "Doğan Alemdar", "pos": "GK", "no": 80},
    {"name": "Emmanuel Agbadou", "pos": "DF", "no": 12},
    {"name": "Taylan Bulut", "pos": "DF", "no": 22},
    {"name": "Yasin Özcan", "pos": "DF", "no": 58},
    {"name": "Wilfred Ndidi", "pos": "MF", "no": 4},
    {"name": "Kartal Kayra Yılmaz", "pos": "MF", "no": 8},
    {"name": "Semih Kılıçsoy", "pos": "FW", "no": 90}
]


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
    
    # Substitutes
    st.markdown("<div class='sidebar-heading'>🔄 SUBSTITUTES</div>", unsafe_allow_html=True)
    for player in SUBSTITUTES:
        p_name = player["name"]
        p_no = player["no"]
        p_pos = player["pos"]
        
        btn_label = f"#{p_no} {p_name} ({p_pos})"
        if st.session_state.secilen_oyuncu == p_name:
            btn_label = f"🔥 🔴 #{p_no} {p_name}"
            
        if st.button(btn_label, key=f"btn_sub_{p_name}", use_container_width=True):
            st.session_state.secilen_oyuncu = p_name
            st.rerun()


# ==============================================================================
# 3. MAIN DASHBOARD CONTENT
# ==============================================================================

# ------------------------------------------------------------------------------
# CASE A: TEAM OVERVIEW (secilen_oyuncu is None)
# ------------------------------------------------------------------------------
if st.session_state.secilen_oyuncu is None:
    # Responsive Scoreboard Banner
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
        st.metric(label="⚽ TOTAL PASSES", value="620", delta="89% Passing Accuracy")
    with col4:
        st.metric(label="🚩 CORNER KICKS", value="15", delta="20+ Key Chances")
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Team Pitch Control Tabs: Heatmap & Team Passing Vectors
    st.markdown("### 🏟️ Match Dominance & Tactical Visualizations")
    team_tab1, team_tab2 = st.tabs(["🔥 Spatial Heatmap & Pressure Zones", "🎯 Team Passing Network & Vectors"])
    
    bjk_events = df_all[df_all["takim"] == "Beşiktaş JK"]
    
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
        fig, ax = pitch.draw(figsize=(12, 7.5))
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
            fontsize=15,
            color='#ffffff',
            fontweight='bold',
            pad=12
        )
        p_col1, p_col2, p_col3 = st.columns([1, 10, 1])
        with p_col2:
            st.pyplot(fig, use_container_width=True)
        plt.close(fig)

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
        fig_pass, ax_pass = pitch_pass.draw(figsize=(12, 7.5))
        fig_pass.patch.set_facecolor('#09160f')
        
        passes_df = bjk_events[bjk_events["aksiyon_turu"].str.contains("Pass", case=False, na=False)]
        comp_passes = passes_df[passes_df["basarili"] == True]
        incomp_passes = passes_df[passes_df["basarili"] == False]
        
        # Draw incompleted passes (red arrows)
        if not incomp_passes.empty:
            pitch_pass.arrows(
                incomp_passes["x"], incomp_passes["y"],
                incomp_passes["end_x"], incomp_passes["end_y"],
                ax=ax_pass,
                color='#ff4757',
                width=1.5,
                headwidth=3.5,
                headlength=3.5,
                alpha=0.45,
                label='Incompleted Pass',
                zorder=2
            )
            
        # Draw completed passes (emerald/bright green arrows)
        if not comp_passes.empty:
            pitch_pass.arrows(
                comp_passes["x"], comp_passes["y"],
                comp_passes["end_x"], comp_passes["end_y"],
                ax=ax_pass,
                color='#2ed573',
                width=2.0,
                headwidth=4.0,
                headlength=4.0,
                alpha=0.75,
                label='Accurate / Completed Pass',
                zorder=3
            )
            
        ax_pass.set_title(
            f"Beşiktaş JK - Match Passing Flow ({len(comp_passes)} Completed / {len(passes_df)} Total Passes • 89% Precision)",
            fontsize=14,
            color='#ffffff',
            fontweight='bold',
            pad=12
        )
        ax_pass.legend(facecolor='#0d1e15', edgecolor='#2ed573', labelcolor='white', loc='upper left', fontsize=10)
        
        p_col1, p_col2, p_col3 = st.columns([1, 10, 1])
        with p_col2:
            st.pyplot(fig_pass, use_container_width=True)
        plt.close(fig_pass)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Team Bottom Visualizations
    g_col1, g_col2 = st.columns(2)
    with g_col1:
        st.markdown("#### ⚡ Team Action Breakdown")
        team_action_counts = bjk_events["aksiyon_turu"].value_counts().reset_index()
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
            plot_bgcolor="rgba(16, 38, 27, 0.75)",
            paper_bgcolor="rgba(16, 38, 27, 0.75)",
            font_color="#ffffff",
            xaxis=dict(showgrid=False, title=""),
            yaxis=dict(showgrid=True, gridcolor="rgba(46, 213, 115, 0.15)", title="Actions", range=[0, max_action * 1.25]),
            coloraxis_showscale=False,
            margin=dict(l=20, r=20, t=30, b=20),
            height=340
        )
        st.plotly_chart(fig_team_bar, use_container_width=True)
        
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
            {"Min": "82'", "Key Moment": "🔄 Tactical Sub: Rıdvan Yılmaz ➡️ Kassoum Ouattara", "Score": "3 - 0"},
            {"Min": "90'", "Key Moment": "🏁 FULL TIME: Dominant 3-0 Victory", "Score": "3 - 0"}
        ])
        st.dataframe(incidents_data, use_container_width=True, hide_index=True)


# ------------------------------------------------------------------------------
# CASE B: PLAYER DETAIL VIEW (secilen_oyuncu is not None)
# ------------------------------------------------------------------------------
else:
    secilen = st.session_state.secilen_oyuncu
    df_oyuncu = df_all[df_all["player_name"] == secilen].copy()
    if df_oyuncu.empty:
        df_oyuncu = df_all[df_all["oyuncu_adi"] == secilen].copy()
    
    pos = df_oyuncu["position"].iloc[0] if "position" in df_oyuncu.columns else (df_oyuncu["mevki"].iloc[0] if not df_oyuncu.empty else "MF")
    opta_pts = df_oyuncu["opta_points"].iloc[0] if not df_oyuncu.empty else 6.00
    jersey_no = df_oyuncu["jersey_number"].iloc[0] if "jersey_number" in df_oyuncu.columns else (df_oyuncu["forma_no"].iloc[0] if not df_oyuncu.empty else "")
    mins_played = df_oyuncu["minutes_played"].iloc[0] if "minutes_played" in df_oyuncu.columns else 90
    sub_status = df_oyuncu["sub_info"].iloc[0] if "sub_info" in df_oyuncu.columns else ("Starter" if mins_played > 60 else "Sub")
    
    # Player Spotlight Scoreboard Box
    st.markdown(f"""
    <div class="scoreboard-box">
        <div class="league-badge">⭐ Player Spotlight • Match Performance</div>
        <div class="scoreboard-grid">
            <div class="team-col-left">
                <div class="team-title-text">#{jersey_no} {secilen.upper()}</div>
                <div class="team-scorers">Position: <strong>{pos}</strong> &nbsp;•&nbsp; ⏱️ <strong>{mins_played} Minutes Played</strong> ({sub_status})</div>
            </div>
            <div>
                <div class="score-center-badge" style="border-color: #2ed573; box-shadow: 0 0 25px rgba(46, 213, 115, 0.45); font-size: 2.8rem;">
                    {opta_pts:.2f} <span style="font-size: 1.1rem; color: #7bed9f;">PTS</span>
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
    
    # Player Metrics Calculations
    passes = df_oyuncu[df_oyuncu["aksiyon_turu"].str.contains("Pass", case=False, na=False)]
    total_passes = len(passes)
    accurate_passes = int(passes["basarili_pas"].sum()) if "basarili_pas" in passes.columns else int(total_passes * 0.89)
    inaccurate_passes = max(0, total_passes - accurate_passes)
    pass_acc = (accurate_passes / total_passes * 100) if total_passes > 0 else 0.0
    
    total_actions = len(df_oyuncu)
    successful_actions = int((df_oyuncu["basarili"] == True).sum()) if "basarili" in df_oyuncu.columns else total_actions
    shots_count = len(df_oyuncu[df_oyuncu["aksiyon_turu"].str.contains("Shot", case=False, na=False)])
    defensive_count = len(df_oyuncu[df_oyuncu["aksiyon_turu"].str.contains("Tackle|Interception", case=False, na=False)])
    chances_count = len(df_oyuncu[df_oyuncu["aksiyon_turu"].str.contains("Chance", case=False, na=False)])
    
    # Individual KPI Cards (5 Columns with Minutes Played)
    kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
    with kpi1:
        st.metric(
            label="⭐ OPTA RATING",
            value=f"{opta_pts:.2f}",
            delta="🌟 MVP" if opta_pts >= 9.5 else ("🔥 Masterclass" if opta_pts >= 8.0 else "Solid")
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
            label="⚡ TOTAL ACTIONS",
            value=f"{successful_actions}",
            delta=f"{total_actions} Total Events"
        )
    with kpi5:
        st.metric(
            label="🛡️ DEFENSE / SHOTS",
            value=f"{defensive_count} / {shots_count}",
            delta=f"{chances_count} Key Chances" if chances_count > 0 else f"{shots_count} Shots"
        )
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Player Visualizations: Heatmap & Accurate Passing Map
    st.markdown(f"### 🏟️ #{jersey_no} {secilen} - Tactical Spatial Maps")
    tab_p1, tab_p2 = st.tabs(["🔥 Spatial Activity & Touch Heatmap", "🎯 Accurate Passing Map & Vectors"])
    
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
        fig_indiv, ax_indiv = pitch_indiv.draw(figsize=(12, 7.5))
        fig_indiv.patch.set_facecolor('#09160f')
        
        px_coords = df_oyuncu['x'].dropna()
        py_coords = df_oyuncu['y'].dropna()
        
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
            fontsize=15,
            color='#ffffff',
            fontweight='bold',
            pad=12
        )
        p_col1, p_col2, p_col3 = st.columns([1, 10, 1])
        with p_col2:
            st.pyplot(fig_indiv, use_container_width=True)
        plt.close(fig_indiv)

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
        fig_p_pass, ax_p_pass = pitch_p_pass.draw(figsize=(12, 7.5))
        fig_p_pass.patch.set_facecolor('#09160f')
        
        p_comp = passes[passes["basarili"] == True]
        p_incomp = passes[passes["basarili"] == False]
        
        # Incompleted passes (red arrows)
        if not p_incomp.empty:
            pitch_p_pass.arrows(
                p_incomp["x"], p_incomp["y"],
                p_incomp["end_x"], p_incomp["end_y"],
                ax=ax_p_pass,
                color='#ff4757',
                width=1.6,
                headwidth=3.8,
                headlength=3.8,
                alpha=0.45,
                label=f'Incompleted Pass ({len(p_incomp)})',
                zorder=2
            )
            
        # Completed passes (bright emerald green arrows)
        if not p_comp.empty:
            pitch_p_pass.arrows(
                p_comp["x"], p_comp["y"],
                p_comp["end_x"], p_comp["end_y"],
                ax=ax_p_pass,
                color='#2ed573',
                width=2.2,
                headwidth=4.2,
                headlength=4.2,
                alpha=0.82,
                label=f'Accurate / Completed Pass ({len(p_comp)})',
                zorder=3
            )
            
        ax_p_pass.set_title(
            f"#{jersey_no} {secilen} - Accurate Passing Map ({accurate_passes} Completed / {total_passes} Total • {pass_acc:.1f}% Accuracy)",
            fontsize=14,
            color='#ffffff',
            fontweight='bold',
            pad=12
        )
        ax_p_pass.legend(facecolor='#0d1e15', edgecolor='#2ed573', labelcolor='white', loc='upper left', fontsize=10)
        
        p_col1, p_col2, p_col3 = st.columns([1, 10, 1])
        with p_col2:
            st.pyplot(fig_p_pass, use_container_width=True)
        plt.close(fig_p_pass)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Individual Charts
    p_graf1, p_graf2 = st.columns(2)
    
    with p_graf1:
        st.markdown("#### 📊 Action Distribution")
        p_act = df_oyuncu["aksiyon_turu"].value_counts().reset_index()
        p_act.columns = ["Action Type", "Count"]
        max_p_act = p_act["Count"].max() if not p_act.empty else 50
        
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
            plot_bgcolor="rgba(16, 38, 27, 0.75)",
            paper_bgcolor="rgba(16, 38, 27, 0.75)",
            font_color="#ffffff",
            xaxis=dict(showgrid=False, title=""),
            yaxis=dict(showgrid=True, gridcolor="rgba(46, 213, 115, 0.15)", title="Count", range=[0, max_p_act * 1.25]),
            coloraxis_showscale=False,
            margin=dict(l=20, r=20, t=30, b=20),
            height=340
        )
        st.plotly_chart(fig_bar, use_container_width=True)
        
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
                textfont_size=13,
                textfont_color=['#000000', '#ffffff'],
                marker=dict(line=dict(color='#0d1a13', width=2))
            )
            fig_pie.update_layout(
                plot_bgcolor="rgba(16, 38, 27, 0.75)",
                paper_bgcolor="rgba(16, 38, 27, 0.75)",
                font_color="#ffffff",
                legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5),
                margin=dict(l=20, r=20, t=30, b=20),
                height=340
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("No registered pass actions for this player in this match.")

    # 100% English Detailed Event Logs Expander
    with st.expander(f"📋 Detailed Event Logs for #{jersey_no} {secilen} ({mins_played} Minutes Played)"):
        # Format columns in 100% English
        table_df = df_oyuncu.copy()
        
        display_cols = {
            "player_name": "Player Name",
            "jersey_number": "Jersey #",
            "position": "Position",
            "minutes_played": "Minutes Played",
            "action_type": "Action Type",
            "outcome": "Outcome",
            "x": "Pitch Start X",
            "y": "Pitch Start Y",
            "end_x": "Pitch End X",
            "end_y": "Pitch End Y",
            "opta_points": "Opta Rating"
        }
        
        # Fallback mappings if old columns exist
        for col in ["player_name", "jersey_number", "position", "minutes_played", "action_type", "outcome", "x", "y", "end_x", "end_y", "opta_points"]:
            if col not in table_df.columns:
                if col == "player_name" and "oyuncu_adi" in table_df.columns:
                    table_df["player_name"] = table_df["oyuncu_adi"]
                elif col == "jersey_number" and "forma_no" in table_df.columns:
                    table_df["jersey_number"] = table_df["forma_no"]
                elif col == "position" and "mevki" in table_df.columns:
                    table_df["position"] = table_df["mevki"]
                elif col == "action_type" and "aksiyon_turu" in table_df.columns:
                    table_df["action_type"] = table_df["aksiyon_turu"]
                elif col == "outcome" and "basarili" in table_df.columns:
                    table_df["outcome"] = table_df["basarili"].apply(lambda x: "Successful" if x else "Unsuccessful")
                elif col == "minutes_played":
                    table_df["minutes_played"] = mins_played
                elif col in ["end_x", "end_y"]:
                    table_df[col] = table_df["x" if col == "end_x" else "y"]

        present_cols = [c for c in display_cols.keys() if c in table_df.columns]
        english_table = table_df[present_cols].rename(columns=display_cols)
        
        st.dataframe(
            english_table,
            use_container_width=True,
            hide_index=True
        )

st.markdown("---")
st.caption("⚽ 2026 Beşiktaş JK Matchday Intelligence • Powered by Streamlit & mplsoccer")
