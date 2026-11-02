from flask import Flask
from flask_cors import CORS

from config.settings import settings
from routes.auth import auth_bp
from routes.data import data_bp


app = Flask(__name__)
app.config['SECRET_KEY'] = settings.SECRET_KEY
CORS(app, resources={r'/api/*': {'origins': '*'}})

app.register_blueprint(auth_bp)
app.register_blueprint(data_bp)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
