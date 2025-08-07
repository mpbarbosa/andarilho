from requests.models import stream_decode_response_unicode
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


def ibge_api_url(tipo_loc: str, loc_id: str | None = None, sub_loc: str | None = None):
    url = api_url() + "/" + tipo_loc
    if loc_id:
        url = url + "/" + loc_id
    if sub_loc:
        url = url + "/" + sub_loc
    return url


def get_api_data(tipo_loc: str, loc_id: str | None = None, sub_loc: str | None = None):
    url = ibge_api_url(tipo_loc, loc_id=loc_id, sub_loc=sub_loc)
    r = requests.get(url)
    r.raise_for_status()
    return json.loads(r.content)


def render_tipo_localidade(tipo_loc):
    ibge_data = get_api_data(tipo_loc)
    descr = descr_tipo_loc(tipo_loc)
    return render_template(
        "body_locs.html", tipo_loc=tipo_loc, ibge_data=ibge_data, descr_tipo_loc=descr
    )


# TODO: o dicionário abaixo pode ir para um arquivo JSON
def tipos_loc() -> dict:
    tipos = {
        "aglomeracoes-urbanas": {
            "descr": ["Aglomerações Urbanas", "Aglomeração urbana"]
        },
        "distritos": {"descr": ["Distritos", "Distrito"]},
        "mesorregioes": {"descr": ["Mesorregiões", "Mesorregião"]},
        "microrregioes": {"descr": ["Microrregiões", "Microrregião"]},
        "municipios": {"descr": ["Municípios", "Município"]},
        "paises": {"descr": ["Países", "País"]},
        "regioes": {"descr": ["Regiões", "Região"]},
        "regioes-imediatas": {"descr": ["Regiões Imediatas", "Região imediata"]},
        "regioes-integradas-de-desenvolvimento": {
            "descr": [
                "Regiões Integradas de Desenvolvimento",
                "Região integrada de desenvolvimento",
            ]
        },
        "regioes-intermediarias": {
            "descr": ["Regiões Intermediárias", "Região intermediária"]
        },
        "regioes-metropolitanas": {
            "descr": ["Regiões Metropolitanas", "Região metropolitana"]
        },
        "subdistritos": {"descr": ["Subdistritos", "Subdistrito"]},
        "estados": {"descr": ["UFs", "UF"], "secoes": ["municipios"]},
    }
    return tipos


def render_localidade(
    tipo_loc: str,
    loc_id: str | None = None,
    sub_loc: str | None = None,
    htmlTemplate: str | None = None,
):
    ibge_data = get_api_data(tipo_loc, loc_id=loc_id, sub_loc=sub_loc)
    descr = descr_tipo_loc(tipo_loc)
    secoes = {}
    htmlTemplate2 = "body_localidade.html" if htmlTemplate is None else htmlTemplate
    if sub_loc is None:
        for secao in (tipos_loc()[tipo_loc]).get("secoes", []):
            secoes[secao] = ls_sub_loc(tipo_loc, loc_id=loc_id, ls_sub_loc=secao)
        htmlTemplate = "body_localidade.html"
    return render_template(
        htmlTemplate2,
        tipo_loc=tipo_loc,
        ibge_data=ibge_data,
        descr_tipo_loc=descr,
        sub_loc=sub_loc,
        secoes=secoes,
    )


def descr_tipo_loc(tipo_loc):
    return tipos_loc()[tipo_loc]["descr"]


def ls_sub_loc(tipo_loc, loc_id, ls_sub_loc):
    return get_api_data(tipo_loc, loc_id=loc_id, sub_loc=ls_sub_loc)


@app.route("/")
def home():
    return render_template("index.html", tipos_loc=tipos_loc())


@app.route("/localidades/<tipo_loc>")
def tipo_loc(tipo_loc):
    return render_tipo_localidade(tipo_loc)


@app.route("/localidades/<tipo_loc>/<loc_id>")
def loc(tipo_loc, loc_id):
    return render_localidade(tipo_loc, loc_id=loc_id)
