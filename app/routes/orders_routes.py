from flask import Blueprint, jsonify, request
from app.models import Client, Order, OrderProduct, SellerProduct, Product, ProductCategory, Seller, SellerProductDetails
from app import db
from datetime import datetime

orders_bp = Blueprint('orders', __name__, url_prefix='/orders')

@orders_bp.route('/client/<int:client_id>', methods=['GET'])
def get_all_clients_orders(client_id):
    """
    Retorna todos os pedidos de um cliente específico,
    incluindo os produtos, vendedor, categoria e detalhes.
    """
    try:
        client = Client.query.get(client_id)
        if not client:
            return jsonify({"error": "Cliente não encontrado"}), 404

        orders_data = []
        for order in client.orders:
            if order.status == "DRAFT":
                continue

            order_info = {
                "id": order.id,
                "totalPrice": float(order.total_price),
                "paymentMethod": order.payment_method,
                "status": order.status,
                "completeDate": order.complete_date,
                "createdAt": order.created_at,
                "products": []
            }

            for op in order.order_products:
                sp = op.seller_product
                product_info = {
                    "id": sp.id,
                    "title": sp.title,
                    "price": float(sp.price),
                    "quantity": op.quantity,
                    "description": sp.description,
                    "careLevel": sp.care_level,
                    "image": sp.image,
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
                            "id": d.id,
                            "color": d.color,
                            "size": d.size,
                            "stock": d.stock
                        } for d in sp.details
                    ]
                }
                order_info["products"].append(product_info)

            orders_data.append(order_info)

        return jsonify(orders_data), 200

    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500

@orders_bp.route('/<int:order_id>', methods=['GET'])
def get_order_by_id(order_id):
    order = (
        db.session.query(Order)
        .filter(Order.id == order_id)
        .first()
    )

    if not order:
        return jsonify({"message": "Pedido não encontrado"}), 404

    products = []
    for op in order.order_products:
        sp = op.seller_product
        products.append({
            "id": sp.id,
            "title": sp.title,
            "brand": sp.brand,
            "price": float(sp.price),
            "quantity": op.quantity,
            "seller": {
                "sellerId": sp.seller.id,
                "userId": sp.seller.user.id,
                "image": sp.seller.user.image,
                "fantasyName": sp.seller.user.name,
                "companyName": sp.seller.company_name
            },
            "details": [
                {
                    "color": d.color,
                    "size": d.size,
                    "stock": d.stock
                }
                for d in sp.details
            ]
        })

    result = {
        "orderId": order.id,
        "status": order.status,
        "clientId": order.client_id,
        "createdAt": order.created_at,
        "completeDate": order.complete_date,
        "products": products
    }

    return jsonify(result), 200

@orders_bp.route('/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    """
    Atualiza o status e as informações de pagamento um pedido existente.
    """
    try:
        order = db.session.query(Order).get(order_id)
        if not order:
            return jsonify({"error": "Pedido não encontrado"}), 404

        if order.status == "COMPLETED":
            return jsonify({"error": "Não é possível alterar pedidos já completados"}), 403

        data = request.get_json()

        status = data.get("status")
        payment_method = data.get("paymentMethod")
        if status:
            order.status = status
            if status == "ON GOING":
                order.complete_date = datetime.now()
        if payment_method:
            order.payment_method = payment_method

        db.session.commit()

        return jsonify({"message": "Pedido atualizado com sucesso", "orderId": order.id}), 200

    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({"error": str(e)}), 500