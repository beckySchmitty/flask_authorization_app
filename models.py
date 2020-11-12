from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

db = SQLAlchemy()

def connect_db(app):
        """connect to database"""
        db.app = app
        db.init_app(app)


class User(db.Model):
    __tablename__ = 'users'

    username = db.Column(db.String(20), nullable=False, unique=True, primary_key=True) 
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)

    feedback = db.relationship('Feedback', backref='users', cascade="all,delete")

    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """register user in db, return user"""

        # generate utf8 password for database
        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode("utf8")

        new_user = cls(
            username=username,
            password=hashed_utf8,
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        # save to database
        db.session.add(new_user)
        db.session.commit()
        return new_user

    @classmethod
    def authenticate(cls, username, password):
            """Check user input password with hashed password in db"""

            user = User.query.filter_by(username=username).first()

            if (bcrypt.check_password_hash(user.password, password)):
                return True
            else:
                False

class Feedback(db.Model):
        __tablename__ = "feedback"

        id = db.Column(db.Integer, primary_key=True, autoincrement=True)
        title = db.Column(db.String(100), nullable=False)
        content = db.Column(db.String, nullable=False)
        username = db.Column(db.String(20), db.ForeignKey('users.username'), nullable=False)
    
