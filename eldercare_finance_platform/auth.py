from flask import Blueprint, render_template, redirect, url_for, flash, request, session, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import re
import random
import time

from . import db
from .models import User

bp = Blueprint('auth', __name__, url_prefix='/auth')

# 模拟验证码存储
verification_codes = {}

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        phone = request.form['phone']
        verification_code = request.form['verification_code']
        
        # 验证手机号格式
        if not re.match(r'^1[3-9]\d{9}$', phone):
            flash('请输入正确的手机号码')
            return render_template('auth/login.html')
        
        # 验证码验证（暂时全部通过）
        # 实际项目中应该有验证码校验逻辑
        # if phone in verification_codes and verification_codes[phone]['code'] == verification_code:
        #     # 验证码正确且未过期
        #     if time.time() - verification_codes[phone]['timestamp'] <= 300:  # 5分钟有效期
        #         pass
        #     else:
        #         flash('验证码已过期，请重新获取')
        #         return render_template('auth/login.html')
        # else:
        #     flash('验证码错误')
        #     return render_template('auth/login.html')
        
        # 查找用户，如果不存在则创建
        user = User.query.filter_by(phone=phone).first()
        if user is None:
            user = User(phone=phone)
            db.session.add(user)
            db.session.commit()
        
        # 登录用户
        login_user(user)
        
        # 获取下一个页面，如果没有则默认到主页
        next_page = request.args.get('next')
        if not next_page or not next_page.startswith('/'):
            next_page = url_for('main.dashboard')
            
        return redirect(next_page)
    
    return render_template('auth/login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/send_verification_code', methods=['POST'])
def send_verification_code():
    phone = request.form['phone']
    
    # 验证手机号格式
    if not re.match(r'^1[3-9]\d{9}$', phone):
        return jsonify({'success': False, 'message': '请输入正确的手机号码'})
    
    # 生成6位随机验证码
    code = ''.join(random.choices('0123456789', k=6))
    
    # 存储验证码和时间戳（实际项目中应该存储在数据库或缓存中）
    verification_codes[phone] = {
        'code': code,
        'timestamp': time.time()
    }
    
    # 实际项目中应该有发送验证码的逻辑
    # 这里暂时模拟发送成功
    print(f"向 {phone} 发送验证码: {code}")
    
    return jsonify({'success': True, 'message': '验证码已发送'})
