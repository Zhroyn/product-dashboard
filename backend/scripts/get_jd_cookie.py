import json
from selenium import webdriver

driver = webdriver.Chrome()
driver.get('https://www.jd.com')
driver.get('https://search.jd.com/Search?keyword=iphone12')

input("请登录后回车退出")
cookies = driver.get_cookies()
json.dump(cookies, open("cookies_jd.json", "w", encoding="utf8"), indent=4)
print("Cookie 已保存到 cookies_jd.json")