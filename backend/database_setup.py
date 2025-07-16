#!/usr/bin/env python3
"""
数据库设置脚本
用于创建数据库和配置用户
"""

import pymysql
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def create_database():
    """创建数据库和用户"""
    
    # 数据库连接参数
    host = os.getenv('DB_HOST', 'localhost')
    port = int(os.getenv('DB_PORT', 3306))
    user = os.getenv('DB_USER', 'root')
    password = os.getenv('DB_PASSWORD', '123456')
    database = os.getenv('DB_NAME', 'MySQL93')
    
    try:
        # 连接到MySQL服务器（不指定数据库）
        connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            charset='utf8mb4'
        )
        
        cursor = connection.cursor()
        
        # 创建数据库
        print(f"正在创建数据库: {database}")
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        
        # 创建专用用户（可选）
        app_user = 'vue3_user'
        app_password = 'vue3_password'
        
        print(f"正在创建用户: {app_user}")
        cursor.execute(f"CREATE USER IF NOT EXISTS '{app_user}'@'localhost' IDENTIFIED BY '{app_password}'")
        cursor.execute(f"GRANT ALL PRIVILEGES ON {database}.* TO '{app_user}'@'localhost'")
        cursor.execute("FLUSH PRIVILEGES")
        
        connection.commit()
        cursor.close()
        connection.close()
        
        print("数据库设置完成！")
        print(f"数据库名: {database}")
        print(f"用户名: {app_user}")
        print(f"密码: {app_password}")
        print("\n请更新 .env 文件中的数据库配置:")
        print(f"DB_USER={app_user}")
        print(f"DB_PASSWORD={app_password}")
        print(f"DB_NAME={database}")
        
    except Exception as e:
        print(f"数据库设置失败: {e}")
        print("\n请检查:")
        print("1. MySQL服务是否已启动")
        print("2. 用户名和密码是否正确")
        print("3. MySQL是否允许本地连接")

if __name__ == "__main__":
    create_database() 