from flask import Blueprint, jsonify, redirect, url_for, request
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy.exc import IntegrityError
from app.models import User, PriceAlert
from app.forms import LoginForm, SignupForm
from app import db, login_manager

bp = Blueprint('auth', __name__)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@bp.route('/api/logout', methods=['DELETE'])
def logout():
    if current_user.is_authenticated:
        logout_user()
        return jsonify({'success': True, 'message': '退出成功'})
    else:
        return jsonify({'success': False, 'message': '用户未登录'})


@bp.route('/api/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return redirect(url_for('main.index'))

    if current_user.is_authenticated:
        return jsonify({'success': False, 'message': '用户已登录'})

    form = LoginForm()
    if form.validate():
        account = form.account.data
        password = form.password.data
        user = User.query.filter_by(username=account).first()
        if not user:
            user = User.query.filter_by(email=account).first()
        if user and user.check_password(password):
            login_user(user)
            user.update_last_login()
            return jsonify({'success': True, 'message': '登录成功', 'user': user.to_dict()})
        else:
            return jsonify({'success': False, 'message': '用户名或密码不正确'})
    else:
        return jsonify({'success': False, 'message': form.errors})


@bp.route('/api/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return redirect(url_for('main.index'))

    form = SignupForm()
    if form.validate():
        new_user = User(
            username=form.username.data,
            email=form.email.data,
        )
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'success': True, 'message': '注册成功'})
    else:
        return jsonify({'success': False, 'message': form.errors})


@bp.route('/api/unregister', methods=['DELETE'])
def unregister():
    if not current_user.is_authenticated:
        return jsonify({'success': False, 'message': '用户未登录'})
    try:
        # 删除与当前用户相关的 price_alert 记录
        PriceAlert.query.filter_by(user_id=current_user.id).delete()
        # 删除当前用户
        db.session.delete(current_user)
        db.session.commit()
        return jsonify({'success': True, 'message': '注销成功'})
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': '注销失败，数据库操作失败', 'error': str(e)})


@bp.route('/api/verify', methods=['GET'])
def verify():
    return jsonify({'success': current_user.is_authenticated})


@bp.route('/api/user', methods=['GET'])
def get_user_info():
    if not current_user.is_authenticated:
        return jsonify({'success': False, 'message': '用户未登录'})
    return jsonify({'success': True, 'user': current_user.to_dict()})


@bp.route('/api/alert', methods=['POST'])
def set_alert():
    if not current_user.is_authenticated:
        return jsonify({'success': False, 'message': '用户未登录'})

    target_price = request.json['target_price']
    try:
        target_price = float(target_price)
    except ValueError:
        return jsonify({'success': False, 'message': '目标价格格式错误'})

    product_id = request.json['product_id']
    if PriceAlert.query.filter_by(user_id=current_user.id, product_id=product_id).first():
        return jsonify({'success': False, 'message': '价格提醒已设置'})

    new_alert = PriceAlert(
        user_id=current_user.id,
        product_id=product_id,
        target_price=target_price
    )
    db.session.add(new_alert)
    db.session.commit()
    return jsonify({'success': True, 'message': '价格提醒设置成功', 'user': current_user.to_dict()})


@bp.route('/api/alert', methods=['DELETE'])
def delete_alert():
    if not current_user.is_authenticated:
        return jsonify({'success': False, 'message': '用户未登录'})

    product = request.json
    alert = PriceAlert.query.filter_by(user_id=current_user.id, product_id=product['id']).first()
    if not alert:
        return jsonify({'success': False, 'message': '价格提醒不存在'})

    try:
        db.session.delete(alert)
        db.session.commit()
        return jsonify({'success': True, 'message': '价格提醒删除成功', 'user': current_user.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': '价格提醒删除失败', 'error': str(e)})
