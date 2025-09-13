from flask import jsonify, Blueprint
from .products_routes import products_bp

main_bp = Blueprint('main', __name__, url_prefix='/api')

def register_routes(app):
    """
    Registra todos os Blueprints da aplicação Flask.
    """
    # Rota principal para teste
    @main_bp.route('/')
    def home():
        return jsonify({"message": "API rodando 🚀"})

    # Registro dos Blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(products_bp)
