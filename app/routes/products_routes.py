from flask import Blueprint, jsonify
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
                "description": sp.description,
                "care_level": sp.care_level.name,
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
                    "color": spd.color.name,
                    "size": spd.size.name,
                    "stock": spd.stock,
                    "price": float(spd.price)
                }
            }
            products_list.append(product_data)

        return jsonify(products_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
