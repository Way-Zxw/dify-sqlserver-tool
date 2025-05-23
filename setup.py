from setuptools import setup, find_packages

setup(
    name="dify-sqlserver-tool",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pyodbc>=4.0.39",
        "python-dotenv>=1.0.0"
    ],
    author="Way-Zxw",
    author_email="your.email@example.com",
    description="A SQL Server tool for Dify",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Way-Zxw/dify-sqlserver-tool",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    entry_points={
        "dify_tools": [
            "sql_server=dify_sqlserver_tool.tool:DifySQLServerTool"
        ]
    }
) 