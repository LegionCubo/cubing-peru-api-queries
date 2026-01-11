import json
from collections import defaultdict
from datetime import datetime

# Archivos de entrada/salida
persons_file = "./../cubing-peru-api-v0/Persons/persons.json"
competitions_file = "./../cubing-peru-api-v0/Competitions/competitions_prueba.json"
output_file = "./../cubing-peru-api-v0/Persons/Organisers/organisers.json"

# Fecha actual
today = datetime.today().date()

# Cargar personas de Perú
with open(persons_file, "r", encoding="utf-8") as pf:
    persons = json.load(pf)

# Crear diccionario {id -> person}
persons_dict = {p["wca_id"]: p for p in persons}

# Contadores
organiser_count = defaultdict(int)
last_organiser_competition = {}

# Leer competitions
with open(competitions_file, "r", encoding="utf-8") as cf:
    competitions = json.load(cf)

# Procesar competencias
for comp in competitions:
    comp_id = comp.get("id")
    comp_name = comp.get("name")
    comp_date_str = comp.get("competitionDate")

    if not comp_date_str:
        continue  # ignoramos comps sin fecha

    comp_date = datetime.strptime(comp_date_str, "%Y-%m-%d").date()

    for organiser_id in comp.get("organiser", []):
        

        # Solo considerar comps que ya ocurrieron
        if comp_date <= today:
            organiser_count[organiser_id] += 1
            
            if (
                organiser_id not in last_organiser_competition
                or comp_date > datetime.strptime(last_organiser_competition[organiser_id]["competitionDate"], "%Y-%m-%d").date()
            ):
                last_organiser_competition[organiser_id] = {
                    "competitionId": comp_id,
                    "competitionName": comp_name,
                    "competitionDate": comp_date_str,
                    "competitionCountryIso": comp["countryIso"]
                }

# Crear salida final
organisers_output = []
for pid, count in organiser_count.items():
    if pid in persons_dict and count > 0:
        person = persons_dict[pid].copy()
        person["competitionsOrganised"] = count
        person["lastOrganiserCompetition"] = last_organiser_competition.get(pid)
        organisers_output.append(person)

# Guardar en JSON
with open(output_file, "w", encoding="utf-8") as out:
    json.dump(organisers_output, out, ensure_ascii=False, indent=2)

print("✅ Listo, se creó json con organizadores peruanos, cantidad de competencias delegadas y última competencia")
