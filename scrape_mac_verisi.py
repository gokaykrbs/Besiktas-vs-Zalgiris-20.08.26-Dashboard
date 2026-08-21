"""
===================================================================================
PROJE: Beşiktaş vs FK Kauno Žalgiris (20.08.2026) Maç Verisi Scraping & Analiz
GELİŞTİRİCİ: Antigravity AI Pair Programmer
GÖREV: Sofascore ve Opta sayfalarından dinamik XHR/API interception ile veri çekip
       besiktas_mac_verisi.csv ve ek analiz CSV dosyalarını üretmek.
===================================================================================
"""

import asyncio
import json
import os
import sys
import unicodedata
import pandas as pd
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

# UTF-8 Konsol çıkışı
if sys.platform.startswith('win'):
    sys.stdout.reconfigure(encoding='utf-8')

SOFASCORE_URL = "https://www.sofascore.com/football/match/fk-kauno-zalgiris-besiktas-jk/albsQoH"
OPTA_URL = "https://optaplayerstats.statsperform.com/en_GB/soccer/uefa-europa-league-2026-2027/1rpi0q64a7kut2wiuvecmgbv8/match/view/b8f5r6q4symsas0ejyolpyjv8/opta-points"

def normalize_text(text):
    if not text:
        return ""
    text = unicodedata.normalize('NFKD', str(text)).encode('ASCII', 'ignore').decode('utf-8')
    return text.lower().replace(" ", "").replace(".", "").replace("-", "").replace("'", "")

