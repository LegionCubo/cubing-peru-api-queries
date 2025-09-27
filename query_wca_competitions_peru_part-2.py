import ijson
import json
import re
from datetime import datetime

# Archivos de entrada/salida
persons_file = "./salida_json/WCA_export_Persons.json"
competitions_file = "./salida_json/WCA_export_Competitions.json"
output_file = "./../cubing-peru-api-v0/Competitions/competitions.json"

# Cargar personas (para mapear nombres → IDs en organiser/delegate)
with open(persons_file, "r", encoding="utf-8") as pf:
    persons = json.load(pf)
name_to_id = {p["name"]: p["id"] for p in persons}

# Regex para extraer nombres dentro de [{Nombre}{correo}]
pattern = re.compile(r"\{\s*([^}]+)\}\{[^}]+\}")

competitions = {}
peruvian_competitions = set()

# 📌 Paso 2: leer competitions y filtrar
with open(competitions_file, "rb") as f:
    for record in ijson.items(f, "item"):
        organisers_ids = []
        delegates_ids = []

        # Procesar organisers
        if record.get("organiser"):
            names = pattern.findall(record["organiser"])
            organisers_ids = [name_to_id[n] for n in names if n in name_to_id]

        # Procesar wcaDelegates
        if record.get("wcaDelegate"):
            names = pattern.findall(record["wcaDelegate"])
            delegates_ids = [name_to_id[n] for n in names if n in name_to_id]

        comp_id = record.get("id")

        # Guardar solo si:
        # 1. Tiene organizadores/delegados peruanos
        # 2. O hubo participación de peruanos
        if record.get("countryId") == "Peru" and record.get("cancelled") != "1":
            # Construir competitionDate
            year = record.get("year")
            month = record.get("month")
            day = record.get("day")
            endMonth = record.get("endMonth")
            endDay = record.get("endDay")

            competition_date = f"{year}-{int(month):02d}-{int(day):02d}"
            competition_end_date = f"{year}-{int(endMonth):02d}-{int(endDay):02d}"

            # Eliminar los campos originales
            for key in ["year", "month", "day", "endMonth", "endDay", "information", "external_website", "cancelled"]:
                record.pop(key, None)

            # Añadir nuevos campos
            record["competitionDate"] = competition_date
            record["competitionEndDate"] = competition_end_date

            # Reemplazar organisers y delegates
            record["organiser"] = organisers_ids
            record["wcaDelegate"] = delegates_ids

            competitions[comp_id] = record  # evitar duplicados

# 📌 Paso 3: ordenar por fecha
competitions = list(competitions.values())
competitions.sort(key=lambda x: datetime.strptime(x["competitionDate"], "%Y-%m-%d"), reverse=True)

# Guardar JSON
with open(output_file, "w", encoding="utf-8") as out:
    json.dump(competitions, out, ensure_ascii=False, indent=2)

print("✅ Listo, todas las competencias de peru")
