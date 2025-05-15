from io import BytesIO

import pandas as pd
from flask import Blueprint, jsonify
from flask import request, send_file
from flask_jwt_extended import jwt_required

from app.models.inspection import Inspection
from app.usecases.analytics.get_analytics_summary import GetAnalyticsSummaryUseCase
from app.utils.auth import get_current_user

analytics_bp = Blueprint("analytics", __name__, url_prefix="/analytics")


@analytics_bp.route("/summary", methods=["GET"])
@jwt_required()
def get_summary():
    try:
        result = GetAnalyticsSummaryUseCase.execute()
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@analytics_bp.route("/export", methods=["GET"])
@jwt_required()
def export_analytics():
    try:
        format = request.args.get("format", "excel")
        user = get_current_user()

        inspections = (
            Inspection.query
            .join(Inspection.product)
            .filter(Inspection.product.has(client_id=user.client_id))
            .all()
        )

        data = []
        for i in inspections:
            data.append({
                "inspection_id": i.id,
                "product_id": i.product_id,
                "result": i.result,
                "inspected_at": i.inspected_at.strftime("%Y-%m-%d %H:%M"),
                "user_id": i.client_id,
                "defects": len(i.defects)
            })

        df = pd.DataFrame(data)

        output = BytesIO()
        if format == "excel":
            df.to_excel(output, index=False)
            output.seek(0)
            return send_file(output, download_name="analytics.xlsx", as_attachment=True)
        elif format == "pdf":
            # (PDF реализация позже, например через ReportLab)
            return jsonify({"error": "PDF export not implemented yet"}), 501
        else:
            return jsonify({"error": "Invalid format"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500
