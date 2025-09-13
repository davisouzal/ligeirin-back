from flask import Blueprint, jsonify
from app.models import ProductCategory
from app import db

categories_bp = Blueprint('categories', __name__, url_prefix='/categories')

@categories_bp.route('/', methods=['GET'])
def get_all_categories():
    """
    Retorna todas as categorias cadastradas
    """
    try:
        categories = db.session.query(ProductCategory).all()

        result = []
        for category in categories:
            result.append({
                "id": category.id,
                "name": category.name,
                "icon": category.icon
            })

        return jsonify(result), 200

    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500
