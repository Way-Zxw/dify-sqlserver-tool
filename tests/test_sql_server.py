import os
import unittest
from dotenv import load_dotenv
from dify_sqlserver_tool.tool import DifySQLServerTool

class TestSQLServerTool(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """设置测试环境"""
        load_dotenv()
        cls.tool = DifySQLServerTool()
        
    def test_tool_definition(self):
        """测试工具定义"""
        definition = self.tool.get_tool_definition()
        self.assertEqual(definition["name"], "sql_server")
        self.assertEqual(definition["type"], "external_tool")
        self.assertEqual(definition["api_version"], "v1")
        
    def test_tool_parameters(self):
        """测试工具参数定义"""
        definition = self.tool.get_tool_definition()
        params = definition["parameters"]["properties"]
        
        # 检查必需参数
        required = definition["parameters"]["required"]
        self.assertIn("operation", required)
        self.assertIn("query", required)
        
        # 检查参数类型
        self.assertEqual(params["server"]["type"], "string")
        self.assertEqual(params["database"]["type"], "string")
        self.assertEqual(params["username"]["type"], "string")
        self.assertEqual(params["password"]["type"], "string")
        self.assertEqual(params["operation"]["type"], "string")
        self.assertEqual(params["query"]["type"], "string")
        
        # 检查操作类型枚举值
        operations = params["operation"]["enum"]
        self.assertIn("query", operations)
        self.assertIn("non_query", operations)
        self.assertIn("batch", operations)
        self.assertIn("schema", operations)

if __name__ == '__main__':
    unittest.main() 