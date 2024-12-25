from flask_apscheduler import APScheduler
from flask_mail import Mail, Message
from .crawlers import JDCrawler, TBCrawler
from .models import Platform, Product, PriceHistory, User, PriceAlert
from . import db

scheduler = APScheduler()
mail = Mail()


def update_product_and_price(products):
    for product in products:
        existing_product = Product.query.get(product['id'])
        if existing_product:
            existing_product = Product.from_dict(product)
        else:
            db.session.add(Product.from_dict(product))
        db.session.add(PriceHistory(product_id=product['id'], price=product['price']))
    db.session.commit()


def send_email(subject, recipients, body):
    msg = Message(subject, recipients=recipients, body=body)
    mail.send(msg)


def update_price_and_alert():
    with scheduler.app.app_context():
        jd_crawler = JDCrawler()
        tb_crawler = TBCrawler()
        users = User.query.all()
        searched_products = {}

        # 遍历所有用户，检查价格提醒
        for user in users:
            jd_crawler.cookies = user.cookies[Platform.JD.value]
            tb_crawler.cookies = user.cookies[Platform.TB.value]
            alerts = PriceAlert.query.filter_by(user_id=user.id).all()
            alerts = [alert.to_dict() for alert in alerts]
            for alert in alerts:
                # 尝试搜索目标商品的新价格
                if alert['product_id'] in searched_products.keys():
                    # 若商品已经搜索过，则直接使用搜索结果
                    new_price = searched_products[alert['product_id']]['price']
                else:
                    # 若商品未搜索过，则使用爬虫搜索
                    if alert['platform'] == Platform.JD.value:
                        products = jd_crawler.search(alert['title'])
                    elif alert['platform'] == Platform.TB.value:
                        products = tb_crawler.search(alert['title'])
                    # 将搜索结果保存到 searched_products 中
                    for product in products:
                        if product['id'] == alert['product_id']:
                            searched_products[alert['product_id']] = product
                    # 再次检查是否搜索到了目标商品
                    if alert['product_id'] in searched_products.keys():
                        new_price = searched_products[alert['product_id']]['price']
                    else:
                        # 若未搜索到目标商品，则跳过
                        continue

                if new_price < alert['target_price']:
                    # 发送邮件提醒
                    send_email(
                        '价格提醒',
                        [user.email],
                        f"您关注的商品《 {alert['title']} 》已经降价到 {new_price} 元"
                    )

        # 更新商品信息和价格历史
        update_product_and_price(searched_products.values())


scheduler.add_job(id='Task', func=update_price_and_alert, trigger='interval', minutes=30, misfire_grace_time=100000)
