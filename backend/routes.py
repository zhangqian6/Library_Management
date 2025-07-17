from flask import Blueprint, request, jsonify, session, send_file
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import db, User, Book
from werkzeug.security import generate_password_hash
import re
from io import BytesIO
import random
import string
from PIL import Image, ImageDraw, ImageFont

api = Blueprint('api', __name__)

# 邮箱验证正则表达式
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

@api.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        # 验证必需字段
        if not all(key in data for key in ['username', 'email', 'password']):
            return jsonify({
                'success': False,
                'message': '请提供用户名、邮箱和密码'
            }), 400
        
        username = data['username'].strip()
        email = data['email'].strip()
        password = data['password']
        
        # 验证用户名
        if len(username) < 3 or len(username) > 20:
            return jsonify({
                'success': False,
                'message': '用户名长度必须在3-20个字符之间'
            }), 400
        
        # 验证邮箱格式
        if not EMAIL_REGEX.match(email):
            return jsonify({
                'success': False,
                'message': '邮箱格式不正确'
            }), 400
        
        # 验证密码长度
        if len(password) < 6:
            return jsonify({
                'success': False,
                'message': '密码长度至少6个字符'
            }), 400
        
        # 检查用户名是否已存在
        if User.query.filter_by(username=username).first():
            return jsonify({
                'success': False,
                'message': '用户名已存在'
            }), 400
        
        # 检查邮箱是否已存在
        if User.query.filter_by(email=email).first():
            return jsonify({
                'success': False,
                'message': '邮箱已被注册'
            }), 400
        
        # 创建新用户
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '注册成功'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': '注册失败，请重试'
        }), 500

@api.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        # 验证必需字段
        if not all(key in data for key in ['username', 'password']):
            return jsonify({
                'success': False,
                'message': '请提供用户名和密码'
            }), 400
        
        username = data['username'].strip()
        password = data['password']
        
        # 查找用户
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            # 生成JWT token
            access_token = create_access_token(identity=user.id)
            
            return jsonify({
                'success': True,
                'token': access_token,
                'user': user.to_dict(),
                'message': '登录成功'
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': '用户名或密码错误'
            }), 401
            
    except Exception as e:
        print(e)  # 这样可以把异常打印到控制台
        return jsonify({
            'success': False,
            'message': '登录失败，请重试'
        }), 500

@api.route('/user', methods=['GET'])
@jwt_required()
def get_user_info():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if user:
            return jsonify({
                'success': True,
                'user': user.to_dict()
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': '用户不存在'
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': '获取用户信息失败'
        }), 500

@api.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    try:
        # JWT token会在客户端删除，这里只需要返回成功消息
        return jsonify({
            'success': True,
            'message': '登出成功'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': '登出失败'
        }), 500 
    
def book_to_dict(book):
    return {
        'id': book.id,
        'number': book.number,
        'title': book.title,
        'author': book.author,
        'price': book.price,
        'publish': book.publish,
        'publishDate': book.publishDate,
        'status': book.status,
    }


@api.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    return jsonify([book_to_dict(b) for b in books])

@api.route('/books', methods=['POST'])
def add_books():
    data = request.json
    required_fields = ['number', 'title', 'author', 'price', 'publish', 'publishDate']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'message': f'{field}不能为空'}), 400
    book = Book(**data)
    db.session.add(book)
    db.session.commit()
    return jsonify({
        'id': book.id,
        **data
    })

# 更新
@api.route('/books/<int:book_id>', methods=['PUT'])
def update_books(book_id):
    data = request.json
    book = Book.query.get_or_404(book_id)
    for key,value in data.items():
        setattr(book, key, value)
    db.session.commit()
    return jsonify({'message': '书籍修改成功'})

@api.route('/books/<string:book_ids>', methods = ['DELETE'])
def del_books(book_ids):
    ids = book_ids.split(',')
    deleted_count = 0

    for book_id in ids:
        try:
            book = Book.query.get(int(book_id))
            if book:
                db.session.delete(book)
                deleted_count += 1
        except ValueError:
            continue # 忽略无效的ID
    db.session.commit()
    return jsonify({'message': f'成功删除{deleted_count}本图书'})

@api.route("/get_captcha", methods = ['GET'])
def get_captcha():
    # 生成随机验证码文本
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    session['captcha'] = code  # 存储以供验证

    # 使用 PIL 生成验证码图片
    image = Image.new('RGB', (100, 40), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    draw.text((10, 10), code, font=font, fill=(0, 0, 0))

    # 返回图片
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)
    return send_file(buffer, mimetype='image/png')