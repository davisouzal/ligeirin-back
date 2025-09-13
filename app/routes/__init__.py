from flask import jsonify, Blueprint
from .products_routes import products_bp
from.orders_routes import orders_bp
from .clients_routes import clients_bp
from .cart_routes import cart_bp
from .categories_routes import categories_bp

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
    app.register_blueprint(orders_bp)
    app.register_blueprint(clients_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(categories_bp)
    
