import ijson
import json
import os
from pathlib import Path
from datetime import date

cats = ["222","333","333bf", "333fm", "333ft", "333mbf", "333mbo", "333oh","444", "444bf", "555", "555bf", "666", "777", "clock", "magic", "minx", "mmagic", "pyram", "skewb", "sq1"]

input_file = "./../cubing-peru-api-v0/Results/results.json"
competitions_file = "./../cubing-peru-api-v0/Competitions/competitions_prueba.json"
persons_file = "./../cubing-peru-api-v0/Persons/persons.json"

# 📌 Cargar competiciones en memoria para lookup rápido
with open(competitions_file, "r", encoding="utf-8") as f:
    competitions = {c["id"]: c for c in json.load(f)}

# 📌 Cargar personas en memoria para lookup rápido (por personId)
with open(persons_file, "r", encoding="utf-8") as f:
    persons = {p["id"]: p for p in json.load(f)}

folder = f"./../cubing-peru-api-v0/Results/single"
os.makedirs(folder, exist_ok=True)

for cat in cats:
    output_file = f"{folder}/{cat}.json"

    filtered_records = []
    with open(input_file, "rb") as f:
        for record in ijson.items(f, "item"):
            if record.get("eventId") == cat:

                single = int(record.get("best", -1))

                # 📌 ignorar -1 y 0
                if single in (-1, 0):
                    continue

                comp_id = record.get("competitionId")
                comp = competitions.get(comp_id, {})

                # añadir datos extra de competition
                record["competitionName"] = comp.get("name", "")
                record["cityName"] = comp.get("cityName", "")
                record["competitionDate"] = comp.get("competitionDate", "")

                # añadir gender desde persons.json
                pid = record.get("personId")
                record["gender"] = persons.get(pid, {}).get("gender", "")

                filtered_records.append(record)

    # 📌 ordenar: primero por best, si empatan usar fecha
    def sort_key(r):
        best = int(r.get("best", 99999999999999))
        date = r.get("competitionDate", "9999-99-99")
        return (best, date)

    filtered_records.sort(key=sort_key)

    # guardar
    with open(output_file, "w", encoding="utf-8") as out:
        json.dump(filtered_records, out, ensure_ascii=False, indent=2)

    print(f"✅ Listo, datos filtrados de la categoría: {cat}")