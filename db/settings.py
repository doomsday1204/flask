from flask_restful import Api

from main import app
from models.base_class import db

ALLOWED_EXTENSIONS = {'csv'}
UPLOAD_FOLDER = '/path/to/the/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['SQLALCHEMY_DATABASE_URI'] = ''
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)

