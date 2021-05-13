import sqlite3
from datetime import datetime
from typing import List, Set, Tuple, Union


class DatabaseWrapper:
    """Wrapper for an SQL database connection

    Args:
        path_to_db: str
            Path where the database is/ will be saved
    
    Attributes:
        None
    
    Methods:
        create_table_safe(site):
            Creates a table in our database
        add_data(site, pid, formatted_pid, image_url)
            Adds a product ID to our database
        get_pids_int(site)
            Gets all pids (as integers)
        get_pids_formatted(site)
            Gets all pids (formatted, as strings)
        get_all_data(site)
            Gets all data
    
    Raises:
        sqlite3.OperationalError
            When the a method calls a table that doesn't match any existing table.
    """
    def __init__(self, path_to_db: str) -> None:
        self._path = path_to_db

        self._connection = None
        self._cursor = None

        self._initialize()

    def __del__(self) -> None:
        if self._connection:
            self._connection.close()

    def _initialize(self):
        self._connection = sqlite3.connect(self._path)
        self._cursor = self._connection.cursor()

    def create_table_safe(self, site: str) -> None:
        """Creates a table specified by the `site` parameter, if it doesn't already exists.

        Args:
            site (str): Name of the site (table)
        
        Returns:
            None
        """

        query = f''' CREATE TABLE IF NOT EXISTS {site} (
                        productId       NUMBER,
                        productIdStr    TEXT,
                        imageUrl        TEXT,
                        dateAdded       TIMESTAMP,
                        UNIQUE (productId)
                    ); '''
        self._cursor.execute(query)
        self._connection.commit()

    def add_data(self, site: str, pid: int, formatted_pid: str, image_url: str) -> bool:
        """Adds the data provided into a table, identified by the `site` parameter

        Args:
            site (str): Name of the site
            pid (int): Product ID
            formatted_pid (str): Formatted product ID
            image_url (str): Image URL
        
        Returns:
            bool: True when added successfully, False otherwise

        Example:
        ```py3
            db.add_data(
                'snipes', 13801929255,
                '00013801929255',
                'https://www.snipes.com/dw/image/v2/BDCB_PRD/on/demandware.static/-/Sites-snse-master-eu/default/dwc45fe2f6/1929255_P.jpg?sw=780&sh=780&sm=fit&sfrm=png'
            )
        ```
        """
        try:
            self._cursor.execute(f"INSERT INTO {site} VALUES ({pid}, '{formatted_pid}', '{image_url}', {datetime.now().timestamp()});")
            self._connection.commit()
            return True
            
        except sqlite3.IntegrityError:
            print(f'Failed to add {pid} ({formatted_pid}) - PID already exists in table "{site}".')
        
        return False

    def get_pids_int(self, site: str) -> List[int]:
        """Gets all product IDs (as integers) in a database table, specified by the `site` parameter 

        Args:
            site (str): Name of the site to get product IDs for

        Returns:
            List[int]: List of (integer) product IDs
        
        Raises:
            sqlite3.OperationalError
                When the `site` parameter doesn't match any existing table.
        """
        try:
            self._cursor.execute(f"SELECT productId FROM {site}")
        except sqlite3.OperationalError:
            raise sqlite3.OperationalError(f"Table '{site}' does not exist. You can create it with the `create_table_safe` method.")
        rows: List[Tuple[int]] = self._cursor.fetchall()
        return [row[0] for row in rows]

    def get_pids_formatted(self, site: str) -> List[str]:
        """Gets all formatted product IDs (as strings) in a database table, specified by the `site` parameter 

        Args:
            site (str): Name of the site to get product IDs for

        Returns:
            List[int]: List of formatted (string) product IDs
        
        Raises:
            sqlite3.OperationalError
                When the `site` parameter doesn't match any existing table.
        """
        try:
            self._cursor.execute(f"SELECT productIdStr FROM {site}")
        except sqlite3.OperationalError:
            raise sqlite3.OperationalError(f"Table '{site}' does not exist. You can create it by the `create_table_safe` method.")
        rows: List[Tuple[int]] = self._cursor.fetchall()
        return [row[0] for row in rows]

    def get_all_data(self, site: str) -> List[Tuple[int, str, str, float]]:
        """Gets all data from a database table, specified by the `site` parameter
        The row order is as follows:
            productId, productIdStr, imageUrl, dateAdded

        Args:
            site (str): Name of the site to get product IDs for

        Returns:
            List[Tuple[int, str, str, float]]: List of (productId, productIdStr, imageUrl, dateAdded) tuples
        
        Raises:
            sqlite3.OperationalError
                When the `site` parameter doesn't match any existing table.
        """
        try:
            self._cursor.execute(f"SELECT productId,productIdStr,imageUrl,dateAdded FROM {site}")
        except sqlite3.OperationalError:
            raise sqlite3.OperationalError(f"Table '{site}' does not exist. You can create it by the `create_table_safe` method.")
        return self._cursor.fetchall()


if __name__ == '__main__':
    db = DatabaseWrapper('./data/pids.db')
    db.create_table_safe('footpatrol')

    # DatabaseWrapper('./test.db').add_data('snipes', 13801929255, '00013801929255', 'https://www.snipes.com/dw/image/v2/BDCB_PRD/on/demandware.static/-/Sites-snse-master-eu/default/dwc45fe2f6/1929255_P.jpg?sw=780&sh=780&sm=fit&sfrm=png')
    print(db.get_pids_int('footpatrol'))
    # print(db.get_pids_formatted('snipes'))
    # print(db.get_all_data('snipes'))
