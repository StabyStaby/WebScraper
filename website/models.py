from sqlalchemy import func
from . import db

class Manga(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(200))
    lastChapterDate = db.Column(db.DateTime())
    url = db.Column(db.String(200))
    nrOfChapters = db.Column(db.Integer)
    imgUrl = db.Column(db.String(200))
    userId = db.Column(db.Integer,db.ForeignKey('user.id'))

class User(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    discordId = db.Column(db.Integer)
    name = db.Column(db.String(200))
    manga = db.relationship('Manga')