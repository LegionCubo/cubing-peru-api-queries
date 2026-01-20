import requests #descargar
import zipfile
import io
import csv
import json
import os

# URL del ZIP
url = "https://assets.worldcubeassociation.org/export/results/WCA_export_v2_020_20260120T000021Z.tsv.zip"

# Carpeta de salida
output_dir = "salida_json"
os.makedirs(output_dir, exist_ok=True)

# 1. Descargar el ZIP desde la URL
print("⬇️ Descargando ZIP...")
response = requests.get(url, stream=True)
response.raise_for_status()  # Lanza error si la descarga falla

# Guardar en memoria (puedes guardarlo en disco si prefieres)
zip_bytes = io.BytesIO(response.content)

# 2. Abrir el ZIP
with zipfile.ZipFile(zip_bytes) as z:
    # Recorrer archivos dentro del ZIP
    for file_name in z.namelist():
        if file_name.endswith(".tsv"):
            print(f"📄 Procesando {file_name}...")

            # 3. Leer archivo TSV directamente del ZIP
            with z.open(file_name) as f:
                reader = csv.DictReader(io.TextIOWrapper(f, encoding="utf-8"), delimiter="\t")
                data = list(reader)

            # 4. Guardar como JSON en la carpeta de salida
            json_name = os.path.join(output_dir, file_name.replace(".tsv", ".json"))
            with open(json_name, "w", encoding="utf-8") as json_file:
                json.dump(data, json_file, ensure_ascii=False, indent=2)

            print(f"✅ Guardado: {json_name}")

print("🎉 Conversión completada")
