import sqlite3
from app.schemas import ShipmentCreate, ShipmentUpdate
from typing import Any

class Database:
    def __init__(self):
        # Make a connection to db
        self.conn = sqlite3.connect("sqlite.db", check_same_thread=False)
        # get cursor to execute queries
        self.cur = self.conn.cursor()

        # Create table execute
        self.create_table()

    def create_table(self):
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS shipment (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT, 
                weight REAL, 
                status TEXT
            )
        """)

    def create(self, shipment: ShipmentCreate):
        self.cur.execute(
            """
                INSERT INTO shipment (content, weight, status)
                VALUES (:content, :weight, :status)
            """,
            {**shipment.model_dump(), "status": "placed"}
        )
        self.conn.commit()
        return self.cur.lastrowid  # Returns the auto-generated ID
    
    def get(self, id:int)->dict[str, Any]:
        self.cur.execute(
            """
                SELECT * FROM shipment
                WHERE id = ?
            """,
            (id,)
            )
        row = self.cur.fetchone()
        return {
            "id":row[0],
            "content":row[1],
            "weight":row[2],
            "status":row[3],
        }
    
    def get_all(self):
        self.cur.execute(
            """
                SELECT * FROM shipment
            """
        )
        rows = self.cur.fetchall()
        return [
            {
                "id":row[0],
                "content":row[1],
                "weight":row[2],
                "status":row[3],
            } for row in rows
        ]
    
    def update(self,id:int, shipment:ShipmentUpdate):
        self.cur.execute(
            """
                UPDATE shipment SET status = :status
                WHERE id = :id
            """,
            {
                "id":id,
                **shipment.model_dump()
            }
        )
        self.conn.commit()
        return self.get(id)

    def delete(self, id:int):
        self.cur.execute(
            """
                DELETE FROM shipment
                WHERE id = ?
            """,
            (id,)
        )
        self.conn.commit()

    def close(self):
        self.conn.close()

