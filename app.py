from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from api.segments import segments_api
from api.auth import auth_api
from api.simulation import simulation_api
from api.defects import defects_api
from api.budget import budget_api
from api.analytics import analytics_api
from api.report import report_api
from api.decision import decision_api
from api.pipelines import pipelines_api

app = Flask(__name__, static_folder="frontend", static_url_path="")
CORS(app)


jwt = JWTManager(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///pipeline.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "CHANGE_ME_SUPER_SECRET"
db = SQLAlchemy(app)

# =========================
# Регистрация API
# =========================
app.register_blueprint(segments_api, url_prefix="/api")
app.register_blueprint(simulation_api, url_prefix="/api")
app.register_blueprint(auth_api, url_prefix="/api")
app.register_blueprint(defects_api, url_prefix="/api")
app.register_blueprint(budget_api, url_prefix="/api")
app.register_blueprint(analytics_api, url_prefix="/api")
app.register_blueprint(report_api, url_prefix="/api")
app.register_blueprint(decision_api, url_prefix="/api")
app.register_blueprint(pipelines_api, url_prefix="/api")

# =========================
# Frontend
# =========================
@app.route("/")
def index():
    return send_from_directory("frontend", "map.html")

# =========================
# Run
# =========================
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000, debug=True)






# # app.py
# from flask import Flask, jsonify, request
# from flask_sqlalchemy import SQLAlchemy
# from flask_cors import CORS
# from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
# from werkzeug.security import generate_password_hash, check_password_hash
# from datetime import timedelta

# import os
# from flask import send_from_directory

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# app = Flask(
#     __name__,
#     static_folder="frontend",
#     static_url_path=""
# )
# CORS(app)

# # ========== CONFIG ==========
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pipeline.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['JWT_SECRET_KEY'] = 'CHANGE_THIS_SUPER_SECRET'  # поменяй в проде
# app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=8)

# db = SQLAlchemy(app)
# jwt = JWTManager(app)

# # ========== MODELS ==========
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     password_hash = db.Column(db.String(255), nullable=False)
#     role = db.Column(db.String(20), default="viewer")

#     def set_password(self, password):
#         self.password_hash = generate_password_hash(password)

#     def check_password(self, password):
#         return check_password_hash(self.password_hash, password)


# class Segment(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     lat = db.Column(db.Float, nullable=False)       # latitude
#     lon = db.Column(db.Float, nullable=False)       # longitude
#     priority = db.Column(db.Float, nullable=False)  # 0..1
#     estimated_cost = db.Column(db.Float, default=0)
#     action = db.Column(db.String(255), default="")

#     def to_geojson(self):
#         return {
#             "type": "Feature",
#             "geometry": {"type": "Point", "coordinates": [self.lon, self.lat]},
#             "properties": {
#                 "segment_id": self.id,
#                 "priority": self.priority,
#                 "estimated_cost": self.estimated_cost,
#                 "action": self.action
#             }
#         }

# # ========== HELPERS ==========
# def is_admin():
#     ident = get_jwt_identity()
#     if not ident:
#         return False
#     return ident.get("role") == "admin"

# # ========== AUTH ==========
# @app.route('/api/login', methods=['POST'])
# def login():
#     payload = request.get_json() or {}
#     username = payload.get('username')
#     password = payload.get('password')
#     if not username or not password:
#         return jsonify({"error": "username and password required"}), 400

#     user = User.query.filter_by(username=username).first()
#     if not user or not user.check_password(password):
#         return jsonify({"error": "invalid credentials"}), 401

#     token = create_access_token(identity={"id": user.id, "username": user.username, "role": user.role})
#     return jsonify({"access_token": token})

# @app.route('/api/register', methods=['POST'])
# def register():
#     # endpoint for creating users (only for initial use; lock down in prod)
#     payload = request.get_json() or {}
#     username = payload.get('username')
#     password = payload.get('password')
#     role = payload.get('role', 'viewer')
#     if not username or not password:
#         return jsonify({"error": "username and password required"}), 400
#     if User.query.filter_by(username=username).first():
#         return jsonify({"error": "username exists"}), 400
#     u = User(username=username, role=role)
#     u.set_password(password)
#     db.session.add(u)
#     db.session.commit()
#     return jsonify({"status": "created", "username": username})

# # ========== SEGMENTS CRUD (GeoJSON for GET) ==========
# @app.route('/api/segments', methods=['GET'])
# def api_get_segments():
#     segments = Segment.query.all()
#     return jsonify({
#         "type": "FeatureCollection",
#         "features": [s.to_geojson() for s in segments]
#     })

# @app.route('/api/segments', methods=['POST'])
# @jwt_required()
# def api_post_segment():
#     if not is_admin():
#         return jsonify({"error": "admin required"}), 403
#     data = request.get_json() or {}
#     # validation
#     try:
#         lat = float(data['lat']); lon = float(data['lon']); priority = float(data['priority'])
#     except Exception:
#         return jsonify({"error": "lat, lon, priority required and numeric"}), 400
#     seg = Segment(
#         lat=lat, lon=lon, priority=priority,
#         estimated_cost=float(data.get('estimated_cost', 0)),
#         action=str(data.get('action', ''))
#     )
#     db.session.add(seg)
#     db.session.commit()
#     return jsonify({"status": "created", "id": seg.id}), 201

