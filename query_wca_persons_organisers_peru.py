import json
from collections import defaultdict

# Archivos de entrada/salida
persons_file = "./../cubing-peru-api-v0/Persons/persons.json"
competitions_file = "./../cubing-peru-api-v0/Competitions/competitions.json"
output_file = "./../cubing-peru-api-v0/Persons/Organisers/organisers.json"

# Cargar personas de Perú
with open(persons_file, "r", encoding="utf-8") as pf:
    persons = json.load(pf)

# Crear diccionario {id -> person}
persons_dict = {p["id"]: p for p in persons}

# Contador de competencias organizadas
organiser_count = defaultdict(int)

# Leer competitions
with open(competitions_file, "r", encoding="utf-8") as cf:
    competitions = json.load(cf)

# Contar apariciones de cada organiser
for comp in competitions:
    for organiser_id in comp.get("organiser", []):
        organiser_count[organiser_id] += 1

# Crear lista solo con los que tienen al menos 1 competencia
organisers_output = []
for pid, count in organiser_count.items():
    if pid in persons_dict and count > 0:
        person = persons_dict[pid].copy()
        person["competitionsOrganised"] = count
        organisers_output.append(person)

# Guardar en JSON
with open(output_file, "w", encoding="utf-8") as out:
    json.dump(organisers_output, out, ensure_ascii=False, indent=2)

print("✅ Listo, se creó json con organizadores peruanos y su cantidad de competencias organizadas")
