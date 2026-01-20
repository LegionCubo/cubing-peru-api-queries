import json
import os
from collections import defaultdict

cats = ["222","333","333bf", "333fm", "333oh","444", "444bf", "555", "555bf", "666", "777", "clock", "minx", "pyram", "skewb", "sq1"]

# 📂 Paths
rankings_folder = "./../cubing-peru-api-v0/Rankings/average"
wca_ranks_file = "./salida_json/WCA_export_ranks_average.json"
persons_file = "./salida_json/WCA_export_persons.json"
output_file = "./../cubing-peru-api-v0/RankingsSum/average_sumatoria.json"

# 📌 Cargar rankings locales
rankings = {}
for cat in cats:
    path = f"{rankings_folder}/{cat}.json"
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            rankings[cat] = json.load(f)
    else:
        rankings[cat] = []

# 📌 Cargar ranks oficiales de la WCA
with open(wca_ranks_file, "r", encoding="utf-8") as f:
    wca_ranks = json.load(f)

# 📌 Cargar persons.json
with open(persons_file, "r", encoding="utf-8") as f:
    persons_data = json.load(f)

# diccionario: (personId, eventId) -> rank info
wca_lookup = {(r["person_id"], r["event_id"]): r for r in wca_ranks}

# diccionario: personId -> gender
persons_lookup = {p["wca_id"]: p.get("gender") for p in persons_data}

# 📌 Todas las personas que aparecen en algún evento
persons = set()
for cat in cats:
    for record in rankings[cat]:
        persons.add(record["person_id"])

# 📌 Construir sumatoria
sumatoria = []

for pid in persons:
    person_data = {
        "personName": None,
        "personId": pid,
        "gender": persons_lookup.get(pid, None),
        "rankingSum": 0,
        "categories": []
    }

    for cat in cats:
        # buscar en ranking local
        records = [r for r in rankings[cat] if r["person_id"] == pid]
        if records:
            record = records[0]  # ya está ordenado por mejor
            country_rank = wca_lookup.get((pid, cat), {}).get("country_rank")

            if not person_data["personName"]:
                person_data["personName"] = record.get("person_name", "")

            # extraer los 5 tiempos si existen
            times = []
            for i in range(1, 6):
                val = record.get(f"value{i}")
                if val is not None:
                    times.append(str(val))

            person_data["categories"].append({
                "eventId": cat,
                "average": record.get("average"),
                "competitionId": record.get("competition_id"),
                "competitionName": record.get("competitionName"),
                "competitionCountryIso": record.get("competitionCountryIso"),
                "countryRank": int(country_rank) if country_rank else None,
                "times": times
            })

            person_data["rankingSum"] += int(country_rank) if country_rank else 0

        else:
            # persona no participó en esta cat
            total = len(rankings[cat])
            simulated_rank = total + 1

            person_data["categories"].append({
                "eventId": cat,
                "best": None,
                "competitionId": None,
                "competitionName": None,
                "competitionCountryIso": None,
                "countryRank": simulated_rank,
                "times": []
            })

            person_data["rankingSum"] += simulated_rank

    sumatoria.append(person_data)

# 📌 Ordenar por rankingSum
sumatoria.sort(key=lambda x: x["rankingSum"])

# 📂 Guardar
with open(output_file, "w", encoding="utf-8") as out:
    json.dump(sumatoria, out, ensure_ascii=False, indent=2)

print(f"✅ Ranking de sumatoria (average) generado en {output_file}")
