import jieba
from concurrent.futures import ThreadPoolExecutor
from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models import Source, Product, PriceHistory
from app.schedule import update_product_and_price
from app import db, logger, jd_crawler, tb_crawler

bp = Blueprint('product', __name__)


@bp.route('/cookie', methods=['PUT'])
def set_cookie():
    if not current_user.is_authenticated:
        return jsonify({'success': False, 'message': '用户未登录'})

    new_cookies = {
        Source.JD.value: current_user.cookies[Source.JD.value],
        Source.TB.value: current_user.cookies[Source.TB.value]
    }
    new_cookies[request.json['source']] = request.json['cookies']
    current_user.cookies = new_cookies
    db.session.commit()
    return jsonify({'success': True, 'message': 'Cookies 设置成功'})


@bp.route('/search', methods=['PUT'])
def search_products_by_crawler():
    if not current_user.is_authenticated:
        return jsonify({'success': False, 'message': '用户未登录'})

    # 对搜索关键词进行分词
    keyword = request.args.get('keyword')
    keywords = jieba.lcut(keyword)
    logger.info(f"搜索关键词：{keywords}")
    keyword = ' '.join(keywords)

    # 使用爬虫搜索商品
    jd_crawler.cookies = current_user.cookies[Source.JD.value]
    tb_crawler.cookies = current_user.cookies[Source.TB.value]
    with ThreadPoolExecutor(max_workers=2) as executor:
        jd_future = executor.submit(jd_crawler.search, keyword)
        tb_future = executor.submit(tb_crawler.search, keyword)
        jd_products = jd_future.result()
        tb_products = tb_future.result()

    # 保存商品信息和价格历史
    update_product_and_price(jd_products + tb_products)

    return jsonify({
        Source.JD.value: jd_products,
        Source.TB.value: tb_products
    })


@bp.route('/history', methods=['GET'])
def get_price_history():
    product_id = request.args.get('product_id')
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'success': False, 'message': '商品不存在'})
    price_history = PriceHistory.query.filter_by(product_id=product_id).all()
    return jsonify({
        'prices': [item.price for item in price_history],
        'timestamps': [item.timestamp for item in price_history]
    })
