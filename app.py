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
    page_title="Beşiktaş JK - Matchday Analytics Live",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# HIGH-ENERGY STADIUM & BROADCAST THEME (CSS)
# ==============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,300;0,500;0,700;0,900;1,700&family=Teko:wght@500;700&display=swap');

    /* Global Atmosphere */
    .stApp {
        background: radial-gradient(circle at 50% 10%, #132219 0%, #0a110e 55%, #050807 100%);
        color: #ffffff;
        font-family: 'Montserrat', sans-serif;
    }
    
    /* Live Broadcast Match Scoreboard Header */
    .scoreboard-banner {
        background: linear-gradient(135deg, rgba(16, 37, 26, 0.9) 0%, rgba(20, 20, 25, 0.95) 50%, rgba(180, 10, 25, 0.85) 100%);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 16px;
        padding: 24px 30px;
        margin-bottom: 25px;
        box-shadow: 0 10px 35px rgba(0, 0, 0, 0.6), inset 0 1px 0 rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(16px);
        position: relative;
        overflow: hidden;
    }
    
    .scoreboard-banner::before {
        content: "";
        position: absolute;
        top: -50%;
        right: -20%;
        width: 300px;
        height: 300px;
        background: radial-gradient(circle, rgba(227, 6, 19, 0.25) 0%, transparent 70%);
        pointer-events: none;
    }
    
    .match-league-tag {
        display: inline-block;
        background: linear-gradient(90deg, #e30613, #ff414d);
        color: #ffffff;
        font-size: 0.8rem;
        font-weight: 800;
        padding: 4px 14px;
        border-radius: 20px;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        box-shadow: 0 0 15px rgba(227, 6, 19, 0.5);
        margin-bottom: 12px;
    }
    
    .scoreboard-content {
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 15px;
    }
    
    .team-name-big {
        font-family: 'Teko', sans-serif;
        font-size: 2.8rem;
        font-weight: 700;
        letter-spacing: 1px;
        color: #ffffff;
        margin: 0;
        line-height: 1;
        text-shadow: 0 0 20px rgba(255, 255, 255, 0.2);
    }
    
    .score-badge {
        font-family: 'Teko', sans-serif;
        font-size: 3.5rem;
        font-weight: 700;
        color: #ffffff;
        background: rgba(0, 0, 0, 0.6);
        padding: 4px 28px;
        border-radius: 12px;
        border: 2px solid #e30613;
        box-shadow: 0 0 25px rgba(227, 6, 19, 0.6);
        letter-spacing: 6px;
        line-height: 1;
    }
    
    .match-subtext {
        color: #a3b899;
        font-size: 0.95rem;
        margin-top: 8px;
        font-weight: 500;
    }
    
    /* Vibrant Holographic Metric Cards */
    div[data-testid="stMetric"] {
        background: linear-gradient(145deg, rgba(21, 38, 29, 0.85), rgba(12, 20, 16, 0.95));
        border: 1px solid rgba(46, 213, 115, 0.25);
        border-radius: 14px;
        padding: 16px 20px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.4), inset 0 0 15px rgba(46, 213, 115, 0.05);
        backdrop-filter: blur(10px);
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    
    div[data-testid="stMetric"]:hover {
        transform: translateY(-4px) scale(1.02);
        border-color: #ff4757;
        box-shadow: 0 12px 30px rgba(227, 6, 19, 0.4);
    }
    
    div[data-testid="stMetricLabel"] > div {
        color: #7bed9f !important;
        font-size: 0.85rem !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    div[data-testid="stMetricValue"] > div {
        color: #ffffff !important;
        font-size: 2.2rem !important;
        font-weight: 900 !important;
        font-family: 'Teko', sans-serif;
        letter-spacing: 1px;
    }
    
    div[data-testid="stMetricDelta"] > div {
        font-weight: 600 !important;
    }
    
    /* Sidebar Atmosphere */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d1a13 0%, #070e0a 100%);
        border-right: 1px solid rgba(46, 213, 115, 0.2);
    }
    
    section[data-testid="stSidebar"] .stButton button {
        background: linear-gradient(90deg, #13241b 0%, #192e23 100%);
        color: #e2f0d9;
        border: 1px solid rgba(46, 213, 115, 0.2);
        border-radius: 10px;
        padding: 9px 14px;
        font-weight: 600;
        text-align: left;
        font-size: 0.88rem;
        transition: all 0.25s ease;
        box-shadow: 0 3px 8px rgba(0,0,0,0.3);
    }
    
    section[data-testid="stSidebar"] .stButton button:hover {
        background: linear-gradient(90deg, #e30613 0%, #ff4757 100%) !important;
        color: #ffffff !important;
        border-color: #ff6b81 !important;
        transform: translateX(6px);
        box-shadow: 0 0 18px rgba(227, 6, 19, 0.6) !important;
    }
    
    .section-title {
        color: #7bed9f;
        font-size: 1.15rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 1px;
        display: flex;
        align-items: center;
        gap: 8px;
        margin-top: 15px;
        margin-bottom: 10px;
    }

    /* Pitch Container Glass Card */
    .pitch-card {
        background: rgba(14, 25, 19, 0.7);
        border: 1px solid rgba(46, 213, 115, 0.2);
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
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

# Squad Definitions
STARTING_XI = [
    {"name": "Alexander Nübel", "pos": "GK", "no": 1, "role": "Goalkeeper"},
    {"name": "Amir Murillo", "pos": "DF", "no": 62, "role": "Right Back ⚽ (12')"},
    {"name": "Tiago Djaló", "pos": "DF", "no": 3, "role": "Center Back"},
    {"name": "Emirhan Topçu", "pos": "DF", "no": 14, "role": "Center Back ⭐ (9.54)"},
    {"name": "Rıdvan Yılmaz", "pos": "DF", "no": 33, "role": "Left Back 🅰️🅰️ (2 Ast)"},
    {"name": "Salih Özcan", "pos": "MF", "no": 6, "role": "Defensive Midfield"},
    {"name": "Junior Olaitan", "pos": "MF", "no": 10, "role": "Central Midfield"},
    {"name": "Orkun Kökçü", "pos": "MF", "no": 8, "role": "Playmaker ⚽ (60') 🌟 10.0"},
    {"name": "Václav Černý", "pos": "MF", "no": 18, "role": "Right Winger"},
    {"name": "Leandro Trossard", "pos": "FW", "no": 19, "role": "Left Winger"},
    {"name": "Hyeon-gyu Oh", "pos": "FW", "no": 9, "role": "Striker ⚽ (6')"}
]

SUBSTITUTES = [
    {"name": "İlhan Fakılı", "pos": "MF", "no": 29, "role": "Sub (46')"},
    {"name": "Amir Hadžiahmetović", "pos": "MF", "no": 88, "role": "Sub (61')"},
    {"name": "Dušan Vlahović", "pos": "FW", "no": 99, "role": "Sub (61')"},
    {"name": "Milot Rashica", "pos": "FW", "no": 7, "role": "Sub (73')"},
    {"name": "Kassoum Ouattara", "pos": "DF", "no": 24, "role": "Sub (82')"},
    {"name": "Doğan Alemdar", "pos": "GK", "no": 96, "role": "Sub GK"},
    {"name": "Emmanuel Agbadou", "pos": "DF", "no": 5, "role": "Sub DF"},
    {"name": "Taylan Bulut", "pos": "DF", "no": 2, "role": "Sub DF"},
    {"name": "Yasin Özcan", "pos": "DF", "no": 27, "role": "Sub DF"},
    {"name": "Wilfred Ndidi", "pos": "MF", "no": 25, "role": "Sub MF"},
    {"name": "Semih Kılıçsoy", "pos": "FW", "no": 90, "role": "Sub FW"}
]


# ==============================================================================
# 2. SIDEBAR - SQUAD NAVIGATION
# ==============================================================================
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/2/20/Logo_of_Besiktas_JK.svg", width=85)
    st.markdown("## 🦅 **BEŞİKTAŞ JK**")
    st.markdown("🔥 **MATCHDAY SQUAD**")
    
    # Return to Team Stats Button
    if st.button("🏟️ 🦅 **FULL TEAM OVERVIEW**", use_container_width=True):
        st.session_state.secilen_oyuncu = None
        st.rerun()

    st.markdown("---")
    
    # Starting XI
    st.markdown("<div class='section-title'>⚡ STARTING XI</div>", unsafe_allow_html=True)
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
    st.markdown("<div class='section-title'>🔄 BENCH & SUBS</div>", unsafe_allow_html=True)
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
# 3. MAIN DASHBOARD DISPLAY
# ==============================================================================

# ------------------------------------------------------------------------------
# CASE A: TEAM OVERVIEW (secilen_oyuncu is None)
# ------------------------------------------------------------------------------
if st.session_state.secilen_oyuncu is None:
    # High-Impact Broadcast Scoreboard Header
    st.markdown("""
    <div class="scoreboard-banner">
        <div class="match-league-tag">🏆 UEFA Europa League • Full Time</div>
        <div class="scoreboard-content">
            <div>
                <div class="team-name-big">🦅 BEŞİKTAŞ JK</div>
                <div style="color: #7bed9f; font-weight: 700; font-size: 0.9rem;">⚽ H. Oh 6' &nbsp;|&nbsp; ⚽ A. Murillo 12' &nbsp;|&nbsp; ⚽ O. Kökçü (P) 60'</div>
            </div>
            <div class="score-badge">3 - 0</div>
            <div style="text-align: right;">
                <div class="team-name-big" style="color: #94a3b8;">FK KAUNO ŽALGIRIS</div>
                <div style="color: #64748b; font-size: 0.9rem;">Clean Sheet Victory</div>
            </div>
        </div>
        <div class="match-subtext">🏟️ Tüpraş Stadium, Istanbul &nbsp;•&nbsp; 👥 Attendance: 31,494 &nbsp;•&nbsp; ⚖️ Referee: Tobias Stieler</div>
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
        st.metric(label="🚩 CORNER KICKS", value="15", delta="20+ Key Chances Created")
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Full Team Pitch Control Heatmap
    st.markdown("### 🏟️ Live Match Spatial Dominance & Pressure Map")
    
    # Realistic Emerald Green Stadium Grass Pitch
    pitch = Pitch(
        pitch_type='statsbomb',
        pitch_color='#0f3622',
        line_color='#ffffff',
        line_zorder=2,
        linewidth=1.8,
        goal_type='box'
    )
    
    fig, ax = pitch.draw(figsize=(12, 7.8))
    fig.patch.set_facecolor('#0a1a11')
    
    bjk_events = df_all[df_all["takim"] == "Beşiktaş JK"]
    x_all = bjk_events["x"].dropna()
    y_all = bjk_events["y"].dropna()
    
    if len(x_all) > 10:
        # Blazing Fire/Magma KDE Heatmap
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
        # Tactical ball-touch action points
        pitch.scatter(
            x_all, y_all,
            ax=ax,
            s=30,
            c='#ffffff',
            edgecolors='#e30613',
            alpha=0.55,
            zorder=3
        )
        
    ax.set_title(
        "🦅 Beşiktaş JK - 90-Minute High-Intensity Territorial Control & Heatmap",
        fontsize=16,
        color='#ffffff',
        fontweight='bold',
        pad=15
    )
    
    # Attack Direction Indicator
    pitch.arrows(
        15, -4, 105, -4,
        ax=ax,
        color='#7bed9f',
        width=2.5,
        headwidth=5,
        headlength=5,
        zorder=4
    )
    ax.text(60, -7, "ATTACKING DIRECTION ➡️", color='#7bed9f', fontsize=11, fontweight='bold', ha='center')
    
    p_col1, p_col2, p_col3 = st.columns([1, 10, 1])
    with p_col2:
        st.pyplot(fig, use_container_width=True)
    plt.close(fig)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Bottom Visualizations: Action Breakdown & Timeline
    g_col1, g_col2 = st.columns(2)
    with g_col1:
        st.markdown("#### ⚡ Team Action Breakdown")
        team_action_counts = bjk_events["aksiyon_turu"].value_counts().reset_index()
        team_action_counts.columns = ["Action Type", "Count"]
        
        # High Energy Neon Theme Bar Chart
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
            plot_bgcolor="rgba(16, 36, 26, 0.7)",
            paper_bgcolor="rgba(16, 36, 26, 0.7)",
            font_color="#ffffff",
            xaxis=dict(showgrid=False, title=""),
            yaxis=dict(showgrid=True, gridcolor="rgba(46, 213, 115, 0.15)", title="Actions"),
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
    df_oyuncu = df_all[df_all["oyuncu_adi"] == secilen].copy()
    
    pos = df_oyuncu["mevki"].iloc[0] if not df_oyuncu.empty else "MF"
    opta_pts = df_oyuncu["opta_points"].iloc[0] if not df_oyuncu.empty else 6.00
    jersey_no = df_oyuncu["forma_no"].iloc[0] if "forma_no" in df_oyuncu.columns else ""
    
    # Player Header Banner
    st.markdown(f"""
    <div class="scoreboard-banner">
        <div class="match-league-tag">⭐ Player Spotlight • UEFA Europa League</div>
        <div class="scoreboard-content">
            <div>
                <div class="team-name-big">#{jersey_no} {secilen.upper()}</div>
                <div style="color: #7bed9f; font-weight: 700; font-size: 1.05rem;">Position: {pos} &nbsp;|&nbsp; 🦅 Beşiktaş JK</div>
            </div>
            <div class="score-badge" style="font-size: 2.8rem; border-color: #2ed573; box-shadow: 0 0 25px rgba(46, 213, 115, 0.5);">
                {opta_pts:.2f} <span style="font-size: 1.2rem; color: #7bed9f;">PTS</span>
            </div>
        </div>
        <div class="match-subtext">Individual Matchday Performance & Tactical Analysis</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Calculations
    passes = df_oyuncu[df_oyuncu["aksiyon_turu"].str.contains("Pass", case=False, na=False)]
    total_passes = len(passes)
    accurate_passes = int(passes["basarili_pas"].sum()) if "basarili_pas" in passes.columns else int(total_passes * 0.89)
    inaccurate_passes = max(0, total_passes - accurate_passes)
    pass_acc = (accurate_passes / total_passes * 100) if total_passes > 0 else 0.0
    
    total_actions = len(df_oyuncu)
    successful_actions = int((df_oyuncu["basarili"] == True).sum()) if "basarili" in df_oyuncu.columns else total_actions
    shots_count = len(df_oyuncu[df_oyuncu["aksiyon_turu"].str.contains("Shot", case=False, na=False)])
    defensive_count = len(df_oyuncu[df_oyuncu["aksiyon_turu"].str.contains("Tackle|Interception", case=False, na=False)])
    
    # Individual KPI Cards
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    with kpi1:
        st.metric(
            label="⭐ OPTA MATCH RATING",
            value=f"{opta_pts:.2f}",
            delta="🌟 Man of the Match" if opta_pts >= 9.5 else ("🔥 Masterclass" if opta_pts >= 8.0 else "Solid Performance")
        )
    with kpi2:
        st.metric(
            label="🎯 PASS ACCURACY",
            value=f"{accurate_passes} / {total_passes}",
            delta=f"{pass_acc:.1f}% Precision" if total_passes > 0 else "No Passes"
        )
    with kpi3:
        st.metric(
            label="⚡ TOTAL ACTIONS",
            value=f"{successful_actions}",
            delta=f"Total: {total_actions} Events"
        )
    with kpi4:
        st.metric(
            label="🛡️ DEFENSE / SHOTS",
            value=f"{defensive_count} / {shots_count}",
            delta=f"{shots_count} Shots on Goal" if shots_count > 0 else f"{defensive_count} Ball Recoveries"
        )
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Individual Player Heatmap
    st.markdown(f"### 🏟️ #{jersey_no} {secilen} - Tactical Touch Zones & Heatmap")
    
    pitch = Pitch(
        pitch_type='statsbomb',
        pitch_color='#0f3622',
        line_color='#ffffff',
        line_zorder=2,
        linewidth=1.8,
        goal_type='box'
    )
    
    fig, ax = pitch.draw(figsize=(12, 7.8))
    fig.patch.set_facecolor('#0a1a11')
    
    px_coords = df_oyuncu['x'].dropna()
    py_coords = df_oyuncu['y'].dropna()
    
    if len(px_coords) >= 4:
        sns.kdeplot(
            x=px_coords,
            y=py_coords,
            ax=ax,
            fill=True,
            cmap='YlOrRd',
            levels=65,
            thresh=0.04,
            alpha=0.75,
            zorder=1
        )
        pitch.scatter(
            px_coords, py_coords,
            ax=ax,
            s=55,
            c='#ffffff',
            edgecolors='#e30613',
            alpha=0.8,
            zorder=3,
            label='Action Point'
        )
    else:
        pitch.scatter(
            px_coords, py_coords,
            ax=ax,
            s=95,
            c='#ff4757',
            edgecolors='#ffffff',
            alpha=0.9,
            zorder=3
        )
        
    ax.set_title(
        f"#{jersey_no} {secilen} ({pos}) - Pitch Influence & Ball Contact Heatmap",
        fontsize=16,
        color='#ffffff',
        fontweight='bold',
        pad=15
    )
    
    # Attack Indicator
    pitch.arrows(
        15, -4, 105, -4,
        ax=ax,
        color='#7bed9f',
        width=2.5,
        headwidth=5,
        headlength=5,
        zorder=4
    )
    ax.text(60, -7, "ATTACKING DIRECTION ➡️", color='#7bed9f', fontsize=11, fontweight='bold', ha='center')
    
    p_col1, p_col2, p_col3 = st.columns([1, 10, 1])
    with p_col2:
        st.pyplot(fig, use_container_width=True)
    plt.close(fig)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Individual Charts
    p_graf1, p_graf2 = st.columns(2)
    
    with p_graf1:
        st.markdown("#### 📊 Action Distribution")
        p_act = df_oyuncu["aksiyon_turu"].value_counts().reset_index()
        p_act.columns = ["Action Type", "Count"]
        
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
            plot_bgcolor="rgba(16, 36, 26, 0.7)",
            paper_bgcolor="rgba(16, 36, 26, 0.7)",
            font_color="#ffffff",
            xaxis=dict(showgrid=False, title=""),
            yaxis=dict(showgrid=True, gridcolor="rgba(46, 213, 115, 0.15)", title="Count"),
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
                plot_bgcolor="rgba(16, 36, 26, 0.7)",
                paper_bgcolor="rgba(16, 36, 26, 0.7)",
                font_color="#ffffff",
                legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5),
                margin=dict(l=20, r=20, t=30, b=20),
                height=340
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("No registered pass actions for this player in this match.")

    # Raw Data Expander
    with st.expander(f"📋 Detailed Event Logs for #{jersey_no} {secilen}"):
        st.dataframe(
            df_oyuncu[["oyuncu_adi", "aksiyon_turu", "x", "y", "basarili", "opta_points"]],
            use_container_width=True,
            hide_index=True
        )

st.markdown("---")
st.caption("⚽ 2026 Beşiktaş JK Matchday Intelligence • Powered by Streamlit & mplsoccer")
