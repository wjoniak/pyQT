import sqlite3

class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cur = self.conn.cursor()

    def create_table(self, table_name, columns):
        columns_str = ', '.join([f'{col[0]} {col[1]}' for col in columns])
        self.cur.execute(f'CREATE TABLE IF NOT EXISTS {table_name} ({columns_str});')
        self.conn.commit()

    def insert_data(self, table_name, data):

        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in data])
        values = tuple(data.values())

        self.cur.execute(f'INSERT INTO {table_name} ({columns}) VALUES ({placeholders});', values)
        self.conn.commit()

    def update_data(self, table_name, data, condition):

        columns = ', '.join([f'{col}=?' for col in data])
        values = tuple(data.values())

        self.cur.execute(f'UPDATE {table_name} SET {columns} WHERE {condition};', values)
        self.conn.commit()

    def delete_data(self, table_name, condition):

        self.cur.execute(f'DELETE FROM {table_name} WHERE {condition};')
        self.conn.commit()

    def fetch_all(self, table_name):
        self.cur.execute(f'SELECT * FROM {table_name};')
        return self.cur.fetchall()

    def close(self):
        self.conn.close()
