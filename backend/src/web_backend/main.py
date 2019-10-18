from flask import Flask, render_template
import os
from web_backend.api.query import api
from Bio import Entrez
import web_backend.config as cfg

base_dir = os.path.dirname(os.path.realpath(__file__))
app = Flask(__name__,
            static_folder=os.path.join(base_dir, "front/static"),
            template_folder=os.path.join("./front"))


app.register_blueprint(api,  url_prefix='/api')


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")


@app.route('/health-check')
def health():
    return "OK"


@app.before_first_request
def startup():
    print ("Starting service!")
    Entrez.email = cfg.MAIL
    Entrez.api_key = cfg.KEY
    Entrez.tool = cfg.TOOL
    print("Started!")

# This is only used when running locally. When running live, gunicorn runs
# the application.
if __name__ == '__main__':
    
    app.run(host='0.0.0.0', port=os.environ.get(
        'BACKEND_PORT', 5001), debug=True)
