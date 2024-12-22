import time
from lxml import html
from selenium import webdriver
from .models import Product, Cookie, Source
from . import logger


class Crawler:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--log-level=3')
        driver = webdriver.Chrome(options=options)
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument",
                               {"source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"})

        self.driver = driver
        self.scrolling = True
        self.scroll_times = 4
        self.scroll_pause_time = 0.5

    def update_cookies(self):
        cookie = Cookie.query.get(self.source)
        self.cookies = cookie.cookies if cookie else []

    def search(self, keyword):
        page = self.get_search_page(keyword)
        items = self.get_products(page)

        if not items:
            logger.error(f"爬取失败：{self.source.value}需要验证，请更新 cookie")
            return []

        results = []
        for item in items:
            product = dict(
                id=self.get_product_id(item),
                url=self.get_product_url(item),
                title=self.get_product_title(item),
                price=self.get_product_price(item),
                shop_name=self.get_shop_name(item),
                shop_url=self.get_shop_url(item),
                image_url=self.get_image_url(item),
                extra_info=self.get_extra_info(item),
                source=self.source.value
            )
            if product["id"] and product["url"] and product["title"] and product["price"] and product["shop_name"] and product["shop_url"] and product["image_url"]:
                if product["url"].startswith("//"):
                    product["url"] = f"https:{product['url']}"
                if product["shop_url"].startswith("//"):
                    product["shop_url"] = f"https:{product['shop_url']}"
                results.append(product)

        logger.info(f"爬取完成：从{self.source.value}搜索到 {len(results)} 条数据")
        return results

    def get_search_page(self, keyword):
        # 添加 cookie
        self.driver.get(self.base_url)
        self.driver.delete_all_cookies()
        for cookie in self.cookies:
            self.driver.add_cookie({
                'domain': self.domain,
                'name': cookie['name'],
                'value': cookie['value'],
            })

        # 访问搜索页面
        search_url = self.search_url.format(keyword=keyword)
        logger.info(f"正在爬取：{search_url}")
        self.driver.get(search_url)

        # 模拟滚动加载
        if self.scrolling:
            for i in range(self.scroll_times):
                self.driver.execute_script(f"window.scrollTo(0, document.body.scrollHeight * {i / self.scroll_times});")
                time.sleep(self.scroll_pause_time)

        # 获取页面源码
        page = html.fromstring(self.driver.page_source)
        return page

    def get_products(self, page):
        raise NotImplementedError

    def get_product_id(self, item):
        raise NotImplementedError

    def get_product_url(self, item):
        raise NotImplementedError

    def get_product_title(self, item):
        raise NotImplementedError

    def get_product_price(self, item):
        raise NotImplementedError

    def get_shop_name(self, item):
        raise NotImplementedError

    def get_shop_url(self, item):
        raise NotImplementedError

    def get_image_url(self, item):
        raise NotImplementedError

    def get_extra_info(self, item):
        raise NotImplementedError


