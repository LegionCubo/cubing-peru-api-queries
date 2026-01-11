import json
import ijson

RESULTS_FILE = "./../cubing-peru-api-v0/Results/results.json"
ATTEMPTS_FILE = "./../cubing-peru-api-v0/Results/attempts.json"   # el archivo que generaste antes
OUTPUT_FILE = "./../cubing-peru-api-v0/Results/merge_results.json"

# 1. Cargar results (pocos datos → memoria OK)
with open(RESULTS_FILE, "r", encoding="utf8") as f:
    results = json.load(f)

# Convertir a diccionario por ID
results_dict = {r["id"]: r for r in results}

# 2. Diccionario para guardar attempts por result_id
attempts_by_result = {}

# 3. Leer attempts en streaming
with open(ATTEMPTS_FILE, "rb") as f:
    attempts = ijson.items(f, "item")

    for att in attempts:
        rid = att["result_id"]
        num = int(att["attempt_number"])
        val = att["value"]   # SE GUARDA COMO STRING

        if rid not in attempts_by_result:
            attempts_by_result[rid] = {}

        attempts_by_result[rid][f"value{num}"] = val

# 4. Fusionar
merged = []

for rid, rdata in results_dict.items():
    new_item = dict(rdata)

    # Prellenar value1..value5 con "0"
    for i in range(1, 6):
        new_item[f"value{i}"] = "0"

    # Reemplazar con valores reales si existen
    if rid in attempts_by_result:
        for key, val in attempts_by_result[rid].items():
            new_item[key] = val  # TODOS SON STRING

    merged.append(new_item)

# 5. Guardar archivo final
with open(OUTPUT_FILE, "w", encoding="utf8") as f:
    json.dump(merged, f, indent=2, ensure_ascii=False)

print("Archivo generado:", OUTPUT_FILE)
