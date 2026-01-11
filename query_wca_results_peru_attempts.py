import json
import ijson

RESULTS_FILE = "./../cubing-peru-api-v0/Results/results.json"
ATTEMPTS_FILE = "./salida_json/WCA_export_result_attempts.json"
OUTPUT_FILE = "./../cubing-peru-api-v0/Results/attempts.json"

# 1. Cargar IDs válidos de results (este archivo es pequeño)
with open(RESULTS_FILE, "r", encoding="utf8") as f:
    results = json.load(f)

valid_ids = {item["id"] for item in results}
print(f"IDs válidos cargados: {len(valid_ids)}")

# 2. Abrir output
with open(OUTPUT_FILE, "w", encoding="utf8") as out:
    out.write("[\n")  # inicio del array JSON

    first = True

    # 3. Leer el archivo gigante con ijson
    with open(ATTEMPTS_FILE, "rb") as f:
        attempts = ijson.items(f, "item")  # cada elemento del array

        for attempt in attempts:
            if attempt["result_id"] in valid_ids:

                # Formato bonito
                json_str = json.dumps(attempt, ensure_ascii=False)

                if not first:
                    out.write(",\n")  # separar JSONs
                first = False

                out.write(json_str)

    out.write("\n]")  # fin del array JSON

print("Filtrado terminado.")
