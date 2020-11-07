from app import app
from models import db, User


db.drop_all()
db.create_all()

u1 = User(username="BoJack", password="password", email="fakeemail@email.com", first_name="BoJack", last_name="Horseman")
u2 = User(username="ByeDon2020", password="password2", email="fakeemail2@email.com", first_name="Joe", last_name="Biden")
u3 = User(username="GusTheCat", password="password3", email="fakeemail3@email.com", first_name="Gus", last_name="Gear")


db.session.add_all([u1, u2, u3])
db.session.commit()