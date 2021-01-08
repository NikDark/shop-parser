import os
from peewee import TextField, IntegerField, Model
from playhouse.postgres_ext import PostgresqlExtDatabase, BooleanField, DateField, DoubleField, ForeignKeyField
from dotenv import load_dotenv

load_dotenv()
conn = PostgresqlExtDatabase(
    database=os.getenv("NAME_DB"), 
    user=os.getenv("USER_DB"), 
    password=os.getenv("PASSWORD_DB"), 
    host=os.getenv("HOST_DB"), 
    port=os.getenv("PORT_DB")
)


class BaseModel(Model):
    class Meta:
        database = conn


class Product(BaseModel):
    id = IntegerField(column_name="id", primary_key=True)
    link_e = TextField(column_name='link_e')
    link_g = TextField(column_name='link_g')
    group = TextField(column_name='group')

    class Meta:
        table_name = 'product_parser'

class Price(BaseModel):
    id = IntegerField(column_name='id')
    date = DateField(column_name='date')
    price = DoubleField(column_name='price')
    product = ForeignKeyField(Product, backref="prices")
    authorized = BooleanField(column_name="authorized")
    shop = TextField(column_name="shop")

    class Meta:
        table_name = 'price_parser'

# print([price.product.__dict__ for price in Price.select(Product).join(Product).execute()])