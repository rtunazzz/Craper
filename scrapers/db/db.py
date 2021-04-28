import sqlite3
from datetime import datetime
from typing import List, Set, Tuple, Union


class DatabaseWrapper:
    def __init__(self, path_to_db: str) -> None:
        self.path = path_to_db

        self.connection = None
        self.cursor = None

        self._initialize()

    def __del__(self) -> None:
        if self.connection:
            self.connection.close()

    def _initialize(self):
        self.connection = sqlite3.connect(self.path)
        self.cursor = self.connection.cursor()

    def create_table_safe(self, site: str):
        query = f""" CREATE TABLE IF NOT EXISTS {site} (
                        productId       NUMBER,
                        productIdStr    TEXT,
                        imageUrl        TEXT,
                        dateAdded       TIMESTAMP,
                        UNIQUE (productId)
                    ); """
        self.cursor.execute(query)

    def add_pid(self, site: str, pid: int, formatted_pid: str, image_url: str):
        self.cursor.execute(f"INSERT INTO {site} VALUES ({pid}, '{formatted_pid}', '{image_url}', {datetime.now().timestamp()});")

    def get_pids_int(self, site: str) -> List[int]:
        self.cursor.execute(f"SELECT productId FROM {site}")
        rows: List[Tuple[int]] = self.cursor.fetchall()
        return [row[0] for row in rows]

    def get_pids_formatted(self, site: str) -> List[str]:
        self.cursor.execute(f"SELECT productIdStr FROM {site}")
        rows: List[Tuple[int]] = self.cursor.fetchall()
        return [row[0] for row in rows]

    def get_all_data(self, site: str) -> List[Tuple[int, str, str, float]]:
        self.cursor.execute(f"SELECT productId,productIdStr,imageUrl,dateAdded FROM {site}")
        return self.cursor.fetchall()


if __name__ == '__main__':
    db = DatabaseWrapper('./test.db')
    db.create_table_safe('snipes')

    db.add_pid('snipes', 13801929255, '00013801929255', 'https://www.snipes.com/dw/image/v2/BDCB_PRD/on/demandware.static/-/Sites-snse-master-eu/default/dwc45fe2f6/1929255_P.jpg?sw=780&sh=780&sm=fit&sfrm=png')
    print(db.get_pids_int('snipes'))
    print(db.get_pids_formatted('snipes'))
    # print(db.get_all_data('snipes'))
