from typing import Union

import asyncpg
from asyncpg.pool import Pool

from data import config

class Database:
    def __init__(self):
        """Создается база данных без подключения в loader"""

        self.pool: Union[Pool, None] = None

    async def create(self):
        """В этой функции создается подключение к базе"""

        pool = await asyncpg.create_pool(
            user=config.PG_USER,  # Пользователь базы (postgres или ваше имя), для которой была создана роль
            password=config.PG_PASSWORD,  # Пароль к пользователю
            host="database-tg",  # Ip адрес базы данных. Если локальный компьютер - localhost, если докер - название сервиса
            database=config.DATABASE  # Название базы данных. По умолчанию - postgres, если вы не создавали свою
        )
        self.pool = pool


    async def create_table_orders(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Orders (
        id INT NOT NULL,
        Name VARCHAR(255) NOT NULL,
        Number VARCHAR(255) NOT NULL,
        Code VARCHAR(255) NOT NULL,
        PRIMARY KEY (id)
        )
        """
        await self.pool.execute(sql)

    async def create_table_products(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Products (
        id INT NOT NULL,
        Name VARCHAR(255) NOT NULL,
        Code VARCHAR(255) NOT NULL,
        File_id VARCHAR(255) NOT NULL,
        Point INT,
        Type VARCHAR(255),
        PRIMARY KEY (id)
        )
        """
        await self.pool.execute(sql)


    @staticmethod
    def format_args(sql, paramteres: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(paramteres, start=1)
        ])
        return sql, tuple(paramteres.values())

    async def add_order(self, id: int, name: str, number: str, code: str):
        sql = "INSERT INTO Orders(id, name, number, code) VALUES ($1, $2, $3, $4)"
        await self.pool.execute(sql, id, name, number, code)

# Orders Table methods

    async def select_all_orders(self):
        sql = "SELECT * FROM Orders"
        return await self.pool.fetch(sql)

    async def select_order(self, **kwargs):
        sql = "SELECT * FROM Orders WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return await self.pool.fetchrow(sql, *parameters)

    async def count_orders(self):
        return await self.pool.fetchval("SELECT COUNT(*) FROM Orders")


    async def delete_order(self, id):
        sql = "DELETE FROM Orders WHERE id = $1"
        await self.pool.execute(sql, id)

    async def delete_orders(self):
        await self.pool.execute("DELETE FROM Orders WHERE True")

    async def delete_table_orders(self):
        await self.pool.execute("DROP TABLE Orders")

# Products Table methods

    async def add_product(self, id: int, name: str, code: str, file_id: str, point: int = 0, type: str = ''):
        sql = "INSERT INTO Products(id, name, code, file_id, point, type) VALUES ($1, $2, $3, $4, $5, $6)"
        await self.pool.execute(sql, id, name, code, file_id, point, type)

    async def select_product(self, **kwargs):
        sql = "SELECT * FROM Products WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return await self.pool.fetchrow(sql, *parameters)

    async def select_all_products(self):
        sql = "SELECT * FROM Products"
        return await self.pool.fetch(sql)

    async def count_products(self):
        return await self.pool.fetchval("SELECT COUNT(*) FROM Products")

    async def delete_product(self, id):
        sql = "DELETE FROM Products WHERE id = $1"
        await self.pool.execute(sql, id)

    async def delete_products(self):
        await self.pool.execute("DELETE FROM Products WHERE True")

    async def delete_table_products(self):
        await self.pool.execute("DROP TABLE Products")
