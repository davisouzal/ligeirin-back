from flask import Blueprint, jsonify
from app.models import Client, User, CardInfo
from app import db

clients_bp = Blueprint('clients', __name__, url_prefix='/clients')

@clients_bp.route('/<int:client_id>', methods=['GET'])
def get_client_by_id(client_id):
    """
    Retorna os dados de um cliente específico, incluindo usuário e cartões de crédito.
    """
    try:
        client = db.session.query(Client).get(client_id)
        if not client:
            return jsonify({"error": "Cliente não encontrado"}), 404

        cards_data = []
        for card in client.card_infos:
            number_str = str(card.number)
            last4digits = number_str[-4:] if len(number_str) >= 4 else number_str
            cards_data.append({
                "id": card.id,
                "last4": last4digits,
                "expirationDate": card.expiration_date,
                "brand": card.brand
            })

        client_data = {
            "clientId": client.id,
            "userId": client.user.id,
            "name": client.user.name,
            "phone": client.user.phone,
            "address": client.user.address,
            "identifier": client.user.identifier,
            "document_path": client.user.document_path,
            "image": client.user.image,
            "cards": cards_data
        }

        return jsonify(client_data), 200

    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500