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


def url_tipo_loc(tipo_loc):
    return api_url() + "/" + tipo_loc


def get_api_data(tipo_loc):
    url = url_tipo_loc(tipo_loc)
    r = requests.get(url)
    return json.loads(r.content)


def render_localidade(tipo_loc):
    ibge_data = get_api_data(tipo_loc)
    descr = descr_tipo_loc(tipo_loc)
    return render_template(
        tipo_loc + ".html", ibge_data=ibge_data, descr_tipo_loc=descr
    )


def render_localidade2(tipo_loc):
    ibge_data = get_api_data(tipo_loc)
    descr = descr_tipo_loc(tipo_loc)
    return render_template("body_loc.html", ibge_data=ibge_data, descr_tipo_loc=descr)


def tipos_loc():
    tipos = {
        "aglomeracos_urbanas": "Aglomerações Urbanas",
        "distritos": "Distritos",
        "mesorregioes": "Mesorregiões",
        "microrregios": "Microrregiões",
        "municipios": "Municípios",
        "paises": "Países",
        "regioes": "Regiões",
        "regioesimediatas": "Regiões Imediatas",
        "regioesintegradasdedesenvolvimento": "Regoões Integradas de Desenvolvimento",
        "regioesintermediarias": "Regiões Intermediárias",
        "regioesmetropolitanas": "Regiões Metropolitanas",
        "subdistritos": "Subdistritos",
        "estados": "UFs",
    }
    return tipos


def descr_tipo_loc(tipo_loc):
    return tipos_loc()[tipo_loc]


@app.route("/")
def home():
    return render_template("index.html", tipos_loc=tipos_loc())


@app.route("/localidades/<tipo_loc>")
def tipo_loc(tipo_loc):
    return render_localidade2(tipo_loc)


@app.route("/ufs")
def ufs():
    with open("./ibge_data/localidades/ufs.geojson", "r") as f:
        ibge_data = json.load(f)
    return render_template("ufs.html", ibge_data=ibge_data)


@app.route("/uf/<uf_id>")
def uf(uf_id):
    url = f"https://servicodados.ibge.gov.br/api/v1/localidades/estados/{uf_id}"
    r = requests.get(url)
    ibge_data = json.loads(r.content)
    return render_template("uf.html", ibge_data=ibge_data)
