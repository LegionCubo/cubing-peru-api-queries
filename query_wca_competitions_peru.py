import ijson
import json
import re

# Archivos de entrada/salida
persons_file = "./../cubing-peru-api-v0/Persons/persons.json"
competitions_file = "./salida_json/WCA_export_Competitions.json"
output_file = "./../cubing-peru-api-v0/Competitions/competitions.json"

# Cargar personas de Perú
with open(persons_file, "r", encoding="utf-8") as pf:
    persons = json.load(pf)

# Diccionario {name -> id}
name_to_id = {p["name"]: p["id"] for p in persons}

# Regex para extraer nombres dentro de [{Nombre}{correo}]
pattern = re.compile(r"\{\s*([^}]+)\}\{[^}]+\}")

with open(competitions_file, "rb") as f, open(output_file, "w", encoding="utf-8") as out:
    out.write("[\n")
    first = True

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

        # Guardar solo si hay organizadores o delegados peruanos
        if organisers_ids or delegates_ids:
            record["organiser"] = organisers_ids
            record["wcaDelegate"] = delegates_ids

            if not first:
                out.write(",\n")
            json.dump(record, out, ensure_ascii=False)
            first = False

    out.write("\n]")

print("✅ Listo, se guardaron solo las competiciones con organizadores/delegados peruanos")
