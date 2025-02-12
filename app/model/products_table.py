from model.database import get_db


class ProductsTable:
    @staticmethod
    def get():
        """Gets all rows from the products table.

        Raises:
            sqlite3.Error: If the database operations fail

        Returns:
            list: a list of all rows; each row is a dictionary that maps
                column names to values. An empty list is returned if the
                table has no columns.
        """
        db = get_db()
        result = db.execute("SELECT * FROM PRODUCTS")
        products = result.fetchall()
        products = [dict(product) for product in products]
        return products

    @staticmethod
    def get_by_id(product_id):
        """Gets the row with the given id from the products table.

        Raises:
            sqlite3.Error: If the database operations fail

        Args:
            product_id (int): the id of the product to be returned

        dict: the product with the specified product id; None if no such
            product exists
        """
        db = get_db()
        query = "SELECT * FROM PRODUCTS WHERE ProductID = ?"
        data = [product_id]
        result = db.execute(query, data)
        product = result.fetchone()
        if product is not None:
            product = dict(product)
        return product

    @staticmethod
    def get_by_name(product_name):
        """Gets the row with the given product name from the products table.

        Raises:
            sqlite3.Error: If the database operations fail

        Args:
            product_name (str): the name of the product to be returned

        Returns:
            dict: the product with the specified name; None if no such
                    product exists
        """
        db = get_db()
        query = "SELECT * FROM PRODUCTS WHERE ProductName = ?"
        data = [product_name]
        result = db.execute(query, data)
        product = result.fetchone()
        if product is not None:
            product = dict(product)
        return product

    @staticmethod
    def get_by_code(product_code):
        """Gets the row with the given product code from the products table.

        Raises:
            sqlite3.Error: If the database operations fail

        Args:
            product_code (str): the code of the product to be returned

        Returns:
            dict: the product with the specified code; None if no such
                    product exists
        """
        db = get_db()
        query = "SELECT * FROM PRODUCTS WHERE ProductCode = ?"
        data = [product_code]
        result = db.execute(query, data)
        product = result.fetchone()
        if product is not None:
            product = dict(product)
        return product

    @staticmethod
    def insert(product_data):
        """Inserts the specified product into the products table.

        Raises:
            sqlite3.Error: If the database operations fail

        Args:
            product_data (dict): the data of the product to be inserted;
                must map "product_name" to a nonempty string.

        Returns:
            tuple: (success, message, product) where
                success (bool): True if the product has been inserted
                message (str): "The product has been inserted." if success is
                    True; an error message if success is False
                product (dict): the inserted product; None if success is False
        """
        ## Validation for product_name field
        if "product_name" not in product_data:
            return False, "Product name is missing.", None

        product_name = product_data["product_name"]
        if len(product_name) == 0:
            return False, "Product name is empty.", None

        product = ProductsTable.get_by_name(product_name)
        if product is not None:
            return False, "Product name exists already.", None

        ## Validation for product_code field
        if "product_code" not in product_data:
            return False, "Product code is missing.", None

        product_code = product_data["product_code"]
        if len(product_code) == 0:
            return False, "Product code is empty.", None

        product = ProductsTable.get_by_code(product_code)
        if product is not None:
            return False, "Product code exists already.", None

        ## Validation for category_id field
        if "category_id" not in product_data:
            return False, "Category id is missing.", None

        category_id = product_data["category_id"]
        if category_id <= 0:
            return False, "Category id is empty.", None

        ## Validation for price field
        if "price" not in product_data:
            return False, "Price is missing.", None

        price = product_data["price"]
        if price <= 0:
            return False, "Price is empty.", None

        db = get_db()
        query = """
            INSERT INTO PRODUCTS (ProductName, ProductCode, CategoryID, Price) 
                VALUES (?,?,?,?)
        """
        data = [product_name, product_code, category_id, price]
        db.execute(query, data)
        product = ProductsTable.get_by_name(product_name)
        db.commit()
        return True, "The product has been inserted.", product

    @staticmethod  #### NEED TO WORK ON THIS
    def delete(product_id):
        """Deletes the row with the given id from the products table.

        Raises:
            sqlite3.Error: If the database operations fail

        Args:
            product_id (int): the id of the product to be deleted

        tuple: (success, message, product) where
                success (bool): True if the product has been deleted
                message (str): "The product has been inserted." if success is
                    True; an error message if success is False
                product (dict): the product with the specified identifier
                    product_id; None if no such product exists
        """
        product = ProductsTable.get_by_id(product_id)
        if product is None:
            return False, "Product not found.", None

        db = get_db()
        query = "SELECT * FROM PRODUCTS WHERE CategoryID = ?"
        data = [category_id]
        result = db.execute(query, data)
        product = result.fetchone()
        if product is not None:
            return False, "Category has products.", category

        query = "DELETE FROM CATEGORIES WHERE CategoryID = ?"
        data = [category_id]
        db.execute(query, data)
        db.commit()
        return True, "The category has been deleted.", category
