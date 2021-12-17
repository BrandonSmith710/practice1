from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()

class Day(DB.Model):
    id = DB.Column(DB.BigInteger, primary_key=True, nullable=False)
    min_temp = DB.Column(DB.Float, nullable=False)
    max_temp = DB.Column(DB.Float, nullable=False)
    date = DB.Column(DB.String, nullable=False)

