# 🦅 Beşiktaş JK vs FK Kauno Žalgiris - Match Performance Analytics Dashboard

An interactive **Master-Detail** football analytics dashboard built with **Streamlit**, **mplsoccer**, and **Plotly** to visualize player performances, spatial pitch heatmaps (KDE plots), action distributions, and match key events from the UEFA Europa League fixture between **Beşiktaş JK (3)** and **FK Kauno Žalgiris (0)** (20 August 2026).

---

## 🌟 Key Features

- **Master-Detail Interactive Navigation:**
  - Dynamic squad sidebar separating **Starting XI** and **Substitutes**.
  - Single-click player transition updating session state seamlessly without dropdown reloads.
  - Quick-switch **"Team Overview & Stats"** button to return to whole-team metrics.
- **Team-Level Match Analytics (Master View):**
  - High-level KPIs: Possession (77%), Total Shots (21), Accurate Passes (620 / 89%), Corners (15).
  - 90-Minute whole-team spatial pressure & territorial dominance heatmap rendered with `mplsoccer.Pitch`.
  - Match timeline with goal scorers, assists, cards, and tactical substitutions.
  - Team action type distribution chart.
- **Individual Player Analytics (Detail View):**
  - Individual **Opta Rating / Points**, accurate passes, total actions, defensive contributions, and shots.
  - Exclusive high-resolution **KDE Spatial Heatmap** showing touch zones and tactical action points.
  - Action type breakdown bar chart and pass completion rate donut chart in Beşiktaş black-white-red theme.
- **Data Scraping & Interception Engine:**
  - Automated network interception script (`scrape_mac_verisi.py`) extracting match events, lineups, and Opta stats via Playwright.

---

## 📂 Project Structure

```
├── app.py                      # Main interactive Streamlit Master-Detail application
├── scrape_mac_verisi.py        # Playwright network interception and scraper script
├── generate_bjk_dataset.py     # Spatial event coordinates generator
├── besiktas_mac_verisi.csv     # Primary match dataset with event coordinates & stats
├── mac_olaylari_incidents.csv  # Match timeline and incident events (goals, subs, cards)
├── mac_takim_istatistikleri.csv# Team-level summary statistics
├── sofascore_api_raw.json      # Raw JSON API snapshot from match day
└── requirements.txt            # Python dependencies
```

---

## 🚀 Quick Start & Installation

### 1. Clone the repository
```bash
git clone https://github.com/gokaykrbs/Besiktas-vs-Zalgiris-20.08.26-Dashboard.git
cd Besiktas-vs-Zalgiris-20.08.26-Dashboard
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Launch the Dashboard
```bash
streamlit run app.py
```
Open your browser and navigate to `http://localhost:8501`.

---

## 🛠️ Tech Stack

- **Frontend & App Framework:** [Streamlit](https://streamlit.io/)
- **Pitch Visualizations:** [mplsoccer](https://mplsoccer.readthedocs.io/)
- **Charts & Plots:** [Plotly](https://plotly.com/python/), [Matplotlib](https://matplotlib.org/), [Seaborn](https://seaborn.pydata.org/)
- **Data Interception & Automation:** [Playwright Python](https://playwright.dev/python/)
- **Data Processing:** [Pandas](https://pandas.pydata.org/), [NumPy](https://numpy.org/)

---

## 📄 License

MIT License © 2026 [gokaykrbs](https://github.com/gokaykrbs)
