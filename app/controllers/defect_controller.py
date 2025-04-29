from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from app.models.defect import Defect
from app.models.inspection import Inspection
from app.utils.auth import get_current_user

defects_bp = Blueprint("defects", __name__, url_prefix="/defects")


@defects_bp.route("/", methods=["GET"])
@jwt_required()
def list_defects():
    user = get_current_user()
    query = Defect.query.join(Defect.inspection).join(Inspection.product)
    query = query.filter(Inspection.product.has(client_id=user.client_id))

    product_id = request.args.get("product_id", type=int)
    min_conf = request.args.get("min_conf", type=float)
    max_conf = request.args.get("max_conf", type=float)
    date_from = request.args.get("date_from")
    date_to = request.args.get("date_to")

    if product_id:
        query = query.filter(Inspection.product_id == product_id)
    if min_conf is not None:
        query = query.filter(Defect.confidence >= min_conf)
    if max_conf is not None:
        query = query.filter(Defect.confidence <= max_conf)
    if date_from:
        query = query.filter(Inspection.inspected_at >= date_from)
    if date_to:
        query = query.filter(Inspection.inspected_at <= date_to)

    defects = query.all()
    return jsonify([
        {
            "id": d.id,
            "label": d.label,
            "confidence": d.confidence,
            "x": d.x,
            "y": d.y,
            "width": d.width,
            "height": d.height,
            "inspection_id": d.inspection_id
        } for d in defects
    ])
