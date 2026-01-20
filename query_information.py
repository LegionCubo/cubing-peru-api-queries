import json
from datetime import datetime

output_file = "./../cubing-peru-api-v0/Information/information.json"

MONTHS = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']

def load_json(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def build_info():
    # 1. LOAD FILES
    persons = load_json("./../cubing-peru-api-v0/Persons/persons.json")
    competitions = load_json("./../cubing-peru-api-v0/Competitions/competitions.json")
    single_333 = load_json("./../cubing-peru-api-v0/Rankings/single/333.json")

    # Rankings
    ranking_333 = load_json("./../cubing-peru-api-v0/Rankings/average/333.json")

    # 2. competitors → count objects
    competitors = len(persons)

    # 3. competitions → count objects
    competitions_count = len(competitions)

    # 4. recordNational → take best from first object
    record_national = int(single_333[0].get("best", 0))

    # 5. upcomingCompetitions → future competitions
    today = datetime.now().strftime("%Y-%m-%d")

    upcoming = []
    for c in competitions:
        if c["competitionDate"] >= today:

            # Procesar fecha YYYY-MM-DD
            year, month, day = c["competitionDate"].split("-")

            # Convertir mes a abreviatura
            monthDate = MONTHS[int(month) - 1]

            upcoming.append({
                "id": c["id"],
                "name": c["name"],
                "venue": c["venue"],
                "city_name": c["city_name"],
                "country_id": c["country_id"],
                "venue_address": c["venue_address"],
                "venue_details": c["venue_details"],
                "latitude_microdegrees": c["latitude_microdegrees"],
                "longitude_microdegrees": c["longitude_microdegrees"],
                "competitionDate": c["competitionDate"],
                "competitionEndDate": c["competitionEndDate"],
                "monthDate": monthDate,         # <-- Nuevo campo
                "dayDate": int(day),            # <-- Nuevo campo
            })

    upcoming.sort(key=lambda x: x["competitionDate"])

    # 6. rankingNational → first 5 based on 333 single ranking
    ranking_national = []
    for r in ranking_333[:5]:
        ranking_national.append({
            "personIdNr": r["person_id"],
            "nameNr": r["person_name"],
            "averageNr": int(r["average"]),
            "idCompetitionNr": r["competition_id"],
            "competitionNr": r["competitionName"],
            "competitionCountryIso": r["competitionCountryIso"]
        })

    # 7. Build final object
    info = {
        "competitors": competitors,
        "competitions": competitions_count,
        "recordNational": record_national,
        "upcomingCompetitions": upcoming,
        "rankingNational": ranking_national
    }

    return info

# Guardar JSON
with open(output_file, "w", encoding="utf-8") as out:
    data = build_info()
    json.dump(data, out, ensure_ascii=False, indent=2)

print("✅ Se genero la informacion para el home.")
