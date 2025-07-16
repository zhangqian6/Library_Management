#!/usr/bin/env python3
"""
数据库调试脚本
"""

import pymysql
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv('data.env')

def debug_database():
    """调试数据库连接和数据"""
    
    # 获取配置
    host = os.getenv('DB_HOST', 'localhost')
    port = int(os.getenv('DB_PORT', 3306))
    user = os.getenv('DB_USER', 'root')
    password = os.getenv('DB_PASSWORD', '123456')
    database = os.getenv('DB_NAME', 'vue3_auth_db')
    
    print("=== 数据库配置 ===")
    print(f"Host: {host}")
    print(f"Port: {port}")
    print(f"User: {user}")
    print(f"Password: {'*' * len(password) if password else '(空)'}")
    print(f"Database: {database}")
    print()
    
    try:
        # 1. 测试MySQL连接（不指定数据库）
        print("1. 测试MySQL服务器连接...")
        connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            charset='utf8mb4'
        )
        print("✓ MySQL服务器连接成功")
        
        cursor = connection.cursor()
        
        # 2. 检查数据库是否存在
        print("\n2. 检查数据库是否存在...")
        cursor.execute("SHOW DATABASES")
        databases = [row[0] for row in cursor.fetchall()]
        
        if database in databases:
            print(f"✓ 数据库 '{database}' 存在")
        else:
            print(f"✗ 数据库 '{database}' 不存在")
            print("正在创建数据库...")
            cursor.execute(f"CREATE DATABASE {database} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print(f"✓ 数据库 '{database}' 创建成功")
        
        # 3. 连接到指定数据库
        print(f"\n3. 连接到数据库 '{database}'...")
        connection.close()
        
        connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            charset='utf8mb4'
        )
        print("✓ 数据库连接成功")
        
        cursor = connection.cursor()
        
        # 4. 检查users表是否存在
        print("\n4. 检查users表是否存在...")
        cursor.execute("SHOW TABLES")
        tables = [row[0] for row in cursor.fetchall()]
        
        if 'users' in tables:
            print("✓ users表存在")
            
            # 5. 查看用户数据
            print("\n5. 查看用户数据...")
            cursor.execute("SELECT id, username, email, created_at FROM users")
            users = cursor.fetchall()
            
            if users:
                print(f"✓ 找到 {len(users)} 个用户:")
                for user in users:
                    print(f"  - ID: {user[0]}, 用户名: {user[1]}, 邮箱: {user[2]}, 创建时间: {user[3]}")
            else:
                print("✗ 没有找到用户数据")
        else:
            print("✗ users表不存在")
            print("这可能是导致500错误的原因")
        
        connection.close()
        
    except Exception as e:
        print(f"✗ 错误: {e}")
        print("\n可能的解决方案:")
        print("1. 检查MySQL服务是否启动")
        print("2. 检查用户名和密码是否正确")
        print("3. 检查数据库名称是否正确")

if __name__ == "__main__":
    debug_database() 