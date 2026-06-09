from flask import Flask

from flask_cors import CORS
import os
import models.cloudinary_config


from db import *
from util.blueprints import register_blueprint

# flask_host = os.environ.get("FLASK_HOST")
# flask_port = os.environ.get("FLASK_PORT")

# database_scheme = os.environ.get("DATABASE_SCHEME")
# database_user = os.environ.get("DATABASE_USER")
# database_address = os.environ.get("DATABASE_ADDRESS")
# database_port = os.environ.get("DATABASE_PORT")
# database_name = os.environ.get("DATABASE_NAME")

app = Flask(__name__)
# CORS(app)
CORS(
    app,
    resources={r"/*": {"origins": "*"}},
    supports_credentials=True,
    allow_headers=["Content-Type", "Authorization"],
    methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
)

@app.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET,POST,PUT,DELETE,OPTIONS")
    return response

@app.route("/", methods=["GET", "POST", "OPTIONS"])
def health():
    return "OK"

register_blueprint(app)
database_url = os.environ.get("DATABASE_URL")

if database_url.startswith("postgres://"):
    database_url = database_url.replace(
        "postgres://",
        "postgresql://",
        1
    )

app.config["SQLALCHEMY_DATABASE_URI"] = database_url + "?sslmode=require"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# CORS(
#     app,
#     resources={r"/*": {"origins": "http://localhost:5173"}},
#     supports_credentials=True,
#     allow_headers=["Content-Type", "Authorization"],
#     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
# )

# app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
# app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

init_db(app, db)



def create_tables():
    with app.app_context():
        print("Creating tables...")
        db.create_all()
        print("Tables created successfully")


if __name__ == '__main__':
    # create_tables()
    port = int(os.environ.get("PORT", 5000)) 
    with app.app_context():
        create_tables()
    # app.run(host=flask_host, port=flask_port)
    app.run(host="0.0.0.0", port=port)