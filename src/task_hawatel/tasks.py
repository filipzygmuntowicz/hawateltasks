from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import requests
import pandas as pd
import logging

logging.basicConfig(filename='logs.log', level=logging.INFO)


# Function to create ORM with flask_sqlalchemy
def create_orm(username, password, host, db_name):

    conn = "mysql://{0}:{1}@{2}/{3}".format(username, password, host, db_name)
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = conn
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db = SQLAlchemy(app)

    class Product(db.Model):
        __tablename__ = 'product'
        ProductID = db.Column(db.String(8), primary_key=True)
        DepartmentID = db.Column(db.String(8))
        Category = db.Column(db.String(45))
        IDSKU = db.Column(db.String(8))
        ProductName = db.Column(db.String(45))
        Quantity = db.Column(db.Integer)
        UnitPrice = db.Column(db.Numeric)
        UnitPriceUSD = db.Column(db.Numeric)
        UnitPriceEuro = db.Column(db.Numeric)
        Ranking = db.Column(db.Integer)
        ProductDesc = db.Column(db.Text)
        UnitsInStock = db.Column(db.Integer)
        UnitsInOrder = db.Column(db.Integer)
        Picture = db.Column(db.LargeBinary)

        def __init__(
            self, ProductID, DepartmentID,
            Category, IDSKU, ProductName, Quantity, UnitPrice,
            UnitPriceUSD, UnitPriceEuro, Ranking, ProductDesc,
            UnitsInStock, UnitsInOrder, Picture
        ):
            self.ProductID = ProductID
            self.DepartmentID = DepartmentID
            self.Category = Category
            self.IDSKU = IDSKU
            self.ProductName = ProductName
            self.Quantity = Quantity
            self.UnitPrice = UnitPrice
            self.UnitPriceUSD = UnitPriceUSD
            self.UnitPriceEuro = UnitPriceEuro
            self.Ranking = Ranking
            self.ProductDesc = ProductDesc
            self.UnitsInStock = UnitsInStock
            self.UnitsInOrder = UnitsInOrder
            self.Picture = Picture
    return db, Product


# Class for required operations, it's made that way so the script can be
# packaged as a module with ability for the user to input his own username,
# password, host and name of the database.
class Operations:
    def __init__(
        self, username="root", password="", host="localhost", db_name="mydb"
            ):
        """
        Input your own username, password, host and db_name or leave it empty
        for default values.
        """
        self.db, self.Product = create_orm(username, password, host, db_name)

    def update_prices(self):
        """
        Downloads the current rates from NBP API and updates the prices in
        Products table.
        """
        try:
            euro = requests.get(
                "http://api.nbp.pl/api/exchangerates/rates/A/EUR?format=json"
                ).json()["rates"][0]["mid"]
            logging.info("eur:{0}".format(euro))
            usd = requests.get(
                "http://api.nbp.pl/api/exchangerates/rates/A/USD?format=json"
                ).json()["rates"][0]["mid"]
            logging.info("usd:{0}".format(usd))
            for product in self.Product.query.all():
                product.UnitPriceUSD = float(product.UnitPrice) * usd
                product.UnitPriceEuro = float(product.UnitPrice) * euro
            self.db.session.commit()
        except Exception:
            print("""\
Exception occured with update_prices method!\
NBP API or database might be down.\
Check logs for more details.\
""")
            logging.exception("")

    def excel(self):
        """
        Creates a xlsx file containing all of the columns from
        Products database.
        """
        try:
            products = self.Product.query.all()
            df = pd.DataFrame({
                'ProductID': [product.ProductID for product in products],
                'DepartmentID': [product.DepartmentID for product in products],
                'Category': [product.Category for product in products],
                'IDSKU': [product.IDSKU for product in products],
                'ProductName': [product.ProductName for product in products],
                'Quantity': [product.Quantity for product in products],
                'UnitPrice': [product.UnitPrice for product in products],
                'UnitPriceUSD': [product.UnitPriceUSD for product in products],
                'UnitPriceEuro': [
                    product.UnitPriceEuro for product in products],
                'Ranking': [product.Ranking for product in products],
                'ProductDesc': [product.ProductDesc for product in products],
                'UnitsInStock': [product.UnitsInStock for product in products],
                'UnitsInOrder': [product.UnitsInOrder for product in products]
            })
            writer = pd.ExcelWriter('Products.xlsx', engine='xlsxwriter')
            df.to_excel(writer, sheet_name='Sheet1', index=False)
            writer.save()
        except Exception:
            print("""\
Exception occured with excel method! The database might be down.\
Check logs for more details.\
""")
            logging.exception("")
