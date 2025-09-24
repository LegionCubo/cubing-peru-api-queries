import ijson
import json

input_file = "./salida_json/WCA_export_Results.json"

output_file = f"./../cubing-peru-api-v0/Results/results.json"

with open(input_file, "rb") as f, open(output_file, "w", encoding="utf-8") as out:
    out.write("[\n")
    first = True
    for record in ijson.items(f, "item"):  # cada objeto del array principal
        if record.get("personCountryId") == "Peru":
            if not first:
                out.write(",\n")
            json.dump(record, out, ensure_ascii=False)
            first = False
    out.write("\n]")

print("✅ Listo, resultados filtrados de Perú")