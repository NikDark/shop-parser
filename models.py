import os
from peewee import TextField, IntegerField, Model
from playhouse.postgres_ext import PostgresqlExtDatabase, BooleanField
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
    shop = TextField(column_name='shop')
    link = TextField(column_name='link')
    group = TextField(column_name='group')

    class Meta:
        table_name = 'product_parser'