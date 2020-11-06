from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
# includes driver


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False, unique=True, primary_key=True) 
    # password
    # email
    # first_name
    # last_name


    
    
def connect_db(app):
        """connect to database"""
        db.app = app
        db.init_app(app)