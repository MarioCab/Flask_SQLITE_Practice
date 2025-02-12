from flask import Flask, request
from flask_cors import CORS
import sqlite3
from model.database import close_db
from model.categories_table import CategoriesTable
from model.products_table import ProductsTable


app = Flask(__name__)
CORS(app)


@app.get("/category")
def get_categories():
    try:
        categories = CategoriesTable.get()
        return {"categories": categories}, 200
    except sqlite3.Error as error:
        return {"error": str(error)}, 500


@app.get("/product")
def get_products():
    try:
        products = ProductsTable.get()
        return {"products": products}, 200
    except sqlite3.Error as error:
        return {"error": str(error)}, 500


@app.get("/category/<int:category_id>")
def get_category(category_id):
    try:
        category = CategoriesTable.get_by_id(category_id)
        if category is None:
            return {"message": "Category not found."}, 404
        return category
    except sqlite3.Error as error:
        return {"error": str(error)}, 500


@app.get("/product/<int:product_id>")
def get_product(product_id):
    try:
        product = ProductsTable.get_by_id(product_id)
        if product is None:
            return {"message": "Product not found."}, 404
        return product, 200
    except sqlite3.Error as error:
        return {"error": str(error)}, 500


@app.post("/category")
def create_category():
    category_data = request.get_json()
    try:
        success, message, category = CategoriesTable.insert(category_data)
        if not success:
            return {"error": message}, 400
        return category, 201
    except sqlite3.Error as error:
        return {"error": str(error)}, 500


@app.post("/product")
def create_product():
    product_data = request.get_json()
    try:
        success, message, product = ProductsTable.insert(product_data)
        if not success:
            return {"error": message}, 400
        return product, 201
    except sqlite3.Error as error:
        return {"error": str(error)}, 500


@app.delete("/category/<int:category_id>")
def delete_category(category_id):
    try:
        success, message, category = CategoriesTable.delete(category_id)
        if not success:
            if category is None:
                return {"message": "Category not found."}, 404
            else:
                return {"error": message}, 400
        return {"message": "Category deleted."}
    except sqlite3.Error as error:
        return {"error": str(error)}, 500


@app.teardown_appcontext
def close_connection(exception):
    close_db()
