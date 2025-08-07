from flask import Flask, render_template
from flask_bootstrap import Bootstrap
import json
import requests

app = Flask(__name__)
bootstrap = Bootstrap(app)


def ibge_host():
    return "https://servicodados.ibge.gov.br"


def api_path():
    return "api/v1/localidades"


def api_url():
    return ibge_host() + "/" + api_path()


def ibge_api_url(tipo_loc: str, loc_id: str | None = None):
    url = api_url() + "/" + tipo_loc
    if loc_id:
        url = url + "/" + loc_id
    return url


def get_api_data(tipo_loc: str, loc_id: str | None = None):
    url = ibge_api_url(tipo_loc, loc_id)
    r = requests.get(url)
    r.raise_for_status()
    return json.loads(r.content)


def render_tipo_localidade(tipo_loc):
    ibge_data = get_api_data(tipo_loc)
    descr = descr_tipo_loc(tipo_loc)
    return render_template(
        "body_locs.html", tipo_loc=tipo_loc, ibge_data=ibge_data, descr_tipo_loc=descr
    )


def render_localidade(tipo_loc, loc_id):
    ibge_data = get_api_data(tipo_loc, loc_id)
    descr = descr_tipo_loc(tipo_loc)
    return render_template(
        "body_localidade.html",
        tipo_loc=tipo_loc,
        ibge_data=ibge_data,
        descr_tipo_loc=descr,
    )


# TODO: o dicionário abaixo pode ir para um arquivo JSON
def tipos_loc():
    tipos = {
        "aglomeracoes-urbanas": {
            "descr": ["Aglomerações Urbanas", "Aglomeração urbana"]
        },
        "distritos": {"descr": ["Distritos", "Distrito"]},
        "mesorregioes": {"descr": ["Mesorregiões", "Mesorregião"]},
        "microrregioes": {"descr": ["Microrregiões", "Microrregião"]},
        "municipios": {"descr": ["Municípios", "Município"]},
        "paises": ["Países", "País"],
        "regioes": ["Regiões", "Região"],
        "regioes-imediatas": ["Regiões Imediatas", "Região imediata"],
        "regioes-integradas-de-desenvolvimento": [
            "Regiões Integradas de Desenvolvimento",
            "Região integrada de desenvolvimento",
        ],
        "regioes-intermediarias": ["Regiões Intermediárias", "Região intermediária"],
        "regioes-metropolitanas": ["Regiões Metropolitanas", "Região metropolitana"],
        "subdistritos": ["Subdistritos", "Subdistrito"],
        "estados": ["UFs", "UF"],
    }
    return tipos


def descr_tipo_loc(tipo_loc):
    return tipos_loc()[tipo_loc]


@app.route("/")
def home():
    return render_template("index.html", tipos_loc=tipos_loc())


@app.route("/localidades/<tipo_loc>")
def tipo_loc(tipo_loc):
    return render_tipo_localidade(tipo_loc)


@app.route("/localidades/<tipo_loc>/<loc_id>")
def loc(tipo_loc, loc_id):
    return render_localidade(tipo_loc, loc_id)