# @app.route('/api/segments/<int:seg_id>', methods=['PUT'])
# @jwt_required()
# def api_put_segment(seg_id):
#     if not is_admin():
#         return jsonify({"error": "admin required"}), 403
#     seg = Segment.query.get_or_404(seg_id)
#     data = request.get_json() or {}
#     if 'lat' in data: seg.lat = float(data['lat'])
#     if 'lon' in data: seg.lon = float(data['lon'])
#     if 'priority' in data: seg.priority = float(data['priority'])
#     if 'estimated_cost' in data: seg.estimated_cost = float(data['estimated_cost'])
#     if 'action' in data: seg.action = str(data['action'])
#     db.session.commit()
#     return jsonify({"status": "updated"})

# @app.route('/api/segments/<int:seg_id>', methods=['DELETE'])
# @jwt_required()
# def api_delete_segment(seg_id):
#     if not is_admin():
#         return jsonify({"error": "admin required"}), 403
#     seg = Segment.query.get_or_404(seg_id)
#     db.session.delete(seg)
#     db.session.commit()
#     return jsonify({"status": "deleted"})

# # ========== ANALYTICS ENDPOINTS ==========
# @app.route('/api/analytics/summary', methods=['GET'])
# def analytics_summary():
#     total = Segment.query.count()
#     if total == 0:
#         return jsonify({"total_segments": 0, "total_cost": 0, "avg_priority": 0})
#     total_cost = db.session.query(db.func.sum(Segment.estimated_cost)).scalar() or 0
#     avg_priority = float(db.session.query(db.func.avg(Segment.priority)).scalar() or 0)
#     return jsonify({
#         "total_segments": total,
#         "total_cost": float(total_cost),
#         "avg_priority": avg_priority
#     })

# @app.route('/api/analytics/by_priority', methods=['GET'])
# def analytics_by_priority():
#     # buckets: low <=0.4, medium (0.4,0.7], high >0.7
#     low = Segment.query.filter(Segment.priority <= 0.4).count()
#     medium = Segment.query.filter(Segment.priority > 0.4, Segment.priority <= 0.7).count()
#     high = Segment.query.filter(Segment.priority > 0.7).count()
#     return jsonify({"low": low, "medium": medium, "high": high})

# @app.route('/api/analytics/value_by_action', methods=['GET'])
# def analytics_value_by_action():
#     rows = db.session.query(Segment.action, db.func.sum(Segment.estimated_cost).label('sum_cost')) \
#         .group_by(Segment.action).all()
#     return jsonify([{ "action": r[0] or "", "sum_cost": float(r[1] or 0) } for r in rows])

# @app.route('/api/analytics/top_costs', methods=['GET'])
# def analytics_top_costs():
#     n = int(request.args.get('n', 10))
#     rows = Segment.query.order_by(Segment.estimated_cost.desc()).limit(n).all()
#     result = [{
#         "id": r.id, "lat": r.lat, "lon": r.lon, "priority": r.priority, "estimated_cost": r.estimated_cost, "action": r.action
#     } for r in rows]
#     return jsonify(result)

# @app.route('/api/analytics/heatmap', methods=['GET'])
# def analytics_heatmap():
#     # return FeatureCollection with weight property (use priority as weight)
#     features = []
#     for s in Segment.query.all():
#         features.append({
#             "type": "Feature",
#             "geometry": {"type": "Point", "coordinates": [s.lon, s.lat]},
#             "properties": {"weight": float(s.priority), "estimated_cost": float(s.estimated_cost)}
#         })
#     return jsonify({"type": "FeatureCollection", "features": features})

# # ========== DB INIT + ADMIN ==========
# with app.app_context():
#     db.create_all()
#     if User.query.filter_by(username="admin").first() is None:
#         admin = User(username="admin", role="admin")
#         admin.set_password("admin123")   # поменяй пароль
#         db.session.add(admin)
#     if Segment.query.count() == 0:
#         db.session.add_all([
#             Segment(lat=55.75, lon=37.61, priority=0.9, estimated_cost=100000, action="Repair"),
#             Segment(lat=56.0, lon=38.0, priority=0.5, estimated_cost=50000, action="Inspection"),
#             Segment(lat=55.5, lon=37.0, priority=0.2, estimated_cost=20000, action="Monitor")
#         ])
#     db.session.commit()

# # =======================
# # Frontend routes
# # =======================
# @app.route("/")
# def index():
#     return send_from_directory(app.static_folder, "map.html")

# @app.route("/<path:path>")
# def static_files(path):
#     return send_from_directory(app.static_folder, path)

# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=5000)
