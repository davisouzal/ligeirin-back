from flask import Blueprint, jsonify, request
from app.models import SellerProduct, Product, ProductCategory, Seller, SellerProductDetails, User
from app import db

products_bp = Blueprint('seller_products', __name__, url_prefix='/products')

@products_bp.route('/', methods=['GET'])
def get_all_seller_products():
    """
    Retorna todos os produtos de vendedores, incluindo produto, categoria, vendedor e user.
    """
    try:
        seller_products = (
            db.session.query(SellerProduct)
            .join(Product, SellerProduct.product_id == Product.id)
            .join(ProductCategory, Product.category_id == ProductCategory.id)
            .join(Seller, SellerProduct.seller_id == Seller.id)
            .join(User, Seller.user_id == User.id)
            .join(SellerProductDetails, SellerProduct.id == SellerProductDetails.seller_product_id)
            .all()
        )

        products_list = []
        for sp in seller_products:
            for spd in sp.details:
                product_data = {
                    "id": sp.id,
                    "title": sp.title,
                    "price": float(sp.price),
                    "image": sp.image,
                    "description": sp.description,
                    "careLevel": sp.care_level,
                    "product": {
                        "id": sp.product.id,
                        "name": sp.product.name,
                        "category": {
                            "id": sp.product.category.id,
                            "name": sp.product.category.name
                        }
                    },
                    "seller": {
                        "sellerId": sp.seller.id,
                        "userId": sp.seller.user.id,
                        "image": sp.seller.user.image,
                        "fantasyName": sp.seller.user.name,
                        "companyName": sp.seller.company_name
                    },
                    "details": {
                        "id": spd.id,
                        "color": spd.color,
                        "size": spd.size,
                        "stock": spd.stock,
                    }
                }
                products_list.append(product_data)

        return jsonify(products_list), 200
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500
    

@products_bp.route('/<int:product_id>', methods=['GET'])
def get_product_by_id(product_id):
    """
    Retorna um produto de vendedor específico pelo ID.
    """
    try:
        sp = db.session.query(SellerProduct).get(product_id)

        if not sp:
            return jsonify({"error": "Produto não encontrado"}), 404

        product_data = {
            "id": sp.id,
            "title": sp.title,
            "price": float(sp.price),
            "image": sp.image,
            "description": sp.description,
            "careLevel": sp.care_level,
            "product": {
                "id": sp.product.id,
                "name": sp.product.name,
                "category": {
                    "id": sp.product.category.id,
                    "name": sp.product.category.name
                }
            },
            "seller": {
                "sellerId": sp.seller.id,
                "userId": sp.seller.user.id,
                "image": sp.seller.user.image,
                "fantasyName": sp.seller.user.name,
                "companyName": sp.seller.company_name
            },
            "details": [
                {
                    "id": detail.id,
                    "color": detail.color,
                    "size": detail.size,
                    "stock": detail.stock
                }
                for detail in sp.details
            ]
        }

        return jsonify(product_data), 200

    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500


@products_bp.route('/category', methods=['GET'])
def get_products_by_category():
    """
    Retorna produtos agrupados por categoria.
    Se passado ?categoryId=<id>, retorna apenas aquela categoria.
    """
    try:
        category_id = request.args.get("categoryId", type=int)

        query = db.session.query(ProductCategory)
        if category_id:
            query = query.filter(ProductCategory.id == category_id)

        categories = query.all()

        result = []
        for category in categories:
            products_list = []
            for product in category.products:
                for sp in product.seller_products:
                    product_data = {
                        "id": sp.id,
                        "title": sp.title,
                        "price": float(sp.price),
                        "image": sp.image,
                        "description": sp.description,
                        "careLevel": sp.care_level,
                        "seller": {
                            "sellerId": sp.seller.id,
                            "userId": sp.seller.user.id,
                            "image": sp.seller.user.image,
                            "fantasyName": sp.seller.user.name,
                            "companyName": sp.seller.company_name
                        },
                        "details": [
                            {
                                "id": detail.id,
                                "color": detail.color,
                                "size": detail.size,
                                "stock": detail.stock
                            }
                            for detail in sp.details
                        ]
                    }
                    products_list.append(product_data)

            result.append({
                "id": category.id,
                "name": category.name,
                "products": products_list
            })

        return jsonify(result), 200

    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500
