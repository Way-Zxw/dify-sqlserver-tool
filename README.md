# Dify SQL Server Tool

这是一个用于在 Dify 中操作 SQL Server 数据库的工具。该工具提供了简单且安全的方式来执行数据库操作。

## 功能特点

- 支持 Windows 身份验证和 SQL Server 身份验证
- 支持查询操作（SELECT）
- 支持非查询操作（INSERT、UPDATE、DELETE）
- 支持批量操作
- 支持获取表结构信息
- 使用参数化查询，防止 SQL 注入
- 支持上下文管理器（with 语句）
- 异常处理和自动事务回滚

## 在 Dify 中安装

1. 在 Dify 的应用设置中，选择"工具"标签页
2. 点击"添加工具"按钮
3. 选择"从 GitHub 安装"
4. 输入此工具的 GitHub 仓库地址
5. 点击"安装"按钮

## 工具配置

在 Dify 中使用此工具时，需要配置以下参数：

- `server`: SQL Server 服务器地址
- `database`: 数据库名称
- `username`: 数据库用户名
- `password`: 数据库密码
- `operation`: 操作类型（query/non_query/batch/schema）
- `query`: SQL 语句
- `params`: 查询参数（可选）
- `batch_data`: 批量操作数据（可选）

## 使用示例

### 1. 查询操作

```json
{
    "operation": "query",
    "query": "SELECT * FROM users WHERE age > ?",
    "params": ["25"]
}
```

### 2. 插入操作

```json
{
    "operation": "non_query",
    "query": "INSERT INTO users (name, age) VALUES (?, ?)",
    "params": ["张三", "30"]
}
```

### 3. 批量插入

```json
{
    "operation": "batch",
    "query": "INSERT INTO users (name, age) VALUES (?, ?)",
    "batch_data": [
        ["李四", "25"],
        ["王五", "35"],
        ["赵六", "28"]
    ]
}
```

### 4. 获取表结构

```json
{
    "operation": "schema",
    "query": "users"
}
```

## 开发环境设置

1. 克隆仓库：
```bash
git clone https://github.com/yourusername/dify-sqlserver-tool.git
cd dify-sqlserver-tool
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

## 注意事项

1. 确保已安装 SQL Server 驱动程序
2. 正确配置数据库连接信息
3. 使用参数化查询来防止 SQL 注入
4. 在生产环境中妥善保管数据库凭据

## 贡献

欢迎提交 Issue 和 Pull Request。

## 许可证

MIT 