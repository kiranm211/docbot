import warnings
from flask import Flask, render_template, request
from disease import disease
# from genral import genral

warnings.filterwarnings('ignore')
# download
app = Flask(__name__)
app.register_blueprint(disease, url_prefix="")
# app.register_blueprint(genral, url_prefix="")


@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)  # debug=True
