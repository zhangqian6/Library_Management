#!/usr/bin/env python3
"""
手动创建数据库表脚本
"""

from flask import Flask
from config import Config
from models import db, User, bcrypt
from dotenv import load_dotenv

# 加载环境变量
load_dotenv('data.env')

def create_tables():
    """创建数据库表"""
    
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # 初始化扩展
    db.init_app(app)
    bcrypt.init_app(app)
    
    with app.app_context():
        try:
            print("正在创建数据库表...")
            db.create_all()
            print("✓ 数据库表创建成功")
            
            # 检查表是否存在
            print("\n检查表结构...")
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"✓ 找到 {len(tables)} 个表: {tables}")
            
            # 创建默认管理员用户
            print("\n检查默认管理员用户...")
            admin_user = User.query.filter_by(username='admin').first()
            if not admin_user:
                admin_user = User(
                    username='admin',
                    email='admin@example.com',
                    password='123456'
                )
                db.session.add(admin_user)
                db.session.commit()
                print("✓ 默认管理员用户已创建: admin/123456")
            else:
                print("✓ 默认管理员用户已存在")
            
            # 显示所有用户
            print("\n当前所有用户:")
            users = User.query.all()
            for user in users:
                print(f"  - ID: {user.id}, 用户名: {user.username}, 邮箱: {user.email}")
            
        except Exception as e:
            print(f"✗ 创建表失败: {e}")
            db.session.rollback()

if __name__ == "__main__":
    create_tables() 