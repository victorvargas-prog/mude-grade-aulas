import base64, json

with open("/home/claude/mude-dashboard/logo_b64.txt") as f:
    logo_b64 = f.read().strip()

logo_src = f"data:image/png;base64,{logo_b64}"

# ── DADOS REAIS EXTRAÍDOS DO PDF ──────────────────────────────────────────────
# Grade semanal RJ · Junho 2026
# Cores do PDF: preto=Riachuelo, roxo=Vivo, amarelo=Porto, vermelho=Premier Pet, branco=Instituto Mude
# Vivo: 3 aulas (2 Mat Pilates Lagoa seg/qua + 1 Yoga Leblon qui) → sp:'direct'
# Demais: projetos incentivados → sp:'incentive'
# Patrocinadores incentivados:
#   Riachuelo: 9 aulas/sem · 22/06/2026–31/12/2026
#   Riachuelo ICMS: 2 aulas/sem · 25/06/2026–31/12/2026
#   Porto: 3 aulas/sem · 06/07/2026–31/12/2026
#   Premier Pet: 2 aulas/sem · 04/07/2026–18/08/2026
# Patrocinador direto:
#   Vivo: 3 aulas/sem · 23/02/2026–31/12/2026

SEED_DATA = [
  # ── SEGUNDA ──────────────────────────────────────────────────────────────────
  {"dia":0,"time":"06:30","name":"Yoga","cat":"yoga","local":"Arpoador - Praça do Arpoador","sp":"incentive","brand":"Riachuelo","instrutor":"Esther Bruno","aud":80},
  {"dia":0,"time":"06:30","name":"Yoga","cat":"yoga","local":"Leblon","sp":"incentive","brand":"Riachuelo","instrutor":"Guga Dale","aud":80},
  {"dia":0,"time":"06:30","name":"Yoga","cat":"yoga","local":"Lagoa","sp":"incentive","brand":"Riachuelo","instrutor":"Ana David","aud":70},
  {"dia":0,"time":"07:30","name":"Beach Workout","cat":"hiit","local":"Arpoador - Posto 4","sp":"incentive","brand":"Riachuelo","instrutor":"Rafaela Matos","aud":60},
  {"dia":0,"time":"08:30","name":"Yoga","cat":"yoga","local":"Lagoa - Platô da Lagoa","sp":"incentive","brand":"Riachuelo","instrutor":"Bianca Coelho","aud":65},
  {"dia":0,"time":"16:00","name":"Mat Pilates","cat":"pilates","local":"Lagoa","sp":"direct","brand":"Vivo","instrutor":"Carol Ivantes","aud":50},
  {"dia":0,"time":"17:00","name":"Yoga","cat":"yoga","local":"Leblon","sp":"incentive","brand":"Riachuelo","instrutor":"Esther Bruno","aud":75},
  {"dia":0,"time":"18:00","name":"Yoga","cat":"yoga","local":"Arpoador - Praça do Arpoador","sp":"incentive","brand":"Riachuelo","instrutor":"Guga Dale","aud":80},
  # ── TERÇA ────────────────────────────────────────────────────────────────────
  {"dia":1,"time":"06:30","name":"Yoga","cat":"yoga","local":"Arpoador","sp":"incentive","brand":"Riachuelo","instrutor":"Guga Dale","aud":80},
  {"dia":1,"time":"06:30","name":"Yoga","cat":"yoga","local":"Lagoa","sp":"incentive","brand":"Riachuelo","instrutor":"Carol Ivantes","aud":70},
  {"dia":1,"time":"07:30","name":"Beach Workout","cat":"hiit","local":"Arpoador - Posto 4","sp":"incentive","brand":"Riachuelo","instrutor":"Mika Choeri","aud":60},
  {"dia":1,"time":"08:30","name":"Yoga","cat":"yoga","local":"Leblon","sp":"incentive","brand":"Riachuelo","instrutor":"Marcela Gorgulho","aud":70},
  {"dia":1,"time":"16:00","name":"HIIT","cat":"hiit","local":"Lagoa","sp":"incentive","brand":"Porto","instrutor":"Rapha Grato","aud":55},
  {"dia":1,"time":"17:00","name":"HIIT","cat":"hiit","local":"Leblon","sp":"incentive","brand":"Riachuelo","instrutor":"Marcela Gorgulho","aud":65},
  {"dia":1,"time":"18:00","name":"Yoga","cat":"yoga","local":"Arpoador - Praça do Arpoador","sp":"incentive","brand":"Riachuelo","instrutor":"Guga Dale","aud":75},
  # ── QUARTA ───────────────────────────────────────────────────────────────────
  {"dia":2,"time":"06:30","name":"Yoga","cat":"yoga","local":"Arpoador - Praça do Arpoador","sp":"incentive","brand":"Riachuelo","instrutor":"Ana David","aud":80},
  {"dia":2,"time":"06:30","name":"Yoga","cat":"yoga","local":"Leblon","sp":"incentive","brand":"Riachuelo","instrutor":"Carol Ivantes","aud":75},
  {"dia":2,"time":"06:30","name":"Yoga","cat":"yoga","local":"Lagoa","sp":"incentive","brand":"Riachuelo","instrutor":"Guga Dale","aud":70},
  {"dia":2,"time":"07:30","name":"HIIT","cat":"hiit","local":"Lagoa","sp":"incentive","brand":"Riachuelo","instrutor":"Telmo","aud":60},
  {"dia":2,"time":"08:30","name":"Mat Pilates","cat":"pilates","local":"Lagoa - Platô da Lagoa","sp":"direct","brand":"Vivo","instrutor":"Victor Menezes","aud":50},
  {"dia":2,"time":"16:00","name":"Mat Pilates","cat":"pilates","local":"Lagoa","sp":"incentive","brand":"Premier Pet","instrutor":"Carol Ivantes","aud":50},
  {"dia":2,"time":"17:00","name":"Yoga","cat":"yoga","local":"Leblon","sp":"incentive","brand":"Riachuelo","instrutor":"Marcela Gorgulho","aud":70},
  {"dia":2,"time":"18:00","name":"Yoga","cat":"yoga","local":"Arpoador - Praça do Arpoador","sp":"incentive","brand":"Riachuelo","instrutor":"Rafa Matos","aud":75},
  # ── QUINTA ───────────────────────────────────────────────────────────────────
  {"dia":3,"time":"06:30","name":"Yoga","cat":"yoga","local":"Arpoador - Praça do Arpoador","sp":"incentive","brand":"Riachuelo","instrutor":"Carol Ivantes","aud":80},
  {"dia":3,"time":"06:30","name":"Yoga","cat":"yoga","local":"Leblon","sp":"direct","brand":"Vivo","instrutor":"Marcela Gorgulho","aud":75},
  {"dia":3,"time":"07:30","name":"Beach Workout","cat":"hiit","local":"Arpoador - Posto 4","sp":"incentive","brand":"Riachuelo","instrutor":"Telmo","aud":60},
  {"dia":3,"time":"08:30","name":"Yoga","cat":"yoga","local":"Lagoa - Platô da Lagoa","sp":"incentive","brand":"Riachuelo","instrutor":"James William","aud":65},
  {"dia":3,"time":"16:00","name":"HIIT","cat":"hiit","local":"Lagoa","sp":"incentive","brand":"Porto","instrutor":"Rapha Grato","aud":55},
  {"dia":3,"time":"16:00","name":"HIIT","cat":"hiit","local":"Leblon","sp":"incentive","brand":"Porto","instrutor":"Victor Menezes","aud":60},
  {"dia":3,"time":"17:00","name":"Yoga","cat":"yoga","local":"Leblon","sp":"incentive","brand":"Riachuelo","instrutor":"Marcela Gorgulho","aud":70},
  {"dia":3,"time":"18:00","name":"Yoga","cat":"yoga","local":"Arpoador - Praça do Arpoador","sp":"incentive","brand":"Riachuelo","instrutor":"Jully Canellas","aud":75},
  # ── SEXTA (tarde OFF) ─────────────────────────────────────────────────────────
  {"dia":4,"time":"06:30","name":"Yoga","cat":"yoga","local":"Leblon","sp":"incentive","brand":"Riachuelo","instrutor":"Marcela Gorgulho","aud":70},
  {"dia":4,"time":"07:30","name":"HIIT","cat":"hiit","local":"Leblon","sp":"incentive","brand":"Riachuelo","instrutor":"Nathalia","aud":55},
  {"dia":4,"time":"08:30","name":"Yoga","cat":"yoga","local":"Lagoa","sp":"incentive","brand":"Riachuelo","instrutor":"Nathalia","aud":60},
  # ── SÁBADO ───────────────────────────────────────────────────────────────────
  {"dia":5,"time":"06:30","name":"Yoga","cat":"yoga","local":"Leblon","sp":"incentive","brand":"Riachuelo","instrutor":"Marcela Gorgulho","aud":90},
  {"dia":5,"time":"07:00","name":"Yoga","cat":"yoga","local":"Recreio","sp":"incentive","brand":"Riachuelo","instrutor":"","aud":60},
  {"dia":5,"time":"07:30","name":"Yoga","cat":"yoga","local":"Leblon","sp":"incentive","brand":"Riachuelo","instrutor":"Dany Langer","aud":85},
  {"dia":5,"time":"08:00","name":"Yoga","cat":"yoga","local":"Engenhão","sp":"incentive","brand":"Riachuelo","instrutor":"","aud":55},
  {"dia":5,"time":"09:00","name":"Yoga","cat":"yoga","local":"Península","sp":"incentive","brand":"Riachuelo","instrutor":"Milena Andrade","aud":50},
  # ── DOMINGO ──────────────────────────────────────────────────────────────────
  {"dia":6,"time":"06:00","name":"Yoga","cat":"yoga","local":"Leblon","sp":"incentive","brand":"Riachuelo","instrutor":"","aud":60},
  {"dia":6,"time":"07:00","name":"Yoga","cat":"yoga","local":"Madureira - Parque","sp":"incentive","brand":"Riachuelo","instrutor":"","aud":45},
  {"dia":6,"time":"08:00","name":"Yoga","cat":"yoga","local":"Parque de Madureira","sp":"incentive","brand":"Riachuelo","instrutor":"","aud":50},
]

