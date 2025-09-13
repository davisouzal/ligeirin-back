from flask import Blueprint, jsonify, request
from app.models import Client, Order, OrderProduct
from app import db
from datetime import datetime

cart_bp = Blueprint('cart', __name__, url_prefix='/cart')


@cart_bp.route('/client/<int:client_id>', methods=['GET'])
def get_client_cart(client_id):
    """
    Retorna a primeira Order em DRAFT de um cliente específico,
    incluindo os produtos, vendedor e detalhes.
    """
    try:
        client = db.session.query(Client).get(client_id)
        if not client:
            return jsonify({"error": "Cliente não encontrado"}), 404

        draft_order = (
            db.session.query(Order)
            .filter(Order.client_id == client_id, Order.status == "DRAFT")
            .order_by(Order.created_at.asc())
            .first()
        )

        if not draft_order:
            return jsonify({"message": "Nenhum carrinho encontrado"}), 404
        
        seller = {}

        products = []
        for op in draft_order.order_products:
            sp = op.seller_product
            seller = {
                "id": sp.seller.id,
                "userId": sp.seller.user.id,
                "image": sp.seller.user.image,
                "fantasyName": sp.seller.user.name,
                "companyName": sp.seller.company_name
            }
            products.append({
                "id": sp.id,
                "title": sp.title,
                "brand": sp.brand,
                "price": float(sp.price),
                "quantity": op.quantity,
                "image": sp.image,
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
            "id": draft_order.id,
            "totalPrice": float(draft_order.total_price),
            "status": draft_order.status,
            "userId": draft_order.client.user.id,
            "clientId": draft_order.client_id,
            "createdAt": draft_order.created_at,
            "products": products,
            "seller": seller
        }

        return jsonify(result), 200

    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500
    
@cart_bp.route('/client/<int:client_id>', methods=['PUT'])
def update_client_cart(client_id):
    """
    Atualiza ou cria a Order em DRAFT de um cliente,
    adicionando ou atualizando os produtos do carrinho.
    """
    try:
        client = db.session.query(Client).get(client_id)
        if not client:
            return jsonify({"error": "Cliente não encontrado"}), 404

        data = request.get_json()
        products_data = request.get_json()
        if not products_data or not isinstance(products_data, list):
            return jsonify({"error": "Envie uma lista de produtos"}), 400

        draft_order = (
            db.session.query(Order)
            .filter(Order.client_id == client_id, Order.status == "DRAFT")
            .order_by(Order.created_at.desc())
            .first()
        )

        if not draft_order:
            draft_order = Order(
                client_id=client_id,
                total_price=0,
                status="DRAFT",
            )
            db.session.add(draft_order)
            db.session.commit()

        for item in products_data:
            seller_product_id = item.get("seller_product_id")
            quantity = item.get("quantity", 1)

            if not seller_product_id:
                continue

            order_product = (
                db.session.query(OrderProduct)
                .filter_by(order_id=draft_order.id, seller_product_id=seller_product_id)
                .first()
            )

            if order_product:
                order_product.quantity = quantity
            else:
                new_order_product = OrderProduct(
                    order_id=draft_order.id,
                    seller_product_id=seller_product_id,
                    quantity=quantity
                )
                db.session.add(new_order_product)

        db.session.commit()

        total = 0
        for op in draft_order.order_products:
            total += float(op.seller_product.price) * op.quantity
        draft_order.total_price = total
        db.session.commit()

        return jsonify({"message": "Carrinho atualizado com sucesso", "orderId": draft_order.id}), 200

    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    
@cart_bp.route('/<int:order_id>/product/<int:product_id>', methods=['DELETE'])
def delete_product_from_cart(order_id, product_id):
    """
    Remove um produto específico do carrinho (Order em DRAFT).
    Se não houver mais produtos, exclui a Order.
    """
    try:
        order = (
            db.session.query(Order)
            .filter_by(id=order_id)
            .first()
        )

        if order.status != "DRAFT":
            return jsonify({"error": "Apenas carrinhos podem ter seus produtos retirados"}), 403

        order_product = (
            db.session.query(OrderProduct)
            .filter_by(order_id=order_id, seller_product_id=product_id)
            .first()
        )

        if not order_product:
            return jsonify({"error": "Produto não encontrado no carrinho"}), 404

        db.session.delete(order_product)
        db.session.commit()

        remaining_products = db.session.query(OrderProduct).filter_by(order_id=order_id).count()

        if remaining_products == 0:
            order = db.session.query(Order).get(order_id)
            if order:
                db.session.delete(order)
                db.session.commit()
                return jsonify({"message": "Produto removido e carrinho excluído"}), 200

        return jsonify({"message": "Produto removido do carrinho"}), 200

    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

