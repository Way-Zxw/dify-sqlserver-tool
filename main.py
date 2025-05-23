from dify_sqlserver_tool.tool import DifySQLServerTool

if __name__ == "__main__":
    tool = DifySQLServerTool()
    # 用于调试时显示工具定义
    print(tool.get_tool_definition()) 