import subprocess

# Lista de scripts a ejecutar (en orden)
scripts = [
    "query_wca_results_peru.py",
    "query_wca_persons_peru.py",
    "query_wca_competitions_peru_part-1.py",
    "query_wca_competitions_peru_part-2.py",
    "query_wca_results_peru_single_for_cat.py",
    "query_wca_results_peru_average_for_cat.py",
    "query_wca_rank_peru.py",
    "query_wca_rank_sum_single_peru.py",
    "query_wca_rank_sum_average_peru.py",
    "query_wca_persons_peru_segundo_paso.py",
    "query_wca_persons_delegates_peru.py",
    "query_wca_persons_organisers_peru.py",
    "query_wca_records_peru.py",
]

for script in scripts:
    subprocess.run(["py", script], check=True)

print("🎉 Todas las queries fueron ejecutadas correctamente")