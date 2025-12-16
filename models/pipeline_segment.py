from database import db
from geoalchemy2 import Geometry

class PipelineSegment(db.Model):
    __tablename__ = "pipeline_segments"

    id = db.Column(db.Integer, primary_key=True)
    pipeline_id = db.Column(db.Integer, db.ForeignKey("pipelines.id"))

    geometry = db.Column(
        Geometry("LINESTRING", srid=4326),
        nullable=False
    )

    corrosion_rate = db.Column(db.Float, nullable=False)
    operating_pressure = db.Column(db.Float, nullable=False)
    length_km = db.Column(db.Float, nullable=False)

    risk = db.Column(db.Float)
    recommended_action = db.Column(db.String(64))
