import os
import sys
import unittest
from dotenv import load_dotenv

def setup_test_env():
    """设置测试环境"""
    # 获取当前目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 加载测试环境配置
    env_path = os.path.join(current_dir, '.env.test')
    load_dotenv(env_path)
    
    # 添加项目根目录到 Python 路径
    project_root = os.path.dirname(current_dir)
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

def run_tests():
    """运行所有测试"""
    # 设置测试环境
    setup_test_env()
    
    # 发现并运行测试
    loader = unittest.TestLoader()
    start_dir = os.path.dirname(os.path.abspath(__file__))
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)

if __name__ == '__main__':
    run_tests() 