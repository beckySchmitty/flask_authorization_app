from app import app
from models import db, User, Feedback


db.drop_all()
db.create_all()

u1 = User(username="BoJack", password="password", email="fakeemail@email.com", first_name="BoJack", last_name="Horseman")
u2 = User(username="ByeDon2020", password="password2", email="fakeemail2@email.com", first_name="Joe", last_name="Biden")
u3 = User(username="GusTheCat", password="password3", email="fakeemail3@email.com", first_name="Gus", last_name="Gear")

db.session.add_all([u1, u2, u3])
db.session.commit()


f1 = Feedback(title="Back in the 90s", content="I was in a very famous tvvvvv show", username="BoJack")
f2 = Feedback(title="Thoughts", content="I have a great show on netflix", username="BoJack")
f3 = Feedback(title="WE DID IT", content="President Eelect", username="ByeDon2020")
f4 = Feedback(title="I am a cat", content="My name is Gus", username="GusTheCat")


db.session.add_all([f1, f2, f3, f4])
db.session.commit()