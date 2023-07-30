import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref

# db handler
#db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"

    id           = db.Column(db.Integer,
                             db.Sequence("users_id_seq"),
                             primary_key=True)
    email       = db.Column(db.String(62) ,
                             nullable=False, unique=True)
    first_name = db.Column(db.String(32) ,
                             nullable=False)
    last_name = db.Column(db.String(32) ,
                             nullable=False)
    street_name = db.Column(db.String(64) ,
                             nullable=False)
    street_number = db.Column(db.String(16) ,
                             nullable=False)
    zip = db.Column(db.String(5) ,
                             nullable=False)
    city = db.Column(db.String(64) ,
                             nullable=False)
    gender = db.Column(db.String(6) ,
                             nullable=False)
    user_since = db.Column(db.DateTime ,
                             nullable=False)
    is_admin = db.Column(db.Boolean ,
                             nullable=False)
    is_confirmed = db.Column(db.Boolean ,
                             nullable=False)
    hash = db.Column(db.String(256) ,
                             nullable=False)

    def __init__(
        self, email, first_name, last_name, street_name, street_number, zip, city, gender, user_since, hash, is_admin=False, is_confirmed=False
    ):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.street_name = street_name
        self.street_number = street_number
        self.zip = zip
        self.city = city
        self.gender = gender
        self.user_since = user_since
        self.is_admin = is_admin
        self.is_confirmed = is_confirmed
        self.hash = hash


    def __repr__(self):
        return '<User %r>' % self.email



class Booking(db.Model):
    __tablename__ = "bookings"

    id           = db.Column(db.Integer,
                             db.Sequence("bookings_id_seq"),
                             primary_key=True)
    email       = db.Column(db.String(62) ,
                             nullable=False, unique=True)
    court       = db.Column(db.Integer ,
                             nullable=False)
    date        = db.Column(db.Date ,
                             nullable=False)
    start       = db.Column(db.DateTime ,
                             nullable=False)
    end         = db.Column(db.DateTime ,
                             nullable=False)


    def __init__(
        self, email, court, start, end
    ):
        self.email = email
        self.court = court
        self.date = datetime.date.today()
        self.start = start
        self.end = end


    def __repr__(self):
        return f"<Booking: booking_id={self.id}, member={self.email}, court={self.court}, start={self.start}, end={self.end}>"
