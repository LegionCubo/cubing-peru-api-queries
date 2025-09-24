import json
from collections import defaultdict
from datetime import datetime

# Archivos de entrada/salida
persons_file = "./../cubing-peru-api-v0/Persons/persons.json"
competitions_file = "./../cubing-peru-api-v0/Competitions/competitions_prueba.json"
output_file = "./../cubing-peru-api-v0/Persons/Delegates/delegates.json"

# Fecha actual
today = datetime.today().date()

# Cargar personas de Perú
with open(persons_file, "r", encoding="utf-8") as pf:
    persons = json.load(pf)

# Crear diccionario {id -> person}
persons_dict = {p["id"]: p for p in persons}

# Contadores
wcaDelegate_count = defaultdict(int)
last_delegate_competition = {}

# Leer competitions
with open(competitions_file, "r", encoding="utf-8") as cf:
    competitions = json.load(cf)

# Procesar cada competencia
for comp in competitions:
    comp_date_str = comp.get("competitionDate")
    if not comp_date_str:
        continue  # ignoramos comps sin fecha

    comp_date = datetime.strptime(comp_date_str, "%Y-%m-%d").date()

    for wcaDelegate_id in comp.get("wcaDelegate", []):
        wcaDelegate_count[wcaDelegate_id] += 1

        # Solo considerar si ya ocurrió
        if comp_date <= today:
            if (
                wcaDelegate_id not in last_delegate_competition
                or comp_date > datetime.strptime(last_delegate_competition[wcaDelegate_id]["competitionDate"], "%Y-%m-%d").date()
            ):
                last_delegate_competition[wcaDelegate_id] = {
                    "competitionId": comp["id"],
                    "competitionName": comp["name"],
                    "competitionDate": comp_date_str,
                }

# Crear salida
wcaDelegates_output = []
for pid, count in wcaDelegate_count.items():
    if pid in persons_dict and count > 0:
        person = persons_dict[pid].copy()
        person["competitionsDelegated"] = count
        person["lastDelegatedCompetition"] = last_delegate_competition.get(pid)
        wcaDelegates_output.append(person)

# Guardar en JSON
with open(output_file, "w", encoding="utf-8") as out:
    json.dump(wcaDelegates_output, out, ensure_ascii=False, indent=2)

print("✅ Listo, se creó json con delegados peruanos, su cantidad de competencias delegadas y la última competencia delegada")
