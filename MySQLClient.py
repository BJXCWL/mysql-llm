import pymysql
from pymysql.cursors import DictCursor
import pandas as pd
import re

class MySQLClient:
    """
    封装了 MySQL 连接的初始化、关闭，及获取 schema 信息的方法。
    """
    def __init__(
        self,
        host: str,
        port: int,
        user: str,
        password: str,
        database: str,
        autocommit: bool = True,
        charset: str = 'utf8mb4'
    ):
        self.connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            charset=charset,
            cursorclass=DictCursor,
            autocommit=autocommit
        )
        print(f"MySQL 连接已初始化: {user}@{host}:{port}/{database}")

    def get_schema_info(self) -> list[str]:
        """
        列出当前数据库中所有表及其字段信息，返回格式化后的字符串列表。
        """
        schema_info: list[str] = []
        with self.connection.cursor() as cursor:
            # 列出所有表
            cursor.execute("SHOW TABLES;")
            tables = [list(row.values())[0] for row in cursor.fetchall()]
            # 遍历每个表，获取字段信息
            for table_name in tables:
                cursor.execute(f"SHOW COLUMNS FROM `{table_name}`;")
                columns = cursor.fetchall()
                # 格式化输出
                table_info = f"Table: {table_name}\n"
                table_info += "\n".join(
                    f"  - {col['Field']} ({col['Type']})"
                    for col in columns
                )
                schema_info.append(table_info)
        return "\n\n".join(schema_info)

    def close(self):
        """关闭数据库连接"""
        if self.connection:
            self.connection.close()
            print("MySQL 连接已关闭")

    def run_sql(self, sql: str) -> pd.DataFrame:
            """
            用原生 PyMySQL 游标执行任意 SQL，并把结果封装到 DataFrame。
            支持传入带 <sql> 标签的文本。
            """
            # 1) 提取标签内 SQL，失败则用原文
            real_sql = self.extract_sql(sql) or sql

            # 2) 执行并 fetchall
            with self.connection.cursor() as cursor:
                cursor.execute(real_sql)
                rows = cursor.fetchall()  # List[dict]

            # 3) pandas DataFrame
            df = pd.DataFrame(rows)
            return df
    
    def extract_sql(self,text: str) -> str | None:
        """
        从给定的字符串中提取第一个 <sql>...</sql> 标签之间的内容并返回。
        如果没找到标签，则返回 None。
        """
        pattern = re.compile(r'<sql>(.*?)</sql>', re.IGNORECASE | re.DOTALL)
        match = pattern.search(text)
        if match:
            # strip() 去掉开头结尾的多余空白或换行
            return match.group(1).strip()
        return None