# Metadados dos patrocinadores
SPONSOR_META = {
  "Riachuelo":    {"tipo":"incentive","aulas_sem":9, "inicio":"22/06/2026","venc":"31/12/2026","cor":"#1a1a1a"},
  "Riachuelo ICMS":{"tipo":"incentive","aulas_sem":2,"inicio":"25/06/2026","venc":"31/12/2026","cor":"#333333"},
  "Porto":        {"tipo":"incentive","aulas_sem":3, "inicio":"06/07/2026","venc":"31/12/2026","cor":"#c4a200"},
  "Premier Pet":  {"tipo":"incentive","aulas_sem":2, "inicio":"04/07/2026","venc":"18/08/2026","cor":"#c0362a"},
  "Vivo":         {"tipo":"direct",   "aulas_sem":3, "inicio":"23/02/2026","venc":"31/12/2026","cor":"#6c3ea6"},
}

seed_json = json.dumps(SEED_DATA, ensure_ascii=False)
meta_json = json.dumps(SPONSOR_META, ensure_ascii=False)

# Data de início: 23 jun 2026 (Sem 2 porque Riachuelo começa 22/jun)
# Semana 1: 16-22 jun, Sem 2: 23-29 jun, Sem 3: 30 jun-6 jul, Sem 4: 7-13 jul
WEEKS_META = [
  {"label":"Sem. 1","range":"16–22 jun","start":[2026,5,16]},
  {"label":"Sem. 2","range":"23–29 jun","start":[2026,5,23]},
  {"label":"Sem. 3","range":"30 jun–6 jul","start":[2026,5,30]},
  {"label":"Sem. 4","range":"7–13 jul","start":[2026,6,7]},
]
weeks_json = json.dumps(WEEKS_META, ensure_ascii=False)

with open("/home/claude/mude-dashboard/index.html", "r") as f:
    html = f.read()

print(f"HTML loaded: {len(html)} chars")
print("Done build.py — data ready")
