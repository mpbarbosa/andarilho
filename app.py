import sys

path = "/home/mpb/Documents/GitHub/andarilho"
if path not in sys.path:
    sys.path.insert(0, path)

from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return "Hello world!"


if __name__ == "__main__":
    app.run()