class JDCrawler(Crawler):
    def __init__(self):
        self.source = Source.JD
        self.domain = ".jd.com"
        self.base_url = "https://www.jd.com"
        self.search_url = "https://search.jd.com/Search?keyword={keyword}"
        super().__init__()

    def get_products(self, page):
        items = page.xpath('//*[@id="J_goodsList"]')
        if items:
            return items[0].xpath('.//li[@class="gl-item"]')
        else:
            return None

    def get_product_id(self, item):
        id = item.xpath('@data-sku')
        return id[0] if id else None

    def get_product_url(self, item):
        url = item.xpath('.//div[contains(@class, "p-name")]/a/@href')
        return url[0] if url else None

    def get_product_title(self, item):
        title = item.xpath('.//div[contains(@class, "p-name")]/a/em//text()')
        return ''.join(title)[3:] if title else None

    def get_product_price(self, item):
        price = item.xpath('.//div[@class="p-price"]/strong/i/text()')
        return float(price[0]) if price else None

    def get_shop_name(self, item):
        shop_name = item.xpath('.//a[contains(@class, "curr-shop")]/@title')
        return shop_name[0] if shop_name else None

    def get_shop_url(self, item):
        shop_url = item.xpath('.//a[contains(@class, "curr-shop")]/@href')
        return shop_url[0] if shop_url else None

    def get_image_url(self, item):
        image_url = item.xpath('.//div[@class="p-img"]/a/img/@src')
        return image_url[0] if image_url else None

    def get_extra_info(self, item):
        extra_info = {}
        priceDesc = item.xpath('.//span[contains(@class, "priceDesc")]/text()')
        if priceDesc:
            extra_info['price_desc'] = priceDesc[0]
        product_desc = item.xpath('.//i[@class="promo-words"]/text()')
        if product_desc:
            extra_info['product_desc'] = product_desc[0]
        picon_tips0 = item.xpath('.//img[contains(@class, "J-picon-tips")]/@desc')
        picon_tips1 = item.xpath('.//i[contains(@class, "J-picon-tips")]/text()')
        if picon_tips0 or picon_tips1:
            extra_info['express_and_discount'] = picon_tips0 + picon_tips1
        comment_num = item.xpath('.//div[@class="p-commit"]/strong/a/text()')
        if comment_num:
            extra_info['comment_num'] = comment_num[0].strip()
        return extra_info


class TBCrawler(Crawler):
    def __init__(self):
        self.source = Source.TB
        self.domain = ".taobao.com"
        self.base_url = "https://www.taobao.com"
        self.search_url = "https://s.taobao.com/search?q={keyword}"
        super().__init__()

    def get_products(self, page):
        items = page.xpath('//*[@id="content_items_wrapper"]')
        if items:
            return items[0].xpath('.//div[contains(@class, "tbpc-col")]')
        else:
            return None

    def get_product_id(self, item):
        id = item.xpath('.//a/@id')
        return id[0] if id else None

    def get_product_url(self, item):
        url = item.xpath('.//a/@href')
        return url[0] if url else None

    def get_product_title(self, item):
        title = item.xpath('.//div[@class="title--qJ7Xg_90 "]/span//text()')
        return ''.join(title) if title else None

    def get_product_price(self, item):
        priceInt = item.xpath('.//span[@class="priceInt--yqqZMJ5a"]/text()')
        priceFloat = item.xpath('.//span[@class="priceFloat--XpixvyQ1"]/text()')
        return float(f"{priceInt[0]}{priceFloat[0]}") if priceInt and priceFloat else None

    def get_shop_name(self, item):
        shop_name = item.xpath('.//span[contains(@class, "shopNameText--DmtlsDKm")]/text()')
        return shop_name[0] if shop_name else None

    def get_shop_url(self, item):
        shop_url = item.xpath('.//div[contains(@class, "TextAndPic--grkZAtsC")]/a/@href')
        return shop_url[0] if shop_url else None

    def get_image_url(self, item):
        image_url = item.xpath('.//img[@class="mainPic--Ds3X7I8z"]/@src')
        return image_url[0] if image_url else None

    def get_extra_info(self, item):
        extra_info = {}
        rankTitle = item.xpath('.//div[@class="rankTitle--yz_cx9ah"]/text()')
        rankSubTitle = item.xpath('.//div[@class="rankSubTitle--Pm6C_LDr"]/text()')
        if rankTitle and rankSubTitle:
            extra_info['rank'] = f"{rankTitle[0]}{rankSubTitle[0]}"
        descBox = item.xpath('.//div[@class="descBox--RunOO4S3"]/span/text()')
        if descBox:
            extra_info['product_params'] = descBox
        express_and_discount = item.xpath('.//div[contains(@class, "subIconWrapper--Vl8zAdQn")]/div/span/text()')
        if express_and_discount:
            extra_info['express_and_discount'] = express_and_discount
        location = item.xpath('.//div[@class="procity--wlcT2xH9"]/span/text()')
        if location:
            extra_info['location'] = ''.join(location)
        sales_num = item.xpath('.//span[@class="realSales--XZJiepmt"]/text()')
        if sales_num:
            extra_info['sales_num'] = sales_num[0]
        return extra_info
