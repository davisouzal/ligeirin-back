from sqlalchemy.sql import func
from app import db

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45))
    phone = db.Column(db.String(45))
    address = db.Column(db.String(45))
    identifier = db.Column(db.String(45))
    document_path = db.Column(db.String(45))
    image = db.Column(db.String(50))

    seller = db.relationship("Seller", back_populates="user", lazy=True)
    driver = db.relationship("Driver", back_populates="user", lazy=True)
    client = db.relationship("Client", back_populates="user", lazy=True)


class BankingInfo(db.Model):
    __tablename__ = "banking_info"
    id = db.Column(db.Integer, primary_key=True)
    account_number = db.Column(db.Numeric(16, 0))
    holder_name = db.Column(db.String(45))
    holder_identifier = db.Column(db.String(45))
    agency = db.Column(db.String(45))
    operation = db.Column(db.String(45))

    sellers = db.relationship("Seller", back_populates="banking_info")
    drivers = db.relationship("Driver", back_populates="banking_info")


class Driver(db.Model):
    __tablename__ = "driver"
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.Enum("BIKE", "MOTORCYCLE", "CAR"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    banking_info_id = db.Column(db.Integer, db.ForeignKey("banking_info.id"))

    user = db.relationship("User", back_populates="driver")
    banking_info = db.relationship("BankingInfo", back_populates="drivers")


class Seller(db.Model):
    __tablename__ = "seller"
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(45))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    banking_info_id = db.Column(db.Integer, db.ForeignKey("banking_info.id"))

    user = db.relationship("User", back_populates="seller")
    banking_info = db.relationship("BankingInfo", back_populates="sellers")
    products = db.relationship("SellerProduct", back_populates="seller")


class ProductCategory(db.Model):
    __tablename__ = "products_category"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45))

    products = db.relationship("Product", back_populates="category")


class Product(db.Model):
    __tablename__ = "product"
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey("products_category.id"))
    name = db.Column(db.String(45))

    category = db.relationship("ProductCategory", back_populates="products")
    seller_products = db.relationship("SellerProduct", back_populates="product")


class SellerProduct(db.Model):
    __tablename__ = "seller_product"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(45))
    brand = db.Column(db.String(45))
    seller_id = db.Column(db.Integer, db.ForeignKey("seller.id"))
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"))
    description = db.Column(db.String(255))
    care_level = db.Column(db.Enum("BAIXO", "MEDIO", "ALTO"))
    image = db.Column(db.String(100))
    price = db.Column(db.Numeric(10, 0))

    seller = db.relationship("Seller", back_populates="products")
    product = db.relationship("Product", back_populates="seller_products")
    details = db.relationship("SellerProductDetails", back_populates="seller_product")
    order_products = db.relationship("OrderProduct", back_populates="seller_product")


class SellerProductDetails(db.Model):
    __tablename__ = "seller_product_details"
    id = db.Column(db.Integer, primary_key=True)
    seller_product_id = db.Column(db.Integer, db.ForeignKey("seller_product.id"))
    color = db.Column(db.Enum("VERMELHO", "BRANCO", "AMARELO", "LARANJA", "VERDE", "AZUL", "CINZA", "ROSA", "ROXO", "BEGE"  ))
    size = db.Column(db.Enum("PP", "P", "M", "G", "GG", "XG", "XG1", "XG2", "XG3")) 
    stock = db.Column(db.Integer)

    seller_product = db.relationship("SellerProduct", back_populates="details")


class Client(db.Model):
    __tablename__ = "client"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    user = db.relationship("User", back_populates="client")
    orders = db.relationship("Order", back_populates="client")
    card_infos = db.relationship("CardInfo", back_populates="client")


class CardInfo(db.Model):
    __tablename__ = "card_info"
    id = db.Column(db.Integer, primary_key=True)
    expiration_date = db.Column(db.String(45))
    number = db.Column(db.Integer)
    security_code = db.Column(db.Integer)
    client_id = db.Column(db.Integer, db.ForeignKey("client.id"))

    client = db.relationship("Client", back_populates="card_infos")


class Order(db.Model):
    __tablename__ = "order"
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey("client.id"))
    total_price = db.Column(db.Numeric(15, 2))
    payment_method = db.Column(db.Enum("CARTAO", "PIX"))
    status = db.Column(db.Enum("COMPLETED", "DRAFT"), default = "DRAFT")
    complete_date = db.Column(db.DateTime(timezone=True))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    client = db.relationship("Client", back_populates="orders")
    order_products = db.relationship("OrderProduct", back_populates="order")


class OrderProduct(db.Model):
    __tablename__ = "order_product"
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"))
    seller_product_id = db.Column(db.String(45), db.ForeignKey("seller_product.id"))

    order = db.relationship("Order", back_populates="order_products")
    seller_product = db.relationship("SellerProduct", back_populates="order_products")

