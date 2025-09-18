import json
from collections import defaultdict

# Archivos de entrada/salida
persons_file = "./../cubing-peru-api-v0/Persons/persons.json"
competitions_file = "./../cubing-peru-api-v0/Competitions/competitions.json"
output_file = "./../cubing-peru-api-v0/Persons/Delegates/delegates.json"

# Cargar personas de Perú
with open(persons_file, "r", encoding="utf-8") as pf:
    persons = json.load(pf)

# Crear diccionario {id -> person}
persons_dict = {p["id"]: p for p in persons}

# Contador de competencias organizadas
wcaDelegate_count = defaultdict(int)

# Leer competitions
with open(competitions_file, "r", encoding="utf-8") as cf:
    competitions = json.load(cf)

# Contar apariciones de cada wcaDelegate
for comp in competitions:
    for wcaDelegate_id in comp.get("wcaDelegate", []):
        wcaDelegate_count[wcaDelegate_id] += 1

# Crear lista solo con los que tienen al menos 1 competencia
wcaDelegates_output = []
for pid, count in wcaDelegate_count.items():
    if pid in persons_dict and count > 0:
        person = persons_dict[pid].copy()
        person["competitionsDelegated"] = count
        wcaDelegates_output.append(person)

# Guardar en JSON
with open(output_file, "w", encoding="utf-8") as out:
    json.dump(wcaDelegates_output, out, ensure_ascii=False, indent=2)

print("✅ Listo, se creó json con delegados peruanos y su cantidad de competencias delegadas")
