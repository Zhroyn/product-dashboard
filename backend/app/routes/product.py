import jieba
from concurrent.futures import ThreadPoolExecutor
from flask import Blueprint, jsonify, request
from app.models import Product, Cookie, Source
from app import db, logger, jd_crawler, tb_crawler

bp = Blueprint('product', __name__)

# 使用爬虫搜索商品
@bp.route('/product/search', methods=['GET'])
def search_product():
    keyword = request.args.get('keyword')
    keywords = jieba.lcut(keyword)
    logger.info(f"搜索关键词：{keywords}")
    keyword = ' '.join(keywords)

    jd_crawler.update_cookies()
    tb_crawler.update_cookies()

    with ThreadPoolExecutor(max_workers=2) as executor:
        jd_future = executor.submit(jd_crawler.search, keyword)
        tb_future = executor.submit(tb_crawler.search, keyword)
        jd_products = jd_future.result()
        tb_products = tb_future.result()

    results = {
        Source.JD.value: jd_products,
        Source.TB.value: tb_products
    }
    return jsonify(results)

# 获取数据库中的所有商品
@bp.route('/product', methods=['GET'])
def get_products():
    products = Product.query.all()
    result = [dict(
        id=product.id,
        url=product.url,
        title=product.title,
        price=product.price,
        shop_name=product.shop_name,
        shop_url=product.shop_url,
        image_url=product.image_url,
        extra_info=product.extra_info,
        source=product.source.value
    ) for product in products]
    return jsonify(result)

# 向数据库中添加商品
@bp.route('/product', methods=['POST'])
def create_product():
    data = request.json
    if Product.query.get(data['id']):
        return jsonify({'message': 'Product already exists'}), 400
    new_product = Product(
        id=data['id'],
        url=data['url'],
        title=data['title'],
        price=data['price'],
        shop_name=data['shop_name'],
        shop_url=data['shop_url'],
        image_url=data['image_url'],
        extra_info=data['extra_info'],
        source=Source(data['source'])
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify({'message': 'Product created successfully'}), 201

# 设置 Cookie
@bp.route('/cookie', methods=['POST'])
def set_cookie():
    data = request.json
    cookie = Cookie.query.get(Source(data['source']))
    if cookie:
        cookie.cookies = data['cookies']
    else:
        cookie = Cookie(
            source=Source(data['source']),
            cookies=data['cookies']
        )
        db.session.add(cookie)
    db.session.commit()
    return jsonify({'message': 'Cookie set successfully'}), 201