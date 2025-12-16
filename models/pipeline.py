from database import db
from geoalchemy2 import Geometry

class Pipeline(db.Model):
    __tablename__ = "pipelines"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)

    geometry = db.Column(
        Geometry("LINESTRING", srid=4326),
        nullable=False
    )

    max_pressure = db.Column(db.Float, nullable=False)
    commissioning_year = db.Column(db.Integer, nullable=False)
