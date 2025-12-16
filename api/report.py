from flask import Blueprint, send_file
from flask_jwt_extended import jwt_required
from services.report_service import generate_report

report_api = Blueprint("report_api", __name__)

@report_api.route("/report/pdf", methods=["GET"])
@jwt_required()
def report():
    path = "pipeline_report.pdf"
    generate_report(path)
    return send_file(path, as_attachment=True)
