#!/usr/bin/env python3
"""
MySQL用户重置脚本
"""

import pymysql
import os

def create_new_user():
    """创建新的MySQL用户"""
    
    # 尝试不同的连接方式
    connection_configs = [
        # 尝试无密码连接
        {
            'host': 'localhost',
            'port': 3306,
            'user': 'root',
            'password': '',
            'charset': 'utf8mb4'
        },
        # 尝试常见密码
        {
            'host': 'localhost',
            'port': 3306,
            'user': 'root',
            'password': 'root',
            'charset': 'utf8mb4'
        },
        {
            'host': 'localhost',
            'port': 3306,
            'user': 'root',
            'password': '123456',
            'charset': 'utf8mb4'
        },
        {
            'host': 'localhost',
            'port': 3306,
            'user': 'root',
            'password': 'password',
            'charset': 'utf8mb4'
        }
    ]
    
    connection = None
    
    for config in connection_configs:
        try:
            print(f"尝试连接MySQL: {config['user']}@{config['host']}")
            connection = pymysql.connect(**config)
            print("连接成功！")
            break
        except Exception as e:
            print(f"连接失败: {e}")
            continue
    
    if not connection:
        print("\n无法连接到MySQL。请检查：")
        print("1. MySQL服务是否已启动")
        print("2. 尝试手动重置MySQL root密码")
        return
    
    try:
        cursor = connection.cursor()
        
        # 创建数据库
        database = 'vue3_auth_db'
        print(f"创建数据库: {database}")
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        
        # 创建新用户
        new_user = 'vue3_user'
        new_password = 'vue3_password'
        
        print(f"创建用户: {new_user}")
        cursor.execute(f"CREATE USER IF NOT EXISTS '{new_user}'@'localhost' IDENTIFIED BY '{new_password}'")
        cursor.execute(f"GRANT ALL PRIVILEGES ON {database}.* TO '{new_user}'@'localhost'")
        cursor.execute("FLUSH PRIVILEGES")
        
        connection.commit()
        
        print("\n=== 设置成功！ ===")
        print(f"数据库: {database}")
        print(f"用户名: {new_user}")
        print(f"密码: {new_password}")
        
        print("\n请更新 .env 文件内容为：")
        print("=" * 50)
        print("# 数据库配置")
        print(f"DB_USER={new_user}")
        print(f"DB_PASSWORD={new_password}")
        print("DB_HOST=localhost")
        print("DB_PORT=3306")
        print(f"DB_NAME={database}")
        print("")
        print("# Flask配置")
        print("SECRET_KEY=your-secret-key-here-change-in-production")
        print("JWT_SECRET_KEY=your-jwt-secret-key-here")
        print("=" * 50)
        
    except Exception as e:
        print(f"设置失败: {e}")
    finally:
        if connection:
            connection.close()

if __name__ == "__main__":
    create_new_user() 