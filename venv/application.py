import warnings
from flask import Flask, render_template, request
from genral import disease
# from genral import genral
from search import gsearch

warnings.filterwarnings('ignore')
# download
application = Flask(__name__)

application.register_blueprint(disease, url_prefix="/d")
# app.register_blueprint(gsearch,url_prefix="/gsearch")
# app.register_blueprint(disease, url_prefix="/d")

@application.route("/")
def home():

    return render_template("index1.html")


if __name__ == "__main__":
    application.run(debug=True)  # debug=True
