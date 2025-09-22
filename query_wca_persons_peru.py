import ijson
import json
from collections import defaultdict

# Archivos
input_persons = "./salida_json/WCA_export_Persons.json"
input_results = "./../cubing-peru-api-v0/Results/results.json"
output_file = "./../cubing-peru-api-v0/Persons/persons.json"

# Cargar resultados de Perú y contar competiciones distintas por persona
competitions_by_person = defaultdict(set)

with open(input_results, "r", encoding="utf-8") as rf:
    results = json.load(rf)
    for r in results:
        pid = r.get("personId")
        cid = r.get("competitionId")
        if pid and cid:
            competitions_by_person[pid].add(cid)

# Crear persons.json con columna competitions
with open(input_persons, "rb") as f, open(output_file, "w", encoding="utf-8") as out:
    out.write("[\n")
    first = True
    for record in ijson.items(f, "item"):  # cada objeto del array principal
        if record.get("countryId") == "Peru":
            pid = record.get("id")
            record["competitions"] = len(competitions_by_person.get(pid, []))  # contar comps

            # Eliminar los campos originales
            for key in ["subid"]:
                record.pop(key, None)

            if not first:
                out.write(",\n")
            json.dump(record, out, ensure_ascii=False)
            first = False
    out.write("\n]")

print("✅ Listo, se filtro las personas de Perú y se agregó la cantidad de competiciones en las que participaron")
