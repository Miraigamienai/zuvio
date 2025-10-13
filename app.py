# 1. 導入必要的模組
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup as bs
import time

#帳號密碼
account = "@ntut.org.tw"
password = ""
#課程點名網址
check_url = "https://irs.zuvio.com.tw/student5/irs/rollcall/1437439"

# 設定 Chrome 選項為無痕模式
options = Options()
options.add_argument("--incognito")

# 2. 建立 WebDriver 實例
# 使用 webdriver_manager 自動下載並管理 ChromeDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# 3. 打開網頁
login_url = "https://irs.zuvio.com.tw/irs/login"
driver.get(login_url)

driver.find_element(By.CSS_SELECTOR, '#email').send_keys(account)
driver.find_element(By.CSS_SELECTOR, '#password').send_keys(password)
driver.find_element(By.CSS_SELECTOR, '#login-btn').click()

# 讓網頁載入一點時間
time.sleep(2)

while(True):
    driver.get(check_url)
    element = bs(driver.page_source, 'html.parser').select('#content > div.irs-rollcall > div.i-r-footer-box > div')
    if len(element):
        e = element[0]
        if element.text == '我到了':
            driver.find_element(By.CSS_SELECTOR, '#submit-make-rollcall').click()
            # 獲取當前的本地時間
            local_time = time.localtime()  # 返回 struct_time 物件
            # 格式化本地時間
            formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
            with open("check_log.txt", 'a', encoding='utf-8') as f:
                f.write(formatted_time+' 成功簽到\n')
            print(formatted_time+' 成功簽到')
        else:
            print("ERROR")
            break
    time.sleep(25)

# 8. 關閉瀏覽器
driver.quit()