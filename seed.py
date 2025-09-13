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
    user_seller1 = User(name="João da Loja", phone="11999999999", address="Rua A, 123", identifier="12345678901", image="http://exemplo.com/imagens/mercearia_joao.jpg")
    user_seller2 = User(name="Alexandre das Ferramentas", phone="11777777777", address="Rua C, 789", identifier="23456789012", image="http://exemplo.com/imagens/ferramentas_alexandre.jpg")
    user_client1 = User(name="Maria Compradora", phone="11988888888", address="Rua B, 456", identifier="98765432100", image="http://exemplo.com/imagens/maria_compradora.jpg")
    user_client2 = User(name="Joaquim Comprador", phone="11988888889", address="Rua D, 012", identifier="98754321001", image="http://exemplo.com/imagens/joaquim_comprador.jpg")
    db.session.add_all([user_seller1, user_seller2,user_client1, user_client2])
    db.session.commit()

    # Banking info
    bank_info_seller1 = BankingInfo(account_number=123456, holder_name="João da Loja", holder_identifier="12345678901", agency="001", operation="013")
    bank_info_seller2 = BankingInfo(account_number=234567, holder_name="Alexandre das Ferramentas", holder_identifier="23456789012", agency="001", operation="013")
    db.session.add_all([bank_info_seller1, bank_info_seller2])
    db.session.commit()

    # Seller vinculado
    seller1 = Seller(company_name="Distribuicão de alimentos divinos", user_id=user_seller1.id, banking_info_id=bank_info_seller1.id)
    seller2 = Seller(company_name="Distribuicão de ferramentas pau pra toda obra", user_id=user_seller2.id, banking_info_id=bank_info_seller2.id)
    db.session.add_all([seller1, seller2])
    db.session.commit()

    # Client vinculado
    client1 = Client(user_id=user_client1.id)
    client2 = Client(user_id=user_client2.id)
    db.session.add_all([client1, client2])
    db.session.commit()

    # Categoria de produto
    pc1 = ProductCategory(name="Roupas", icon="shirt-outline")
    pc2 = ProductCategory(name="Ferramentas", icon="build-outline")
    db.session.add_all([pc1, pc2])
    db.session.commit()

    # Produto
    product1 = Product(category_id=pc1.id, name="Camiseta")
    product2 = Product(category_id=pc2.id, name="Chave de Fenda")
    product3 = Product(category_id=pc1.id, name="Boné")
    product4 = Product(category_id=pc1.id, name="Martelo")
    db.session.add_all([product1, product2, product3, product4])
    db.session.commit()

    # SellerProduct
    sp1 = SellerProduct(
        title="Camiseta Básica Azul",
        brand="Genérica",
        seller_id=seller1.id,
        product_id=product1.id,
        description="Camiseta confortável de algodão",
        care_level="BAIXO",
        image="https://cdn.awsli.com.br/600x1000/1154/1154659/produto/161909164/005c94be4f.jpg",
        price=59.90
    )
    sp2 = SellerProduct(
        title="Chave de Fenda Magnética",
        brand="Bosch",
        seller_id=seller2.id,
        product_id=product2.id,
        description="Chave de Fenda Magnética e Confiável",
        care_level="MEDIO",
        image="https://cdn.leroymerlin.com.br/products/chave_de_fenda_phillips_ponta_magnetica_imantada_ima_grande_c_1571229180_d169_600x600.jpg",
        price=20.0
    )
    sp3 = SellerProduct(
        title="Bone massa",
        brand="Nike",
        seller_id=seller1.id,
        product_id=product3.id,
        description="Bone muito legal da nike",
        care_level="BAIXO",
        image="https://cdn.discordapp.com/attachments/1416162813637955624/1416569320062062743/21YVNPVXGqS._SY1000_.jpg?ex=68c7527c&is=68c600fc&hm=11ca13afc4ac0c39ac2558fa6db47c6afddecb4c9f12e7c354aa9e389687d481&",
        price=59.90
    )
    sp4 = SellerProduct(
        title="Martelo",
        brand="Bosch",
        seller_id=seller2.id,
        product_id=product4.id,
        description="Martelo quebra tudo",
        care_level="BAIXO",
        image="https://cdn.discordapp.com/attachments/1416162813637955624/1416569533837344779/267270.webp?ex=68c752af&is=68c6012f&hm=c9085a81a94db1f57c581152ab54da85751c1741cd41fa5e0986635fff0e2c07&",
    )
    db.session.add_all([sp1, sp2, sp3, sp4])
    db.session.commit()

    # Detalhes do produto
    sp_detail1 = SellerProductDetails(
        seller_product_id=sp1.id,
        color="AZUL",
        size="M",
        stock=100
    )
    sp_detail2 = SellerProductDetails(
        seller_product_id=sp2.id,
        color="AMARELO",
        stock=20
    )
    db.session.add_all([sp_detail1, sp_detail2])
    db.session.commit()

    # Pedido
    order1 = Order(
        client_id=client1.id,
        total_price = 120,
        status = "COMPLETED",
        complete_date=datetime.datetime.now(),
        payment_method = "PIX"
    )
    order2 = Order(
        client_id=client1.id,
        total_price = 20,
        status = "DRAFT",
    )
    db.session.add_all([order1, order2])
    db.session.commit()

    # Produtos do pedido
    order_product1 = OrderProduct(
        order_id=order1.id,
        seller_product_id=sp1.id,
        quantity=2
    )
    order_product2 = OrderProduct(
        order_id=order2.id,
        seller_product_id=sp2.id,
        quantity=1
    )
    db.session.add_all([order_product1, order_product2])
    db.session.commit()

    print("✅ Banco populado com dados fictícios!")
