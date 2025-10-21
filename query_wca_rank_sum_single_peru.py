import json
import os
from collections import defaultdict

cats = ["222","333","333bf", "333fm", "333mbf", "333oh","444", "444bf", "555", "555bf", "666", "777", "clock", "minx", "pyram", "skewb", "sq1"]

# 📂 Paths
rankings_folder = "./../cubing-peru-api-v0/Rankings/single"
wca_ranks_file = "./salida_json/WCA_export_RanksSingle.json"
persons_file = "./../cubing-peru-api-v0/Persons/persons.json"
output_file = "./../cubing-peru-api-v0/RankingsSum/single_sumatoria.json"

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

# diccionario: (personId, eventId) -> rank info
wca_lookup = {(r["personId"], r["eventId"]): r for r in wca_ranks}

# 📌 Cargar persons.json para obtener gender
with open(persons_file, "r", encoding="utf-8") as f:
    persons_data = json.load(f)

gender_lookup = {p["id"]: p.get("gender") for p in persons_data}

# 📌 Todas las personas que aparecen en algún evento
persons = set()
for cat in cats:
    for record in rankings[cat]:
        persons.add(record["personId"])

# 📌 Construir sumatoria
sumatoria = []

for pid in persons:
    person_data = {
        "personName": None,  # se llenará con el primer record encontrado
        "personId": pid,
        "gender": gender_lookup.get(pid, None),
        "rankingSum": 0,
        "categories": []
    }

    for cat in cats:
        # buscar en ranking local
        records = [r for r in rankings[cat] if r["personId"] == pid]
        if records:
            record = records[0]  # ya está ordenado por mejor
            country_rank = wca_lookup.get((pid, cat), {}).get("countryRank")

            if not person_data["personName"]:
                person_data["personName"] = record.get("personName", "")

            person_data["categories"].append({
                "eventId": cat,
                "best": record.get("best"),
                "competitionId": record.get("competitionId"),
                "competitionName": record.get("competitionName"),
                "competitionCountryIso": record.get("competitionCountryIso"),
                "countryRank": int(country_rank) if country_rank else None
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
                "countryRank": simulated_rank
            })

            person_data["rankingSum"] += simulated_rank

    sumatoria.append(person_data)

# 📌 Ordenar por rankingSum (menor es mejor)
sumatoria.sort(key=lambda x: x["rankingSum"])

# 📂 Guardar
with open(output_file, "w", encoding="utf-8") as out:
    json.dump(sumatoria, out, ensure_ascii=False, indent=2)

print(f"✅ Ranking de sumatoria generado en {output_file}")
