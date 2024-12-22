from flask import Blueprint, send_from_directory

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return send_from_directory('static', 'index.html')

@bp.route('/<path:path>')
def static_files(path):
    return send_from_directory('static', path)