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
    """
    Retrieves all categories from the bakery.

    Returns:
        categories: The specified category.

    Response Codes:
        200: Successful Request.
        500: Database operation failed

    """
    try:
        categories = CategoriesTable.get()
        return {"categories": categories}, 200
    except sqlite3.Error as error:
        return {"error": str(error)}, 500


@app.get("/product")
def get_products():
    """
    Retrieves all products from the bakery.

    Returns:
        products: The specified product.

    Response Codes:
        200: Successful Request.
        500: Database operation failed
    """
    try:
        products = ProductsTable.get()
        return {"products": products}, 200
    except sqlite3.Error as error:
        return {"error": str(error)}, 500


@app.get("/category/<int:category_id>")
def get_category(category_id):
    """
    Retrieves a specific category by its ID.

    Parameters:
    category_id (integer): category identifier.

    Returns:
        category: The specified category.

    Response Codes:
        200: Successful Request.
        404: The category ID given does not exist/did not fetch anything.
        500: Database operation failed

    """
    try:
        category = CategoriesTable.get_by_id(category_id)
        if category is None:
            return {"message": "Category not found."}, 404
        return category, 200
    except sqlite3.Error as error:
        return {"error": str(error)}, 500


@app.get("/product/<int:product_id>")
def get_product(product_id):
    """
    Retrieves a specific category by its ID.

    Parameters:
    product_id (integer): product identifier.

    Returns:
        product: The specified product.

    Response Codes:
        200: Successful Request.
        404: The product ID given does not exist/did not fetch anything.
        500: Database operation failed

    """
    try:
        product = ProductsTable.get_by_id(product_id)
        if product is None:
            return {"message": "Product not found."}, 404
        return product, 200
    except sqlite3.Error as error:
        return {"error": str(error)}, 500


@app.post("/category")
def create_category():
    """
    Creates a new category in the bakery.

    Request Body:

    The JSON representation of the new category
    Example:
        {
            "category_name": "Cakes"
        }

    Returns:
        category: The newly created category.

    Response Codes:
        201: Successful Request.
        400: The JSON payload does not contain the category name or the given category name exists already.
        500: Database operation failed

    """
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
    """
    Creates a new product in the bakery.

    Request Body:

        The JSON representation of the new category
        Example:
        {
        "category_id": 3,
        "product_code": "cnrP",
        "product_name": "Cinnamon Raisin Roll",
        "price": 1.09
        }

    Returns:
        product: The newly created product.

    Response Codes:
        201: Successful Request.
        400: The JSON payload does not contain the product name or the given product name exists already.
        500: Database operation failed

    """
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
    """
    Deletes a category from the bakery.

    Params:
        category_id (integer): category identifier

    Response Codes:
        200: Successful Request.
        400: the category is not deleted because there are products associated with the given category
        404: the given category identifier does not exist
        500: Database operation failed

    """
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


@app.delete("/product/<int:product_id>")
def delete_product(product_id):
    """
    Deletes a product from the bakery.

    Params:
        product_id (integer): product identifier

    Response Codes:
        200: Successful Request.
        404: the given product identifier does not exist
        500: Database operation failed

    """
    try:
        success, message, product = ProductsTable.delete(product_id)
        if not success:
            if product is None:
                return {"message": "Product not found."}, 404
            else:
                return {"error": message}, 400
        return {"message": "Product deleted."}, 200
    except sqlite3.Error as error:
        return {"error": str(error)}, 500


@app.put("/product/<int:product_id>")
def update_product(product_id):
    """
    Updates a product in the bakery.

    Request Body:

        The JSON representation of the new category
        Example:
        {
        "category_id": 3,
        "product_code": "cnrP",
        "product_name": "Cinnamon Raisin Roll",
        "price": 1.09
        }

    Returns:
        product: The updated or new product.

    Response Codes:
        200: The existing product was updated.
        201: The product was created
        400: The JSON payload does not contain the product name or the given product name exists already.
        500: Database operation failed

    """
    product_data = request.get_json()
    try:
        success, message, product = ProductsTable.update(product_id, product_data)
        if success:
            return product, 200
        if not success:
            success, message, product = ProductsTable.insert(product_data)
            if success:
                return product, 201
            if not success:
                return {"message": "fields either not unique or missing"}, 400
    except sqlite3.Error as error:
        return {"error": str(error)}, 500


@app.teardown_appcontext
def close_connection(exception):
    close_db()
