from app import db

class Contact_form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(30), nullable=False)
    phone_number = db.Column(db.String(30), nullable=False)
    message = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(30), nullable=False)