from model.database import get_db


class CategoriesTable:

    @staticmethod
    def get():
        """Gets all rows from the categories table.

        Raises:
            sqlite3.Error: If the database operations fail

        Returns:
            list: a list of all rows; each row is a dictionary that maps
                column names to values. An empty list is returned if the 
                table has no columns.
        """
        db = get_db()
        result = db.execute("SELECT * FROM CATEGORIES")
        categories = result.fetchall()
        categories = [dict(category) for category in categories]
        return categories


    @staticmethod
    def get_by_id(category_id):
        """Gets the row with the given id from the categories table.

        Raises:
            sqlite3.Error: If the database operations fail

        Args:
            category_id (int): the id of the category to be returned

        dict: the catgory with the specified category id; None if no such
            category exists
        """
        db = get_db()
        query = "SELECT * FROM CATEGORIES WHERE CategoryID = ?"
        data = [category_id]
        result = db.execute(query, data)
        category = result.fetchone()
        if category is not None:
            category = dict(category)
        return category


    @staticmethod
    def get_by_name(category_name):
        """Gets the row with the given category name from the categories table.

        Raises:
            sqlite3.Error: If the database operations fail

        Args:
            category_name (str): the name of the category to be returned

        Returns:
            dict: the catgory with the specified name; None if no such 
                    catgory exists
        """
        db = get_db()
        query = "SELECT * FROM CATEGORIES WHERE CategoryName = ?"
        data = [category_name]
        result = db.execute(query, data)
        category = result.fetchone()
        if category is not None:
                category = dict(category)
        return category


    @staticmethod
    def insert(category_data):
        """Inserts the specified category into the categories table.

        Raises:
            sqlite3.Error: If the database operations fail

        Args:
            category_data (dict): the data of the category to be inserted;  
                must map "category_name" to a nonempty string.

        Returns:
            tuple: (success, message, category) where
                success (bool): True if the category has been inserted
                message (str): "The category has been inserted." if success is 
                    True; an error message if success is False
                category (dict): the inserted category; None if success is False
        """
        if "category_name" not in category_data:
            return False, "Category name is missing.", None

        category_name = category_data["category_name"]
        if len(category_name) == 0:
            return False, "Category name is empty.", None

        category = CategoriesTable.get_by_name(category_name)
        if category is not None:
            return False, "Category name exists already.", None

        db = get_db()
        query = """
            INSERT INTO CATEGORIES (CategoryName) 
                VALUES (?)
        """
        data = [category_name]
        db.execute(query, data)
        category = CategoriesTable.get_by_name(category_name)
        db.commit()
        return True, "The category has been inserted.", category


    @staticmethod
    def delete(category_id):
        """Deletes the row with the given id from the categories table.

        Raises:
            sqlite3.Error: If the database operations fail

        Args:
            category_id (int): the id of the category to be deleted

        tuple: (success, message, category) where
                success (bool): True if the category has been deleted
                message (str): "The category has been inserted." if success is 
                    True; an error message if success is False
                category (dict): the category with the specified identifier 
                    category_id; None if no such category exists
        """
        category = CategoriesTable.get_by_id(category_id)
        if category is None:
            return False, "Category not found.", None

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

