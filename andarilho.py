from requests.models import stream_decode_response_unicode
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
import json
import requests
import app.localidades as localidades

app = Flask(__name__)
bootstrap = Bootstrap(app)


def file_ext() -> str:
    return "jinja"


def ibge_host() -> str:
    return "https://servicodados.ibge.gov.br"


def api_path() -> str:
    return "api/v1/localidades"


def api_url() -> str:
    return ibge_host() + "/" + api_path()


def render_tipo_localidade(tipo_loc: str) -> str:
    ibge_data = get_api_data(tipo_loc)
    descr = descr_tipo_loc(tipo_loc)
    return render_template(
        f"body_locs.{file_ext()}",
        tipo_loc=tipo_loc,
        ibge_data=ibge_data,
        descr_tipo_loc=descr,
    )


# TODO: o dicionário abaixo pode ir para um arquivo JSON
def tipos_loc() -> dict:
    tipos = {
        "aglomeracoes-urbanas": {
            "descr": ["Aglomerações Urbanas", "Aglomeração urbana"],
            "secoes-internas": [[0, "municipios"]],
            "ordem": "?orderBy=nome",
        },
        "distritos": {"descr": ["Distritos", "Distrito"], "ordem": "?orderBy=nome"},
        "mesorregioes": {"descr": ["Mesorregiões", "Mesorregião"]},
        "microrregioes": {
            "descr": ["Microrregiões", "Microrregião"],
            "ordem": "?orderBy=nome",
        },
        "municipios": {
            "descr": ["Municípios", "Município"],
            "pertence": [{"aglomeracoes-urbanas": "municipio"}],
        },
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


def extra_url(tipo_loc: str) -> str | None:
    specs = tipos_loc()[tipo_loc]
    return specs["ordem"]


def ibge_api_url(
    tipo_loc: str,
    loc_id: str | None = None,
    sub_loc: str | None = None,
    extras: str | None = None,
    qsub_loc: str | None = None,
    qid: str | None = None,
) -> str:
    url = ""
    for item in [
        f"{api_url()}/{tipo_loc}" if tipo_loc else "",
        f"/{loc_id}" if loc_id else "",
        f"/{sub_loc}" if sub_loc else "",
        extras if extras else "",
        f"/{qsub_loc}?" if qsub_loc else "",
        f"{qid}" if qid else "",
    ]:
        url += item
    return url


def get_api_data(
    tipo_loc: str,
    loc_id: str | None = None,
    sub_loc: str | None = None,
    qsub_loc: str | None = None,
    qid: str | None = None,
) -> str:
    url = ibge_api_url(
        tipo_loc, loc_id=loc_id, sub_loc=sub_loc, qsub_loc=qsub_loc, qid=qid
    )
    r = requests.get(url)
    r.raise_for_status()
    return json.loads(r.content)


def render_localidade(
    tipo_loc: str,
    loc_id: str | None = None,
    sub_loc: str | None = None,
    htmlTemplate: str | None = None,
) -> str:
    ibge_data = get_api_data(tipo_loc, loc_id=loc_id, sub_loc=sub_loc)
    obj_loc = localidades.factory(tipo_loc, ibge_data)
    descr = descr_tipo_loc(tipo_loc)
    secoes = {}
    secoes_pertence = {}
    htmlTemplate2 = (
        f"body_localidade.{file_ext()}" if htmlTemplate is None else htmlTemplate
    )
    if sub_loc is None:
        for secao in (tipos_loc()[tipo_loc]).get("secoes", []):
            secoes[secao] = ls_sub_loc(tipo_loc, loc_id=loc_id, ls_sub_loc=secao)
        htmlTemplate = f"body_localidade.{file_ext()}"
    for secao in tipos_loc()[tipo_loc].get("secoes-internas", []):
        secaoDados = (
            ibge_data[0]["municipios"] if isinstance(secao, list) else ibge_data[secao]
        )
        nomeSecao = secao[1] if isinstance(secao, list) else secao
        secoes[nomeSecao] = secaoDados
    for secao in (tipos_loc()[tipo_loc]).get("pertence", []):
        for key in secao:
            ibge_data_pertence = get_api_data(key, qsub_loc=secao.get(key), qid=loc_id)
            secoes_pertence[key] = ibge_data_pertence
    return render_template(
        htmlTemplate2,
        tipo_loc=tipo_loc,
        ibge_data=ibge_data,
        descr_tipo_loc=descr,
        sub_loc=sub_loc,
        secoes=secoes,
        secoes_pertence=secoes_pertence,
        obj_loc=obj_loc,
    )


def descr_tipo_loc(tipo_loc: str) -> str:
    return tipos_loc()[tipo_loc]["descr"]


def ls_sub_loc(tipo_loc, loc_id, ls_sub_loc) -> str:
    return get_api_data(tipo_loc, loc_id=loc_id, sub_loc=ls_sub_loc)


@app.route("/")
def home() -> str:
    return render_template(f"index.{file_ext()}", tipos_loc=tipos_loc())


@app.route("/localidades/<tipo_loc>")
def tipo_loc(tipo_loc) -> str:
    return render_tipo_localidade(tipo_loc)


@app.route("/localidades/<tipo_loc>/<loc_id>")
def loc(tipo_loc, loc_id) -> str:
    return render_localidade(tipo_loc, loc_id=loc_id)
