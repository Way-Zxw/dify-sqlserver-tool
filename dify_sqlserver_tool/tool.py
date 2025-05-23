from typing import Any, Dict, List
from .sql_server_tool import SQLServerTool

class DifySQLServerTool:
    def __init__(self):
        self.db_tool = None

    @staticmethod
    def get_tool_definition() -> Dict[str, Any]:
        """返回工具定义"""
        return {
            "name": "sql_server",
            "label": "SQL Server Database",
            "description": "执行 SQL Server 数据库操作的工具",
            "parameters": {
                "type": "object",
                "required": ["operation", "query"],
                "properties": {
                    "server": {
                        "type": "string",
                        "title": "服务器地址",
                        "description": "SQL Server 服务器地址"
                    },
                    "database": {
                        "type": "string",
                        "title": "数据库名称",
                        "description": "要连接的数据库名称"
                    },
                    "username": {
                        "type": "string",
                        "title": "用户名",
                        "description": "数据库用户名"
                    },
                    "password": {
                        "type": "string",
                        "title": "密码",
                        "description": "数据库密码",
                        "format": "password"
                    },
                    "operation": {
                        "type": "string",
                        "title": "操作类型",
                        "description": "要执行的操作类型",
                        "enum": ["query", "non_query", "batch", "schema"],
                        "enumLabels": {
                            "query": "查询操作",
                            "non_query": "非查询操作",
                            "batch": "批量操作",
                            "schema": "获取表结构"
                        }
                    },
                    "query": {
                        "type": "string",
                        "title": "SQL语句",
                        "description": "要执行的SQL语句"
                    },
                    "params": {
                        "type": "array",
                        "title": "参数",
                        "description": "SQL语句的参数",
                        "items": {
                            "type": "string"
                        }
                    },
                    "batch_data": {
                        "type": "array",
                        "title": "批量数据",
                        "description": "批量操作的数据",
                        "items": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            }
                        }
                    }
                }
            }
        }

    def initialize(self, context: Dict[str, Any]) -> None:
        """初始化工具"""
        self.db_tool = SQLServerTool(
            server=context.get("server"),
            database=context.get("database"),
            username=context.get("username"),
            password=context.get("password")
        )

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """执行工具操作"""
        operation = params.get("operation")
        query = params.get("query")
        query_params = tuple(params.get("params", []))
        batch_data = params.get("batch_data", [])

        try:
            with self.db_tool:
                if operation == "query":
                    results = self.db_tool.execute_query(query, query_params)
                    return {"success": True, "data": results}
                
                elif operation == "non_query":
                    affected_rows = self.db_tool.execute_non_query(query, query_params)
                    return {"success": True, "affected_rows": affected_rows}
                
                elif operation == "batch":
                    affected_rows = self.db_tool.execute_many(query, [tuple(row) for row in batch_data])
                    return {"success": True, "affected_rows": affected_rows}
                
                elif operation == "schema":
                    schema = self.db_tool.get_table_schema(query)
                    return {"success": True, "schema": schema}
                
                else:
                    return {"success": False, "error": "不支持的操作类型"}

        except Exception as e:
            return {"success": False, "error": str(e)} 