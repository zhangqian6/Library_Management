from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from models import db, bcrypt
from routes import api

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # 初始化扩展
    db.init_app(app)
    bcrypt.init_app(app)
    jwt = JWTManager(app)

    # 只给这个蓝图的路由加 CORS
    CORS(api, resources={r"/*": {"origins": app.config['CORS_ORIGINS']}}, supports_credentials=True)

    # 注册蓝图
    app.register_blueprint(api, url_prefix='/api')

    
    # 创建数据库表
    with app.app_context():
        db.create_all()
        
        # 创建默认管理员用户（如果不存在）
        from models import User
        admin_user = User.query.filter_by(username='admin').first()
        if not admin_user:
            admin_user = User(
                username='admin',
                email='admin@example.com',
                password='123456'
            )
            db.session.add(admin_user)
            db.session.commit()
            print("默认管理员用户已创建: admin/123456")
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000) 