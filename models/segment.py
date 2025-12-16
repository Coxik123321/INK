from app import db

class Segment(db.Model):
    __tablename__ = "segments"

    id = db.Column(db.Integer, primary_key=True)
    lat = db.Column(db.Float, nullable=False)
    lon = db.Column(db.Float, nullable=False)

    priority = db.Column(db.Float, nullable=False)
    risk_level = db.Column(db.String(50))
    remaining_life = db.Column(db.Float)
    corrosion_rate = db.Column(db.Float, nullable=False)
    age_years = db.Column(db.Integer, nullable=False)
    operating_pressure = db.Column(db.Float, nullable=False)
    max_pressure = db.Column(db.Float, nullable=False)
    length_km = db.Column(db.Float, nullable=False)
    
    recommended_action = db.Column(db.String(64))
    decision_risk = db.Column(db.Float)
    decision_cost = db.Column(db.Float)

    estimated_cost = db.Column(db.Float)
    recommended_action = db.Column(db.String(255))
    depth = db.Column(db.Float)               # глубина дефекта
    corrosion_rate = db.Column(db.Float)      # мм/год
    wall_thickness = db.Column(db.Float) 
    def to_feature(self):
        return {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [self.lon, self.lat]
            },
            "properties": {
                "segment_id": self.id,
                "priority": self.priority,
                "risk_level": self.risk_level,
                "remaining_life": self.remaining_life,
                "estimated_cost": self.estimated_cost,
                "action": self.recommended_action
            }
        }
