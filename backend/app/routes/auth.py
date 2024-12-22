from flask import Blueprint, jsonify, redirect, url_for, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User
from app.forms import LoginForm, RegisterForm
from app import db, login_manager

bp = Blueprint('auth', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


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
            return jsonify({'message': '登录成功'}), 200
        else:
            return jsonify({'message': '用户名或密码不正确'}), 401
    else:
        return jsonify({'message': form.errors}), 401


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return redirect(url_for('main.index'))

    form = RegisterForm()
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


@bp.route('/unregister', methods=['GET', 'DELETE'])
def unregister():
    if request.method == 'GET':
        return redirect(url_for('main.index'))

    if current_user.is_authenticated:
        db.session.delete(current_user)
        db.session.commit()
        return jsonify({'message': '注销成功'}), 200
    else:
        return jsonify({'message': '用户未登录'}), 401