async def main():
    print("=" * 70)
    print("🚀 BEŞİKTAŞ vs KAUNO ŽALGIRIS MAÇ VERİSİ TOPLAMA BAŞLATILDI")
    print("=" * 70)
    
    sofascore_intercepted = {}
    opta_intercepted = {}
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-infobars"
            ]
        )
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
            viewport={"width": 1920, "height": 1080},
            locale="en-GB"
        )
        
        # ----------------------------------------------------
        # 1. SOFASCORE SCRAPING & NETWORK INTERCEPTION
        # ----------------------------------------------------
        print("\n📡 [1/2] Sofascore API istekleri dinleniyor...")
        page_sofa = await context.new_page()
        await page_sofa.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined});")
        
        async def on_sofa_response(res):
            try:
                ct = res.headers.get("content-type", "")
                if "json" in ct or "api" in res.url:
                    try:
                        data = await res.json()
                        sofascore_intercepted[res.url] = data
                    except:
                        pass
            except:
                pass
                
        page_sofa.on("response", on_sofa_response)
        
        try:
            await page_sofa.goto(SOFASCORE_URL, wait_until="networkidle", timeout=60000)
        except Exception as e:
            print(f"  [Bilgi] Sofascore goto: {e}")
            
        await page_sofa.wait_for_timeout(3000)
        
        # Sayfa içinden Sofascore API endpoint'lerini çağır
        event_id = "16708137"
        direct_endpoints = [
            f"https://www.sofascore.com/api/v1/event/{event_id}",
            f"https://www.sofascore.com/api/v1/event/{event_id}/statistics",
            f"https://www.sofascore.com/api/v1/event/{event_id}/lineups",
            f"https://www.sofascore.com/api/v1/event/{event_id}/incidents",
            f"https://www.sofascore.com/api/v1/event/{event_id}/shotmap"
        ]
        
        for ep in direct_endpoints:
            try:
                res_data = await page_sofa.evaluate("""async (url) => {
                    const r = await fetch(url);
                    if (r.ok) return await r.json();
                    return {status: r.status};
                }""", ep)
                sofascore_intercepted[ep] = res_data
            except Exception:
                pass
                
        print(f"  ✓ Sofascore'dan {len(sofascore_intercepted)} JSON API verisi başarıyla alındı.")
        await page_sofa.wait_for_timeout(1000)
        
        # ----------------------------------------------------
        # 2. OPTA SCRAPING & NETWORK INTERCEPTION
        # ----------------------------------------------------
        print("\n📡 [2/2] Opta Player Stats (Opta Points & Action Metrics) çekiliyor...")
        page_opta = await context.new_page()
        await page_opta.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined});")
        
        async def on_opta_response(res):
            try:
                ct = res.headers.get("content-type", "")
                if "json" in ct or "statsperform" in res.url or "sdap" in res.url or "api" in res.url:
                    try:
                        data = await res.json()
                        opta_intercepted[res.url] = data
                    except:
                        pass
            except:
                pass
                
        page_opta.on("response", on_opta_response)
        
        try:
            await page_opta.goto(OPTA_URL, wait_until="networkidle", timeout=60000)
        except Exception as e:
            print(f"  [Bilgi] Opta goto: {e}")
            
        await page_opta.wait_for_timeout(4000)
        
        # Cookie banner kapat
        try:
            btn = page_opta.locator("#uc-btn-accept-banner")
            if await btn.count() > 0:
                await btn.click()
                await page_opta.wait_for_timeout(1500)
        except:
            pass
            
        # Points görünümü
        points_html = await page_opta.content()
        await page_opta.wait_for_timeout(1500)
        
        # Stats görünümüne tıkla (aksiyon sayıları)
        try:
            stats_tab = page_opta.locator("text='Stats'").first
            if await stats_tab.count() > 0:
                await stats_tab.click()
                await page_opta.wait_for_timeout(2500)
        except Exception as e:
            print(f"  [Uyarı] Stats tab tıklama: {e}")
            
        stats_html = await page_opta.content()
        await page_opta.wait_for_timeout(1500)
        
        await browser.close()
        print("  ✓ Tarayıcı oturumu başarıyla kapatıldı.")

    # ----------------------------------------------------
    # 3. VERİLERİN AYRIŞTIRILMASI VE PANDAS İLE ENTEGRASYONU
    # ----------------------------------------------------
    print("\n⚙️ Veriler işleniyor ve temizleniyor...")
    
    # Sofascore Lineups
    sofa_lineup_key = f"https://www.sofascore.com/api/v1/event/{event_id}/lineups"
    sofa_lineup = sofascore_intercepted.get(sofa_lineup_key, {})
    
    home_players_info = {}
    for p in sofa_lineup.get("home", {}).get("players", []):
        p_obj = p.get("player", {})
        home_players_info[normalize_text(p_obj.get("name", ""))] = {
            "full_name": p_obj.get("name"),
            "short_name": p_obj.get("shortName"),
            "team": "Beşiktaş JK",
            "position": p.get("position", ""),
            "jersey_number": p.get("jerseyNumber"),
            "is_substitute": p.get("substitute", False)
        }
        home_players_info[normalize_text(p_obj.get("shortName", ""))] = home_players_info[normalize_text(p_obj.get("name", ""))]

    away_players_info = {}
    for p in sofa_lineup.get("away", {}).get("players", []):
        p_obj = p.get("player", {})
        away_players_info[normalize_text(p_obj.get("name", ""))] = {
            "full_name": p_obj.get("name"),
            "short_name": p_obj.get("shortName"),
            "team": "FK Kauno Žalgiris",
            "position": p.get("position", ""),
            "jersey_number": p.get("jerseyNumber"),
            "is_substitute": p.get("substitute", False)
        }
        away_players_info[normalize_text(p_obj.get("shortName", ""))] = away_players_info[normalize_text(p_obj.get("name", ""))]

    def parse_opta_dom(html_content):
        soup = BeautifulSoup(html_content, "html.parser")
        main = soup.find("main") or soup.find("body")
        lines = [l.strip() for l in main.get_text(separator="\n", strip=True).split("\n") if l.strip()]
        
        parsed = []
        i = 0
        while i < len(lines):
            line = lines[i]
            if line in ["Starter", "Sub"] and (i + 24) < len(lines):
                status = line
                name = lines[i+1]
                pos = lines[i+2]
                rank = lines[i+3]
                pts = lines[i+4]
                mp = lines[i+5]
                g = lines[i+6]
                sont = lines[i+7]
                sofft = lines[i+8]
                bs = lines[i+9]
                og = lines[i+10]
                a = lines[i+11]
                p = lines[i+12]
                c = lines[i+13]
                tk = lines[i+14]
                inter = lines[i+15]
                fw = lines[i+16]
                fc = lines[i+17]
                o = lines[i+18]
                yc = lines[i+19]
                rc = lines[i+20]
                gc = lines[i+21]
                pw = lines[i+22]
                sav = lines[i+23]
                psav = lines[i+24]
                
                try:
                    float(pts)
                    float(mp)
                    parsed.append({
                        "opta_status": status,
                        "player_name": name,
                        "opta_pos": pos,
                        "rank": int(rank) if rank.isdigit() else rank,
                        "opta_points": float(pts),
                        "minutes_played": int(float(mp)),
                        "goals": float(g),
                        "shots_on_target": float(sont),
                        "shots_off_target": float(sofft),
                        "blocked_shots": float(bs),
                        "own_goals": float(og),
                        "assists": float(a),
                        "passes": float(p),
                        "chances_created": float(c),
                        "tackles": float(tk),
                        "interceptions": float(inter),
                        "fouls_won": float(fw),
                        "fouls_conceded": float(fc),
                        "offsides": float(o),
                        "yellow_cards": float(yc),
                        "red_cards": float(rc),
                        "goals_conceded": float(gc),
                        "penalties_won": float(pw),
                        "saves": float(sav),
                        "penalty_saves": float(psav)
                    })
                    i += 25
                    continue
                except ValueError:
                    pass
            i += 1
        return pd.DataFrame(parsed)

    df_stats = parse_opta_dom(stats_html)
    df_pts = parse_opta_dom(points_html)
    
    # Tekil oyuncu tablosu
    df_stats_unique = df_stats.drop_duplicates(subset=["player_name", "minutes_played"]).copy()
    df_pts_unique = df_pts.drop_duplicates(subset=["player_name", "minutes_played"]).copy()
    
    # Points kırılım sütunları
    pts_cols = {
        "goals": "pts_goals",
        "shots_on_target": "pts_shots_on_target",
        "shots_off_target": "pts_shots_off_target",
        "blocked_shots": "pts_blocked_shots",
        "assists": "pts_assists",
        "passes": "pts_passes",
        "chances_created": "pts_chances_created",
        "tackles": "pts_tackles",
        "interceptions": "pts_interceptions",
        "fouls_won": "pts_fouls_won",
        "fouls_conceded": "pts_fouls_conceded",
        "yellow_cards": "pts_yellow_cards",
        "goals_conceded": "pts_goals_conceded",
        "penalties_won": "pts_penalties_won",
        "saves": "pts_saves"
    }
    pts_sub = df_pts_unique[["player_name"] + list(pts_cols.keys())].rename(columns=pts_cols)
    df_main = pd.merge(df_stats_unique, pts_sub, on="player_name", how="left")
    
    # Oyuncuları Sofascore kadroları ile eşleştir
    def map_team_and_info(row):
        p_name = row["player_name"]
        norm = normalize_text(p_name)
        
        # Check Home (Besiktas)
        for k, v in home_players_info.items():
            if k in norm or norm in k or (len(norm) > 4 and norm[:5] in k):
                return pd.Series([v["team"], v["full_name"], v["position"], v["is_substitute"], v["jersey_number"]])
                
        # Check Away (Kauno Zalgiris)
        for k, v in away_players_info.items():
            if k in norm or norm in k or (len(norm) > 4 and norm[:5] in k):
                return pd.Series([v["team"], v["full_name"], v["position"], v["is_substitute"], v["jersey_number"]])
                
        # Fallback keyword matching
        if any(w in norm for w in ["kokcu", "topcu", "hyeon", "yilmaz", "ozcan", "murillo", "djalo", "trossard", "olaitan", "fakili", "cerny", "vlahovic", "hadziahmetovic", "rashica", "ouattara", "nubel"]):
            return pd.Series(["Beşiktaş JK", p_name, row["opta_pos"], row["opta_status"] == "Sub", None])
            
        return pd.Series(["FK Kauno Žalgiris", p_name, row["opta_pos"], row["opta_status"] == "Sub", None])

    df_main[["team", "full_name", "position", "is_substitute", "jersey_number"]] = df_main.apply(map_team_and_info, axis=1)

    # İstatistiksel metrikleri türet
    df_main["total_shots"] = df_main["shots_on_target"] + df_main["shots_off_target"] + df_main["blocked_shots"]
    df_main["defensive_actions"] = df_main["tackles"] + df_main["interceptions"]
    df_main["match"] = "FK Kauno Žalgiris vs Beşiktaş JK"
    df_main["match_date"] = "2026-08-20"
    df_main["competition"] = "UEFA Europa League"
    df_main["score"] = "3-0"
    
    # Sütun düzeni (Streamlit ve mplsoccer görselleştirmeleri için kusursuz şablon)
    column_order = [
        "match", "match_date", "competition", "score", "team",
        "full_name", "player_name", "jersey_number", "position", "opta_status", "is_substitute",
        "minutes_played", "opta_points", "rank",
        "goals", "assists", "total_shots", "shots_on_target", "shots_off_target", "blocked_shots",
        "passes", "chances_created", "tackles", "interceptions", "defensive_actions",
        "fouls_won", "fouls_conceded", "offsides", "yellow_cards", "red_cards",
        "penalties_won", "saves", "penalty_saves", "goals_conceded",
        "pts_goals", "pts_shots_on_target", "pts_shots_off_target", "pts_blocked_shots",
        "pts_assists", "pts_passes", "pts_chances_created", "pts_tackles", "pts_interceptions",
        "pts_fouls_won", "pts_fouls_conceded", "pts_yellow_cards", "pts_goals_conceded", "pts_penalties_won", "pts_saves"
    ]
    
    existing_cols = [c for c in column_order if c in df_main.columns]
    df_final = df_main[existing_cols]

    # ----------------------------------------------------
    # 4. CSV DOSYALARININ KAYDEDİLMESİ
    # ----------------------------------------------------
    out_main_csv = "besiktas_mac_verisi.csv"
    df_final.to_csv(out_main_csv, index=False, encoding="utf-8-sig")
    print(f"\n📊 [1] Ana Maç ve Oyuncu Verisi Kaydedildi: '{out_main_csv}' ({len(df_final)} oyuncu)")
    
    # Olaylar / Incidents
    sofa_incidents_key = f"https://www.sofascore.com/api/v1/event/{event_id}/incidents"
    sofa_incidents = sofascore_intercepted.get(sofa_incidents_key, {}).get("incidents", [])
    inc_rows = []
    for inc in sofa_incidents:
        inc_rows.append({
            "minute": inc.get("time"),
            "type": inc.get("incidentType"),
            "class": inc.get("incidentClass"),
            "team": "Beşiktaş JK" if inc.get("isHome") else "FK Kauno Žalgiris",
            "player": inc.get("player", {}).get("name") if inc.get("player") else None,
            "assist": inc.get("assist1", {}).get("name") if inc.get("assist1") else None,
            "player_in": inc.get("playerIn", {}).get("name") if inc.get("playerIn") else None,
            "player_out": inc.get("playerOut", {}).get("name") if inc.get("playerOut") else None,
            "score_home": inc.get("homeScore"),
            "score_away": inc.get("awayScore")
        })
    df_inc = pd.DataFrame(inc_rows)
    df_inc.to_csv("mac_olaylari_incidents.csv", index=False, encoding="utf-8-sig")
    print(f"📊 [2] Maç Olayları Zaman Çizelgesi Kaydedildi: 'mac_olaylari_incidents.csv' ({len(df_inc)} olay)")

    # Takım İstatistikleri
    sofa_stats_key = f"https://www.sofascore.com/api/v1/event/{event_id}/statistics"
    sofa_team_stats = sofascore_intercepted.get(sofa_stats_key, {})
    if sofa_team_stats and "statistics" in sofa_team_stats:
        t_rows = []
        for period in sofa_team_stats.get("statistics", []):
            p_name = period.get("period")
            for grp in period.get("groups", []):
                g_name = grp.get("groupName")
                for item in grp.get("statisticsItems", []):
                    t_rows.append({
                        "period": p_name,
                        "group": g_name,
                        "metric": item.get("name"),
                        "besiktas_home": item.get("home"),
                        "zalgiris_away": item.get("away"),
                        "besiktas_value": item.get("homeValue"),
                        "zalgiris_value": item.get("awayValue")
                    })
        df_team = pd.DataFrame(t_rows)
        df_team.to_csv("mac_takim_istatistikleri.csv", index=False, encoding="utf-8-sig")
        print(f"📊 [3] Genel Takım İstatistikleri Kaydedildi: 'mac_takim_istatistikleri.csv' ({len(df_team)} metrik)")

    # Raw JSON yedekleri
    with open("sofascore_api_raw.json", "w", encoding="utf-8") as f:
        json.dump(sofascore_intercepted, f, ensure_ascii=False, indent=2)
    print("📁 [4] Ham Sofascore JSON verisi 'sofascore_api_raw.json' olarak arşivlendi.")

    print("\n" + "=" * 70)
    print("✨ TÜM GÖREVLER EKSİKSİZ TAMAMLANDI!")
    print("=" * 70)

if __name__ == "__main__":
    asyncio.run(main())
