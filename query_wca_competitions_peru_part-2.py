import ijson
import json
import re
from datetime import datetime

# Archivos de entrada/salida
persons_file = "./salida_json/WCA_export_persons.json"
competitions_file = "./salida_json/WCA_export_competitions.json"
output_file = "./../cubing-peru-api-v0/Competitions/competitions.json"

# Cargar personas (para mapear nombres → IDs en organiser/delegate)
with open(persons_file, "r", encoding="utf-8") as pf:
    persons = json.load(pf)
name_to_id = {p["name"]: p["wca_id"] for p in persons}

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
        if record.get("organizers"):
            names = pattern.findall(record["organizers"])
            organisers = [
                {"id": name_to_id[n], "name": n} if n in name_to_id else {"name": n}
                for n in names
            ]
        else:
            organisers = []

        # Procesar wcaDelegates
        if record.get("delegates"):
            names = pattern.findall(record["delegates"])
            delegates = [
                {"id": name_to_id[n], "name": n} if n in name_to_id else {"name": n}
                for n in names
            ]
        else:
            delegates = []

        comp_id = record.get("id")

        # Guardar solo si:
        # 1. Tiene organizadores/delegados peruanos
        # 2. O hubo participación de peruanos
        if record.get("country_id") == "Peru" and record.get("cancelled") != "1":
            # Construir competitionDate
            year = record.get("year")
            month = record.get("month")
            day = record.get("day")
            endMonth = record.get("end_month")
            endDay = record.get("end_day")

            competition_date = f"{year}-{int(month):02d}-{int(day):02d}"
            competition_end_date = f"{year}-{int(endMonth):02d}-{int(endDay):02d}"

            # Eliminar los campos originales
            for key in ["year", "month", "day", "end_month", "end_day", "information", "external_website", "cancelled", "delegates", "organizers","end_year"]:
                record.pop(key, None)

            # Añadir nuevos campos
            record["competitionDate"] = competition_date
            record["competitionEndDate"] = competition_end_date

            # Reemplazar organisers y delegates
            record["organiser"] = organisers
            record["wcaDelegate"] = delegates

            competitions[comp_id] = record  # evitar duplicados

# 📌 Paso 3: ordenar por fecha
competitions = list(competitions.values())
competitions.sort(key=lambda x: datetime.strptime(x["competitionDate"], "%Y-%m-%d"), reverse=True)

# Guardar JSON
with open(output_file, "w", encoding="utf-8") as out:
    json.dump(competitions, out, ensure_ascii=False, indent=2)

print("✅ Listo, todas las competencias de peru")
