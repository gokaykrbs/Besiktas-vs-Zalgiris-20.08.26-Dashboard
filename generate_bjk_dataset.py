import pandas as pd
import numpy as np

np.random.seed(1903)

# Official Beşiktaş Matchday Squad Roster
bjk_players_roster = [
    # --- STARTING XI ---
    {"player_name": "Alexander Nübel", "pos": "GK", "no": 1, "is_sub": False, "opta_points": 7.20, "minutes": 90, "sub_info": "Starter (Full 90')", "passes": 24, "shots": 0, "tackles": 0, "inter": 1, "chances": 0, "fouls_won": 0, "cx": 12, "cy": 40, "sx": 6, "sy": 14, "shot_events": []},
    {"player_name": "Amir Murillo", "pos": "DF", "no": 62, "is_sub": False, "opta_points": 8.22, "minutes": 90, "sub_info": "Starter (Full 90') ⚽ (12')", "passes": 53, "shots": 2, "tackles": 0, "inter": 0, "chances": 3, "fouls_won": 3, "cx": 68, "cy": 68, "sx": 20, "sy": 10,
     "shot_events": [
         {"x": 108.5, "y": 44.2, "end_x": 120.0, "end_y": 41.5, "outcome": "Goal ⚽ (12')", "xg": 0.45, "body_part": "Right Foot", "desc": "Goal: Precision finish into bottom corner"},
         {"x": 96.0, "y": 55.0, "end_x": 118.0, "end_y": 48.0, "outcome": "Blocked Shot", "xg": 0.08, "body_part": "Right Foot", "desc": "Blocked by defending center-back"}
     ]},
    {"player_name": "Tiago Djaló", "pos": "DF", "no": 35, "is_sub": False, "opta_points": 7.80, "minutes": 90, "sub_info": "Starter (Full 90')", "passes": 95, "shots": 1, "tackles": 0, "inter": 1, "chances": 0, "fouls_won": 0, "cx": 46, "cy": 52, "sx": 16, "sy": 14,
     "shot_events": [
         {"x": 109.0, "y": 38.5, "end_x": 119.5, "end_y": 46.0, "outcome": "Blocked Shot", "xg": 0.12, "body_part": "Header", "desc": "Corner header attempt blocked"}
     ]},
    {"player_name": "Emirhan Topçu", "pos": "DF", "no": 53, "is_sub": False, "opta_points": 9.54, "minutes": 90, "sub_info": "Starter (Full 90') ⭐ (9.54)", "passes": 105, "shots": 3, "tackles": 3, "inter": 3, "chances": 2, "fouls_won": 0, "cx": 48, "cy": 28, "sx": 16, "sy": 14,
     "shot_events": [
         {"x": 111.0, "y": 39.0, "end_x": 120.0, "end_y": 42.0, "outcome": "Shot on Target", "xg": 0.28, "body_part": "Header", "desc": "Powerful header saved by goalkeeper"},
         {"x": 92.0, "y": 32.0, "end_x": 120.0, "end_y": 32.0, "outcome": "Shot off Target", "xg": 0.06, "body_part": "Left Foot", "desc": "Long range effort wide left"},
         {"x": 106.0, "y": 45.0, "end_x": 116.0, "end_y": 43.0, "outcome": "Blocked Shot", "xg": 0.10, "body_part": "Left Foot", "desc": "Box scramble blocked"}
     ]},
    {"player_name": "Rıdvan Yılmaz", "pos": "DF", "no": 33, "is_sub": False, "opta_points": 8.40, "minutes": 81, "sub_info": "Starter (Sub off 82') 🅰️🅰️ (2 Ast)", "passes": 51, "shots": 0, "tackles": 1, "inter": 0, "chances": 14, "fouls_won": 2, "cx": 72, "cy": 12, "sx": 22, "sy": 10, "shot_events": []},
    {"player_name": "Salih Özcan", "pos": "MF", "no": 6, "is_sub": False, "opta_points": 8.30, "minutes": 90, "sub_info": "Starter (Full 90')", "passes": 85, "shots": 1, "tackles": 2, "inter": 2, "chances": 0, "fouls_won": 1, "cx": 60, "cy": 42, "sx": 18, "sy": 18,
     "shot_events": [
         {"x": 94.0, "y": 42.0, "end_x": 120.0, "end_y": 47.0, "outcome": "Shot off Target", "xg": 0.05, "body_part": "Right Foot", "desc": "Long range shot over the crossbar"}
     ]},
    {"player_name": "Junior Olaitan", "pos": "MF", "no": 15, "is_sub": False, "opta_points": 6.62, "minutes": 60, "sub_info": "Starter (Sub off 61')", "passes": 36, "shots": 1, "tackles": 0, "inter": 0, "chances": 0, "fouls_won": 0, "cx": 75, "cy": 64, "sx": 18, "sy": 15,
     "shot_events": [
         {"x": 102.0, "y": 52.0, "end_x": 120.0, "end_y": 38.5, "outcome": "Shot on Target", "xg": 0.18, "body_part": "Right Foot", "desc": "Curling effort saved by GK"}
     ]},
    {"player_name": "Orkun Kökçü", "pos": "MF", "no": 10, "is_sub": False, "opta_points": 10.00, "minutes": 90, "sub_info": "Starter (Full 90') ⚽ (60') 🌟 MVP", "passes": 89, "shots": 4, "tackles": 2, "inter": 0, "chances": 11, "fouls_won": 1, "cx": 78, "cy": 38, "sx": 20, "sy": 20,
     "shot_events": [
         {"x": 108.0, "y": 40.0, "end_x": 120.0, "end_y": 37.8, "outcome": "Goal ⚽ (60')", "xg": 0.78, "body_part": "Penalty (Right Foot)", "desc": "Penalty Goal: Ice-cold finish into side netting"},
         {"x": 95.0, "y": 36.0, "end_x": 120.0, "end_y": 41.0, "outcome": "Shot on Target", "xg": 0.14, "body_part": "Right Foot", "desc": "Direct free kick on target"},
         {"x": 98.5, "y": 44.0, "end_x": 116.0, "end_y": 42.0, "outcome": "Blocked Shot", "xg": 0.09, "body_part": "Right Foot", "desc": "Edge of penalty area shot blocked"},
         {"x": 102.0, "y": 30.0, "end_x": 117.0, "end_y": 34.0, "outcome": "Blocked Shot", "xg": 0.08, "body_part": "Left Foot", "desc": "Deflected shot for corner kick"}
     ]},
    {"player_name": "Václav Černý", "pos": "MF", "no": 18, "is_sub": False, "opta_points": 6.85, "minutes": 45, "sub_info": "Starter (Sub off 46')", "passes": 24, "shots": 1, "tackles": 1, "inter": 0, "chances": 1, "fouls_won": 0, "cx": 82, "cy": 68, "sx": 18, "sy": 14,
     "shot_events": [
         {"x": 104.0, "y": 62.0, "end_x": 120.0, "end_y": 34.0, "outcome": "Shot off Target", "xg": 0.11, "body_part": "Left Foot", "desc": "Cut-inside shot missed far post"}
     ]},
    {"player_name": "Leandro Trossard", "pos": "FW", "no": 19, "is_sub": False, "opta_points": 6.94, "minutes": 72, "sub_info": "Starter (Sub off 73')", "passes": 51, "shots": 1, "tackles": 0, "inter": 0, "chances": 1, "fouls_won": 3, "cx": 84, "cy": 22, "sx": 18, "sy": 15,
     "shot_events": [
         {"x": 105.0, "y": 24.0, "end_x": 120.0, "end_y": 48.0, "outcome": "Shot off Target", "xg": 0.12, "body_part": "Right Foot", "desc": "Curling winger shot past the post"}
     ]},
    {"player_name": "Hyeon-gyu Oh", "pos": "FW", "no": 9, "is_sub": False, "opta_points": 8.42, "minutes": 60, "sub_info": "Starter (Sub off 61') ⚽ (6')", "passes": 11, "shots": 4, "tackles": 0, "inter": 0, "chances": 0, "fouls_won": 3, "cx": 98, "cy": 40, "sx": 14, "sy": 16,
     "shot_events": [
         {"x": 112.0, "y": 38.0, "end_x": 120.0, "end_y": 39.5, "outcome": "Goal ⚽ (6')", "xg": 0.52, "body_part": "Right Foot", "desc": "Goal: Clinical box strike into the roof of the net"},
         {"x": 109.0, "y": 42.0, "end_x": 120.0, "end_y": 40.0, "outcome": "Shot on Target", "xg": 0.31, "body_part": "Header", "desc": "Header saved by goalkeeper"},
         {"x": 105.0, "y": 35.0, "end_x": 120.0, "end_y": 32.0, "outcome": "Shot off Target", "xg": 0.16, "body_part": "Right Foot", "desc": "Volley just over the bar"},
         {"x": 101.0, "y": 46.0, "end_x": 114.0, "end_y": 43.0, "outcome": "Blocked Shot", "xg": 0.09, "body_part": "Left Foot", "desc": "Turn and shoot blocked by defender"}
     ]},
    
    # --- SUBSTITUTES ---
    {"player_name": "İlhan Fakılı", "pos": "MF", "no": 29, "is_sub": True, "opta_points": 6.70, "minutes": 45, "sub_info": "Sub (46' in)", "passes": 28, "shots": 1, "tackles": 1, "inter": 1, "chances": 1, "fouls_won": 1, "cx": 80, "cy": 65, "sx": 16, "sy": 14,
     "shot_events": [
         {"x": 98.0, "y": 60.0, "end_x": 120.0, "end_y": 43.0, "outcome": "Shot on Target", "xg": 0.10, "body_part": "Right Foot", "desc": "Low drive saved at near post"}
     ]},
    {"player_name": "Amir Hadžiahmetović", "pos": "MF", "no": 5, "is_sub": True, "opta_points": 6.80, "minutes": 30, "sub_info": "Sub (61' in)", "passes": 32, "shots": 0, "tackles": 1, "inter": 1, "chances": 1, "fouls_won": 0, "cx": 65, "cy": 45, "sx": 16, "sy": 16, "shot_events": []},
    {"player_name": "Dušan Vlahović", "pos": "FW", "no": 24, "is_sub": True, "opta_points": 6.90, "minutes": 30, "sub_info": "Sub (61' in)", "passes": 8, "shots": 2, "tackles": 0, "inter": 0, "chances": 1, "fouls_won": 1, "cx": 102, "cy": 42, "sx": 12, "sy": 15,
     "shot_events": [
         {"x": 107.0, "y": 38.0, "end_x": 120.0, "end_y": 41.0, "outcome": "Shot on Target", "xg": 0.35, "body_part": "Left Foot", "desc": "Powerful strike tipped over by GK"},
         {"x": 96.0, "y": 48.0, "end_x": 120.0, "end_y": 50.0, "outcome": "Shot off Target", "xg": 0.08, "body_part": "Left Foot", "desc": "Left-footed strike wide"}
     ]},
    {"player_name": "Milot Rashica", "pos": "FW", "no": 7, "is_sub": True, "opta_points": 6.60, "minutes": 18, "sub_info": "Sub (73' in)", "passes": 14, "shots": 1, "tackles": 0, "inter": 0, "chances": 1, "fouls_won": 0, "cx": 85, "cy": 20, "sx": 15, "sy": 12,
     "shot_events": [
         {"x": 103.0, "y": 26.0, "end_x": 115.0, "end_y": 35.0, "outcome": "Blocked Shot", "xg": 0.07, "body_part": "Right Foot", "desc": "Fast break attempt blocked"}
     ]},
    {"player_name": "Kassoum Ouattara", "pos": "DF", "no": 11, "is_sub": True, "opta_points": 6.40, "minutes": 9, "sub_info": "Sub (82' in)", "passes": 10, "shots": 0, "tackles": 1, "inter": 0, "chances": 0, "fouls_won": 0, "cx": 68, "cy": 14, "sx": 15, "sy": 10, "shot_events": []},
    {"player_name": "Doğan Alemdar", "pos": "GK", "no": 80, "is_sub": True, "opta_points": np.nan, "minutes": 0, "sub_info": "Unused Sub (0')", "passes": 0, "shots": 0, "tackles": 0, "inter": 0, "chances": 0, "fouls_won": 0, "cx": 10, "cy": 40, "sx": 4, "sy": 10, "shot_events": []},
    {"player_name": "Emmanuel Agbadou", "pos": "DF", "no": 12, "is_sub": True, "opta_points": np.nan, "minutes": 0, "sub_info": "Unused Sub (0')", "passes": 0, "shots": 0, "tackles": 0, "inter": 0, "chances": 0, "fouls_won": 0, "cx": 45, "cy": 35, "sx": 10, "sy": 10, "shot_events": []},
    {"player_name": "Taylan Bulut", "pos": "DF", "no": 22, "is_sub": True, "opta_points": np.nan, "minutes": 0, "sub_info": "Unused Sub (0')", "passes": 0, "shots": 0, "tackles": 0, "inter": 0, "chances": 0, "fouls_won": 0, "cx": 55, "cy": 65, "sx": 10, "sy": 10, "shot_events": []},
    {"player_name": "Yasin Özcan", "pos": "DF", "no": 58, "is_sub": True, "opta_points": np.nan, "minutes": 0, "sub_info": "Unused Sub (0')", "passes": 0, "shots": 0, "tackles": 0, "inter": 0, "chances": 0, "fouls_won": 0, "cx": 50, "cy": 20, "sx": 10, "sy": 10, "shot_events": []},
    {"player_name": "Wilfred Ndidi", "pos": "MF", "no": 4, "is_sub": True, "opta_points": np.nan, "minutes": 0, "sub_info": "Unused Sub (0')", "passes": 0, "shots": 0, "tackles": 0, "inter": 0, "chances": 0, "fouls_won": 0, "cx": 58, "cy": 40, "sx": 10, "sy": 10, "shot_events": []},
    {"player_name": "Kartal Kayra Yılmaz", "pos": "MF", "no": 8, "is_sub": True, "opta_points": np.nan, "minutes": 0, "sub_info": "Unused Sub (0')", "passes": 0, "shots": 0, "tackles": 0, "inter": 0, "chances": 0, "fouls_won": 0, "cx": 62, "cy": 45, "sx": 10, "sy": 10, "shot_events": []},
    {"player_name": "Semih Kılıçsoy", "pos": "FW", "no": 90, "is_sub": True, "opta_points": np.nan, "minutes": 0, "sub_info": "Unused Sub (0')", "passes": 0, "shots": 0, "tackles": 0, "inter": 0, "chances": 0, "fouls_won": 0, "cx": 95, "cy": 45, "sx": 10, "sy": 10, "shot_events": []}
]

