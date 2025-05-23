import os
import pyodbc
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

class SQLServerTool:
    def __init__(self, server: str, database: str, username: str, password: str, 
                 driver: str = "SQL Server", trusted_connection: bool = False):
        """
        初始化 SQL Server 连接工具
        
        Args:
            server: 服务器地址
            database: 数据库名称
            username: 用户名
            password: 密码
            driver: 数据库驱动名称
            trusted_connection: 是否使用 Windows 身份验证
        """
        self.server = server
        self.database = database
        self.username = username
        self.password = password
        self.driver = driver
        self.trusted_connection = trusted_connection
        self.conn = None
        self.cursor = None

    def connect(self) -> None:
        """建立数据库连接"""
        try:
            if self.trusted_connection:
                conn_str = f"DRIVER={{{self.driver}}};SERVER={self.server};DATABASE={self.database};Trusted_Connection=yes;"
            else:
                conn_str = f"DRIVER={{{self.driver}}};SERVER={self.server};DATABASE={self.database};UID={self.username};PWD={self.password}"
            
            self.conn = pyodbc.connect(conn_str)
            self.cursor = self.conn.cursor()
            print("数据库连接成功！")
        except Exception as e:
            raise Exception(f"数据库连接失败: {str(e)}")

    def disconnect(self) -> None:
        """关闭数据库连接"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
            print("数据库连接已关闭！")

    def execute_query(self, query: str, params: tuple = None) -> List[Dict[str, Any]]:
        """
        执行查询语句并返回结果
        
        Args:
            query: SQL 查询语句
            params: 查询参数元组
        
        Returns:
            查询结果列表，每个元素为字典形式
        """
        try:
            if not self.conn or not self.cursor:
                self.connect()
            
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            
            columns = [column[0] for column in self.cursor.description]
            results = []
            
            for row in self.cursor.fetchall():
                results.append(dict(zip(columns, row)))
            
            return results
        except Exception as e:
            raise Exception(f"查询执行失败: {str(e)}")

    def execute_non_query(self, query: str, params: tuple = None) -> int:
        """
        执行非查询语句（INSERT, UPDATE, DELETE）
        
        Args:
            query: SQL 语句
            params: 查询参数元组
        
        Returns:
            受影响的行数
        """
        try:
            if not self.conn or not self.cursor:
                self.connect()
            
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            
            self.conn.commit()
            return self.cursor.rowcount
        except Exception as e:
            self.conn.rollback()
            raise Exception(f"执行失败: {str(e)}")

    def execute_many(self, query: str, params: List[tuple]) -> int:
        """
        批量执行SQL语句
        
        Args:
            query: SQL 语句
            params: 参数列表，每个元素为一个元组
        
        Returns:
            受影响的行数
        """
        try:
            if not self.conn or not self.cursor:
                self.connect()
            
            self.cursor.executemany(query, params)
            self.conn.commit()
            return self.cursor.rowcount
        except Exception as e:
            self.conn.rollback()
            raise Exception(f"批量执行失败: {str(e)}")

    def get_table_schema(self, table_name: str) -> List[Dict[str, Any]]:
        """
        获取表结构信息
        
        Args:
            table_name: 表名
        
        Returns:
            表结构信息列表
        """
        query = f"""
        SELECT 
            c.name as column_name,
            t.name as data_type,
            c.max_length,
            c.precision,
            c.scale,
            c.is_nullable
        FROM sys.columns c
        JOIN sys.types t ON c.user_type_id = t.user_type_id
        WHERE c.object_id = OBJECT_ID(?)
        """
        return self.execute_query(query, (table_name,))

    def __enter__(self):
        """上下文管理器入口"""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        self.disconnect() 