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


@bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "退出登录成功"}), 200


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return redirect(url_for('main.index'))

    if current_user.is_authenticated:
        return jsonify({'message': '用户已登录'}), 401

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
            return jsonify({'message': '登录成功'}), 200
        else:
            return jsonify({'message': '用户名或密码不正确'}), 401
    else:
        return jsonify({'message': form.errors}), 401


@bp.route('/signup', methods=['GET', 'POST'])
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
        return jsonify({'message': '注册成功'}), 201
    else:
        return jsonify({'message': form.errors}), 400


@bp.route('/unregister', methods=['DELETE'])
def unregister():
    if current_user.is_authenticated:
        try:
            # 删除与当前用户相关的 price_alert 记录
            PriceAlert.query.filter_by(user_id=current_user.id).delete()
            # 删除当前用户
            db.session.delete(current_user)
            db.session.commit()
            return jsonify({'message': '注销成功'}), 200
        except IntegrityError as e:
            db.session.rollback()
            return jsonify({'message': '注销失败，数据库操作失败', 'error': str(e)}), 500
    else:
        return jsonify({'message': '用户未登录'}), 401


@bp.route('/alert', methods=['POST'])
@login_required
def set_alert():
    product = request.json
    if PriceAlert.query.filter_by(user_id=current_user.id, product_id=product['id']).first():
        return jsonify({'message': '价格提醒已设置'}), 400

    new_alert = PriceAlert(
        user_id=current_user.id,
        product_id=product['id'],
        target_price=product['price']
    )
    db.session.add(new_alert)
    db.session.commit()
    return jsonify({'message': '价格提醒设置成功'}), 201


@bp.route('/alert', methods=['GET'])
@login_required
def get_alerts():
    alerts = PriceAlert.query.filter_by(user_id=current_user.id).all()
    return jsonify([alert.to_dict() for alert in alerts]), 200


@bp.route('/alert', methods=['DELETE'])
@login_required
def delete_alert():
    product = request.json
    alert = PriceAlert.query.filter_by(user_id=current_user.id, product_id=product['id']).first()
    if not alert:
        return jsonify({'message': '价格提醒不存在'}), 404

    db.session.delete(alert)
    db.session.commit()
    return jsonify({'message': '价格提醒删除成功'}), 200
