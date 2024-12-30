import json
from selenium import webdriver

driver = webdriver.Chrome()
driver.get('https://s.taobao.com/search?q=iphone12')

input("请登录后回车退出")
cookies = driver.get_cookies()
json.dump(cookies, open("cookies_tb.json", "w", encoding="utf8"), indent=4)
print("Cookie 已保存到 cookies_tb.json")