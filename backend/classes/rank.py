from config import *

class Rank(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer)

    def __str__(self):
        return f"ID: {self.id}, Pontos: {self.score}"

    def json(self):
        return {
            "id": self.id,
            "pontos": self.score
        }