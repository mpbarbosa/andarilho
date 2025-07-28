import os
import requests

# Inicialmente faz-se necessário criar uma pasta que receberá os dados do IBGE
data_path = os.path.join("..", "ibge_data")
input_path = os.path.join(data_path, "input")
loc_input_path = os.path.join(data_path, "localidades")
output_path = os.path.join(data_path, "output")

output_path_geo = os.path.join(output_path, "geo")
output_path_tab = os.path.join(output_path, "tab")

os.makedirs(data_path, exist_ok=True)
os.makedirs(input_path, exist_ok=True)
os.makedirs(loc_input_path, exist_ok=True)
os.makedirs(output_path, exist_ok=True)
os.makedirs(output_path_geo, exist_ok=True)
os.makedirs(output_path_tab, exist_ok=True)

data_files = [
    (
        "https://servicodados.ibge.gov.br/api/v1/localidades/aglomeracoes-urbanas?orderBy=nome",
        "aglomeracoes_urbanas.geojson",
    ),
    ("https://servicodados.ibge.gov.br/api/v1/localidades/regioes", "regioes.geojson"),
    ("https://servicodados.ibge.gov.br/api/v1/localidades/estados", "ufs.geojson"),
]

for f in data_files:
    geojson_file = os.path.join(loc_input_path, f[1])
    if not os.path.exists(geojson_file):
        url = f[0]
        r = requests.get(url)

        # Save
        with open(geojson_file, "wb") as f:
            f.write(r.content)