all_events = []
for p in bjk_players_roster:
    name = p["player_name"]
    pos = p["pos"]
    no = p["no"]
    pts = p["opta_points"]
    mins = p["minutes"]
    sub_info = p["sub_info"]
    cx, cy, sx, sy = p["cx"], p["cy"], p["sx"], p["sy"]
    
    # Exclude unused substitutes (0 minutes) from on-pitch match actions
    if mins == 0:
        continue
    
    # Passes with Start (x, y) and Destination (end_x, end_y)
    for _ in range(p["passes"]):
        px = np.clip(np.random.normal(cx, sx), 4, 116)
        py = np.clip(np.random.normal(cy, sy), 4, 76)
        
        pass_len = np.random.uniform(12, 35)
        angle = np.random.normal(0.2, 0.7)
        end_x = np.clip(px + pass_len * np.cos(angle), 2, 118)
        end_y = np.clip(py + pass_len * np.sin(angle), 2, 78)
        
        is_succ = np.random.rand() < 0.89
        all_events.append({
            "player_name": name,
            "jersey_number": no,
            "team": "Beşiktaş JK",
            "position": pos,
            "is_substitute": p["is_sub"],
            "minutes_played": mins,
            "sub_info": sub_info,
            "action_type": "Pass",
            "x": round(float(px), 2),
            "y": round(float(py), 2),
            "end_x": round(float(end_x), 2),
            "end_y": round(float(end_y), 2),
            "is_successful": is_succ,
            "outcome": "Completed" if is_succ else "Incompleted",
            "shot_xg": 0.0,
            "shot_detail": "Pass",
            "opta_points": pts
        })
        
    # Real Match Shot Events
    for s in p.get("shot_events", []):
        all_events.append({
            "player_name": name,
            "jersey_number": no,
            "team": "Beşiktaş JK",
            "position": pos,
            "is_substitute": p["is_sub"],
            "minutes_played": mins,
            "sub_info": sub_info,
            "action_type": "Shot",
            "x": round(float(s["x"]), 2),
            "y": round(float(s["y"]), 2),
            "end_x": round(float(s["end_x"]), 2),
            "end_y": round(float(s["end_y"]), 2),
            "is_successful": "Goal" in s["outcome"] or "Target" in s["outcome"],
            "outcome": s["outcome"],
            "shot_xg": s["xg"],
            "shot_detail": f"{s['outcome']} ({s['body_part']} • xG: {s['xg']:.2f})",
            "opta_points": pts
        })
        
    # Tackles
    for _ in range(p["tackles"]):
        tx = np.clip(np.random.normal(cx * 0.9, sx), 10, 110)
        ty = np.clip(np.random.normal(cy, sy), 5, 75)
        all_events.append({
            "player_name": name,
            "jersey_number": no,
            "team": "Beşiktaş JK",
            "position": pos,
            "is_substitute": p["is_sub"],
            "minutes_played": mins,
            "sub_info": sub_info,
            "action_type": "Tackle",
            "x": round(float(tx), 2),
            "y": round(float(ty), 2),
            "end_x": round(float(tx + np.random.uniform(-4, 4)), 2),
            "end_y": round(float(ty + np.random.uniform(-4, 4)), 2),
            "is_successful": True,
            "outcome": "Won",
            "shot_xg": 0.0,
            "shot_detail": "Tackle Won",
            "opta_points": pts
        })
        
    # Interceptions
    for _ in range(p["inter"]):
        ix = np.clip(np.random.normal(cx * 0.95, sx), 10, 110)
        iy = np.clip(np.random.normal(cy, sy), 5, 75)
        all_events.append({
            "player_name": name,
            "jersey_number": no,
            "team": "Beşiktaş JK",
            "position": pos,
            "is_substitute": p["is_sub"],
            "minutes_played": mins,
            "sub_info": sub_info,
            "action_type": "Interception",
            "x": round(float(ix), 2),
            "y": round(float(iy), 2),
            "end_x": round(float(ix + np.random.uniform(5, 12)), 2),
            "end_y": round(float(iy + np.random.uniform(-6, 6)), 2),
            "is_successful": True,
            "outcome": "Intercepted",
            "shot_xg": 0.0,
            "shot_detail": "Ball Intercepted",
            "opta_points": pts
        })
        
    # Chances Created
    for _ in range(p["chances"]):
        ch_x = np.clip(np.random.normal(92, 10), 75, 115)
        ch_y = np.clip(np.random.normal(40, 18), 12, 68)
        end_x = np.clip(np.random.normal(106, 6), 95, 118)
        end_y = np.clip(np.random.normal(40, 8), 24, 56)
        all_events.append({
            "player_name": name,
            "jersey_number": no,
            "team": "Beşiktaş JK",
            "position": pos,
            "is_substitute": p["is_sub"],
            "minutes_played": mins,
            "sub_info": sub_info,
            "action_type": "Chance Created",
            "x": round(float(ch_x), 2),
            "y": round(float(ch_y), 2),
            "end_x": round(float(end_x), 2),
            "end_y": round(float(end_y), 2),
            "is_successful": True,
            "outcome": "Key Pass Delivered",
            "shot_xg": 0.0,
            "shot_detail": "Key Pass",
            "opta_points": pts
        })
        
    # Fouls Won
    for _ in range(p["fouls_won"]):
        fx = np.clip(np.random.normal(cx, sx), 15, 110)
        fy = np.clip(np.random.normal(cy, sy), 5, 75)
        all_events.append({
            "player_name": name,
            "jersey_number": no,
            "team": "Beşiktaş JK",
            "position": pos,
            "is_substitute": p["is_sub"],
            "minutes_played": mins,
            "sub_info": sub_info,
            "action_type": "Foul Won",
            "x": round(float(fx), 2),
            "y": round(float(fy), 2),
            "end_x": round(float(fx), 2),
            "end_y": round(float(fy), 2),
            "is_successful": True,
            "outcome": "Free Kick Awarded",
            "shot_xg": 0.0,
            "shot_detail": "Foul Drawn",
            "opta_points": pts
        })

df_bjk = pd.DataFrame(all_events)
# Compatibility columns
df_bjk["oyuncu_adi"] = df_bjk["player_name"]
df_bjk["aksiyon_turu"] = df_bjk["action_type"]
df_bjk["takim"] = df_bjk["team"]
df_bjk["mevki"] = df_bjk["position"]
df_bjk["forma_no"] = df_bjk["jersey_number"]
df_bjk["basarili"] = df_bjk["is_successful"]
df_bjk["basarili_pas"] = df_bjk["is_successful"].apply(lambda x: 1 if x else 0)

df_bjk.to_csv("besiktas_mac_verisi.csv", index=False, encoding="utf-8-sig")
print(f"Dataset regenerated with detailed shot events ({len(df_bjk)} records). Total shots: {len(df_bjk[df_bjk['action_type']=='Shot'])}")
