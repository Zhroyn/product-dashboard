import jieba
from sqlalchemy import or_
from concurrent.futures import ThreadPoolExecutor
from flask import Blueprint, jsonify, request
from flask_login import current_user
from app.models import Platform, Product, PriceHistory
from app.schedule import update_product_and_price
from app import db, logger, jd_crawler, tb_crawler

bp = Blueprint('product', __name__)


@bp.route('/api/cookie', methods=['PUT'])
def set_cookie():
    if not current_user.is_authenticated:
        return jsonify({'success': False, 'message': '用户未登录'})

    new_cookies = {
        Platform.JD.value: current_user.cookies[Platform.JD.value],
        Platform.TB.value: current_user.cookies[Platform.TB.value]
    }
    new_cookies[request.json['platform']] = request.json['cookie']
    current_user.cookies = new_cookies
    db.session.commit()
    return jsonify({'success': True, 'message': 'Cookies 设置成功'})


@bp.route('/api/search', methods=['GET'])
def search_in_database():
    # 对搜索关键词进行分词
    keyword = request.args.get('keyword')
    keywords = jieba.lcut(keyword)
    logger.info(f"搜索关键词：{keywords}")

    # 构建查询条件
    query_conditions = []
    for kw in keywords:
        query_conditions.append(Product.title.ilike(f"%{kw}%"))

    # 执行查询并返回查询结果，默认只返回前 100 条结果
    products = Product.query.filter(or_(*query_conditions)).all()
    products = [product.to_dict() for product in products][:100]
    return jsonify({'success': True, 'message': f'商品搜索成功，共获得{len(products)}条结果', 'products': products})


@bp.route('/api/search', methods=['PUT'])
def search_by_crawler():
    if not current_user.is_authenticated:
        return jsonify({'success': False, 'message': '用户未登录'})

    # 使用爬虫搜索商品
    keyword = request.args.get('keyword')
    jd_crawler.cookies = current_user.cookies[Platform.JD.value]
    tb_crawler.cookies = current_user.cookies[Platform.TB.value]
    with ThreadPoolExecutor(max_workers=2) as executor:
        jd_future = executor.submit(jd_crawler.search, keyword)
        tb_future = executor.submit(tb_crawler.search, keyword)
        jd_products = jd_future.result()
        tb_products = tb_future.result()

    # 保存商品信息和价格历史
    products = jd_products + tb_products
    update_product_and_price(products)

    return jsonify({'success': True, 'message': f'商品爬取成功，共获得{len(products)}条结果', 'products': products})
