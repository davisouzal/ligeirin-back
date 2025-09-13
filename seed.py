from app import create_app, db
import datetime
from app.models import (
    User, BankingInfo, Driver, Seller, ProductCategory,
    Product, SellerProduct, SellerProductDetails, Client,
    CardInfo, Order, OrderProduct
)

app = create_app()
with app.app_context():
    db.drop_all()
    db.create_all()

    # Criar usuários
    user_seller = User(name="João da Loja", phone="11999999999", address="Rua A, 123", identifier="12345678901", image="http://exemplo.com/imagens/mercearia_joao.jpg")
    user_client = User(name="Maria Compradora", phone="11988888888", address="Rua B, 456", identifier="98765432100", image="http://exemplo.com/imagens/maria_compradora.jpg")
    db.session.add_all([user_seller, user_client])
    db.session.commit()

    # Banking info
    bank_info = BankingInfo(account_number=123456, holder_name="João da Loja", holder_identifier="12345678901", agency="001", operation="013")
    db.session.add(bank_info)
    db.session.commit()

    # Seller vinculado
    seller = Seller(company_name="Distribuicão de alimentos divinos", user_id=user_seller.id, banking_info_id=bank_info.id)
    db.session.add(seller)
    db.session.commit()

    # Client vinculado
    client = Client(user_id=user_client.id)
    db.session.add(client)
    db.session.commit()

    # Categoria de produto
    cat_roupa = ProductCategory(name="Roupas")
    db.session.add(cat_roupa)
    db.session.commit()

    # Produto
    product = Product(category_id=cat_roupa.id, name="Camiseta")
    db.session.add(product)
    db.session.commit()

    # SellerProduct
    sp = SellerProduct(
        title="Camiseta Básica Azul",
        brand="Genérica",
        seller_id=seller.id,
        product_id=product.id,
        description="Camiseta confortável de algodão",
        care_level="BAIXO",
        image="http://exemplo.com/imagens/camiseta.jpg",
        price=59.90
    )
    db.session.add(sp)
    db.session.commit()

    # Detalhes do produto
    sp_detail = SellerProductDetails(
        seller_product_id=sp.id,
        color="AZUL",
        size="M",
        stock=100
    )
    db.session.add(sp_detail)
    db.session.commit()

    # 🔹 Criar pedido
    order = Order(
        client_id=client.id,
        total_price = 120,
        status = "COMPLETED",
        complete_date=datetime.datetime.now(),
        payment_method = "PIX"
    )
    db.session.add(order)
    db.session.commit()

    # 🔹 Vincular produto ao pedido
    order_product = OrderProduct(
        order_id=order.id,
        seller_product_id=sp.id,
        quantity=2
    )
    db.session.add(order_product)
    db.session.commit()

    print("✅ Banco populado com dados fictícios incluindo pedidos!")
