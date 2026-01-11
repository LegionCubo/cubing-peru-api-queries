import ijson
import json
import re
from datetime import datetime

# Archivos de entrada/salida
persons_file = "./../cubing-peru-api-v0/Persons/persons.json"
competitions_file = "./salida_json/WCA_export_competitions.json"
results_file = "./../cubing-peru-api-v0/Results/results.json"
output_file = "./../cubing-peru-api-v0/Competitions/competitions_prueba.json"

countriesFile = "./salida_json/WCA_export_countries.json"

# Cargar personas (para mapear nombres → IDs en organiser/delegate)
with open(persons_file, "r", encoding="utf-8") as pf:
    persons = json.load(pf)
name_to_id = {p["name"]: p["wca_id"] for p in persons}

with open(countriesFile, "r", encoding="utf-8") as f:
    countries = {p["id"]: p for p in json.load(f)}

# Regex para extraer nombres dentro de [{Nombre}{correo}]
pattern = re.compile(r"\{\s*([^}]+)\}\{[^}]+\}")

competitions = {}
peruvian_competitions = set()

# 📌 Paso 1: leer results.json y detectar competencias con peruanos
with open(results_file, "rb") as rf:
    for record in ijson.items(rf, "item"):
        if record.get("person_country_id") == "Peru":  # 🔥 más directo
            comp_id = record.get("competition_id")
            if comp_id:
                peruvian_competitions.add(comp_id)

# 📌 Paso 2: leer competitions y filtrar
with open(competitions_file, "rb") as f:
    for record in ijson.items(f, "item"):
        organisers_ids = []
        delegates_ids = []

        # Procesar organisers
        if record.get("organizers"):
            names = pattern.findall(record["organizers"])
            organisers_ids = [name_to_id[n] for n in names if n in name_to_id]

        # Procesar wcaDelegates
        if record.get("delegates"):
            names = pattern.findall(record["delegates"])
            delegates_ids = [name_to_id[n] for n in names if n in name_to_id]

        comp_id = record.get("id")

        # Guardar solo si:
        # 1. Tiene organizadores/delegados peruanos
        # 2. O hubo participación de peruanos
        if organisers_ids or delegates_ids or comp_id in peruvian_competitions:
            # Construir competitionDate
            year = record.get("year")
            month = record.get("month")
            day = record.get("day")
            end_month = record.get("end_month")
            end_day = record.get("end_day")

            competition_date = f"{year}-{int(month):02d}-{int(day):02d}"
            competition_end_date = f"{year}-{int(end_month):02d}-{int(end_day):02d}"

            # Eliminar los campos originales
            for key in ["year", "month", "day", "end_month", "end_day"]:
                record.pop(key, None)

            # Añadir nuevos campos
            record["competitionDate"] = competition_date
            record["competitionEndDate"] = competition_end_date

            # Reemplazar organisers y delegates
            record["organiser"] = organisers_ids
            record["wcaDelegate"] = delegates_ids

            competitions[comp_id] = record  # evitar duplicados

            #REGISTRAR ISO
            countryId = record.get("country_id")
            country = countries.get(countryId, {})
            record["countryIso"] = country.get("iso2", "")

# 📌 Paso 3: ordenar por fecha
competitions = list(competitions.values())
competitions.sort(key=lambda x: datetime.strptime(x["competitionDate"], "%Y-%m-%d"))

# Guardar JSON
with open(output_file, "w", encoding="utf-8") as out:
    json.dump(competitions, out, ensure_ascii=False, indent=2)

print("✅ Listo, ahora incluye todas las competencias donde participaron cuberos peruanos, además de organizadas/delegadas")
