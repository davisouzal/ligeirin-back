from flask import Blueprint, jsonify, request
from app.models import SellerProduct, Product, ProductCategory, Seller, SellerProductDetails
from app import db

products_bp = Blueprint('seller_products', __name__, url_prefix='/products')

@products_bp.route('/', methods=['GET'])
def get_all_seller_products():
    """
    Retorna uma lista de todos os produtos de vendedor, incluindo
    informações detalhadas sobre o produto, categoria e vendedor.
    """
    try:
        seller_products = db.session.query(
            SellerProduct, Product, ProductCategory, Seller, SellerProductDetails
        ).join(
            Product, SellerProduct.product_id == Product.id
        ).join(
            ProductCategory, Product.category_id == ProductCategory.id
        ).join(
            Seller, SellerProduct.seller_id == Seller.id
        ).join(
            SellerProductDetails, SellerProduct.id == SellerProductDetails.seller_product_id
        ).all()


        products_list = []
        for sp, p, pc, s, spd in seller_products:
            product_data = {
                "id": sp.id,
                "title": sp.title,
                "price": sp.price,
                "image": sp.image,
                "description": sp.description,
                "care_level": sp.care_level, # sqlite sem o .name, se n for sp.care_level.name
                "product": {
                    "id": p.id,
                    "name": p.name,
                    "category": {
                        "id": pc.id,
                        "name": pc.name
                    }
                },
                "seller": {
                    "id": s.id,
                    "real_name": s.real_name
                },
                "details": {
                    "id": spd.id,
                    "color": spd.color, # sqlite sem o .name, se n for spd.color.name
                    "size": spd.size, # sqlite sem o .name, se n for spd.size.name
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
    Retorna um produto específico de vendedor pelo ID.
    Estrutura:
    {
        "id": ...,
        "title": ...,
        "price": ...,
        "image": ...,
        "description": ...,
        "care_level": ...,
        "product": {
            "id": ...,
            "name": ...,
            "category": {
                "id": ...,
                "name": ...
            }
        },
        "seller": {
            "id": ...,
            "real_name": ...
        },
        "details": [...]
    }
    """
    try:
        sp = db.session.query(SellerProduct).get(product_id)

        if not sp:
            return jsonify({"error": "Produto não encontrado"}), 404

        product_data = {
            "id": sp.id,
            "title": sp.title,
            "price": str(sp.price),
            "image": sp.image,
            "description": sp.description,
            "care_level": sp.care_level,
            "product": {
                "id": sp.product.id,
                "name": sp.product.name,
                "category": {
                    "id": sp.product.category.id,
                    "name": sp.product.category.name
                }
            },
            "seller": {
                "id": sp.seller.id,
                "real_name": sp.seller.real_name
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
    Se passado ?name=<categoria>, retorna apenas aquela.
    Estrutura:
    [
        {
            "name": "Categoria X",
            "products": [...]
        }
    ]
    """
    try:
        category_name = request.args.get("name")

        query = db.session.query(ProductCategory)

        if category_name:
            query = query.filter(ProductCategory.name.ilike(f"%{category_name}%"))

        categories = query.all()

        result = []
        for category in categories:
            products_list = []
            for product in category.products:
                for sp in product.seller_products:
                    product_data = {
                        "id": sp.id,
                        "title": sp.title,
                        "price": str(sp.price),
                        "image": sp.image,
                        "description": sp.description,
                        "care_level": sp.care_level,
                        "seller": {
                            "id": sp.seller.id,
                            "real_name": sp.seller.real_name
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
                "name": category.name,
                "products": products_list
            })

        return jsonify(result), 200

    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500

