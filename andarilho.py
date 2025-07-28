from flask import Flask, render_template
from flask_bootstrap import Bootstrap
import json

app = Flask(__name__)
bootstrap = Bootstrap(app)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/aglomeracoes_urbanas")
def aglomeracoes_urbanas():
    with open("./ibge_data/localidades/aglomeracoes_urbanas.geojson", "r") as f:
        ibge_data = json.load(f)
    return render_template("aglomeracoes_urbanas.html", ibge_data=ibge_data)


@app.route("/regioes")
def regioes():
    with open("./ibge_data/localidades/regioes.geojson", "r") as f:
        ibge_data = json.load(f)
    return render_template("regioes.html", ibge_data=ibge_data)


@app.route("/ufs")
def ufs():
    with open("./ibge_data/localidades/ufs.geojson", "r") as f:
        ibge_data = json.load(f)
    return render_template("ufs.html", ibge_data=ibge_data)
