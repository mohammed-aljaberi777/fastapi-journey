from contextlib import contextmanager
import sqlite3
import json


class Database:

    def connect_to_db(self):
        self.conn = sqlite3.connect("sqlite.db", check_same_thread=False)
        self.cur = self.conn.cursor()

    def create_table(self):
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                year INTEGER NOT NULL,
                copies INTEGER NOT NULL,
                borrow_records TEXT NOT NULL                                             
            )
        """)
        self.conn.commit()

    def get_all(self) -> list:
        self.cur.execute("SELECT * FROM books")
        rows = self.cur.fetchall()
        return [self._row_to_dict(row) for row in rows]

    def get(self, id: int) -> dict | None:
        self.cur.execute("""
            SELECT * FROM books WHERE id = ?
        """, (id,))
        row = self.cur.fetchone()
        return self._row_to_dict(row) if row else None

    def create(self, item) -> int:
        self.cur.execute("SELECT MAX(id) FROM books")
        result = self.cur.fetchone()
        new_id = (result[0] or 0) + 1

        item_data = item.model_dump(mode="json")
        borrow_records_json = json.dumps(item_data["borrow_records"])

            
        
        self.cur.execute("""
            INSERT INTO books
            VALUES (:id, :title, :author,:year, :copies,:borrow_records)
        """, {
            "id": new_id,
            "title":item.title,
            "author":item.author,
            "year":item.year,
            "copies":item.copies,
            "borrow_records":borrow_records_json
             
             
             
             
        })
        self.conn.commit()
        return new_id

    def update(self, id: int, item) -> dict | None:
       item_data = item.model_dump(mode="json")
       borrow_records_json = json.dumps(item_data["borrow_records"])

       self.cur.execute("""
        UPDATE books
        SET title = :title,
            author = :author,
            year = :year,
            copies = :copies,
            borrow_records = :borrow_records
        WHERE id = :id
    """, {
        "id": id,
        "title": item_data["title"],
        "author": item_data["author"],
        "year": item_data["year"],
        "copies": item_data["copies"],
        "borrow_records": borrow_records_json
    })
       self.conn.commit()
       return self.get(id)
    def delete(self, id: int):
        self.cur.execute("""
            DELETE FROM books WHERE id = ?
        """, (id,))
        self.conn.commit()

    def close(self):
        self.conn.close()

    def _row_to_dict(self, row) -> dict:
        borrow_records_data = json.loads(row[5]) if row[5] else []

        return {
            "id": row[0],
            "title": row[1],
            "author": row[2],
            "year": row[3],
            "copies": row[4],
            "borrow_records": borrow_records_data
        }



@contextmanager
def managed_db():
    db = Database()
    db.connect_to_db()
    db.create_table()
    try:
        yield db
    finally:
        db.close()