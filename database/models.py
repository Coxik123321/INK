from datetime import datetime
from database.db import db


class Segment(db.Model):
    __tablename__ = "segments"

    id = db.Column(db.Integer, primary_key=True)

    lat = db.Column(db.Float, nullable=False)
    lon = db.Column(db.Float, nullable=False)

    defect_type = db.Column(db.String(50), nullable=False)

    records = db.relationship(
        "DefectRecord",
        backref="segment",
        cascade="all, delete-orphan",
        lazy=True
    )

    def to_geojson(self, latest_record=None):
        record = latest_record or (self.records[-1] if self.records else None)

        return {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [self.lon, self.lat]
            },
            "properties": {
                "segment_id": self.id,
                "defect_type": self.defect_type,
                "priority": record.priority if record else None,
                "pressure": record.pressure if record else None,
                "estimated_cost": record.estimated_cost if record else None,
                "action": record.action if record else None,
                "date": record.date.isoformat() if record else None
            }
        }


class DefectRecord(db.Model):
    __tablename__ = "defect_records"

    id = db.Column(db.Integer, primary_key=True)

    segment_id = db.Column(
        db.Integer,
        db.ForeignKey("segments.id"),
        nullable=False
    )

    date = db.Column(db.DateTime, default=datetime.utcnow)

    priority = db.Column(db.Float, nullable=False)
    pressure = db.Column(db.Float)
    estimated_cost = db.Column(db.Float)
    action = db.Column(db.String(255))
