from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Users(db.model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

    # Represent object as a string
    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


