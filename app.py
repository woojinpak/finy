from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import pandas as ps

# from sqlalchemy import create_engine
# import pymysql


# db = pymysql.connect(host='localhost', user='root', password='1234', charset='utf8')
# cursor = db.cursor()
# cursor.execute("USE finy")

# db.commit()
# db.close()

Name, Price, Platform = [], [], []
exclude = ['구매', '삽니다', '구해요', '광고']

driver = webdriver.Chrome() #셀레니움 구동

def getBunjang(itemname):
    url = f"https://m.bunjang.co.kr/search/products?order=date&page=1&q={itemname}"
    driver.get(url)

    i = 1
    while True:
        try:
            nameInfo = driver.find_element(By.XPATH, f'//*[@id="root"]/div/div/div[4]/div/div[4]/div/div[{i}]/a/div[2]/div[1]').text
            price = driver.find_element(By.XPATH, f'//*[@id="root"]/div/div/div[4]/div/div[4]/div/div[{i}]/a/div[2]/div[2]/div[1]').text
        
        except NoSuchElementException: #없으면 정지
            break

        if any(keyword in nameInfo for keyword in exclude): # 제외 키워드가 있으면 건너뛰기
            i += 1
            continue

        price_clean = price.replace(',', '').strip() #가격에서 쉼표, 공백 제거
        Name.append(nameInfo)
        Price.append(price_clean)
        Platform.append('Bunjang')
        i += 1

        

def getFruits(itemname):
    url = f'https://fruitsfamily.com/search/{itemname}'
    driver.get(url)

    i = 1
    while True:
        try:
            nameInfo = driver.find_element(By.XPATH, f'//*[@id="root"]/div[1]/section/div/div/div/div/div/ul/li[{i}]/div/div/h7').text
            price = driver.find_element(By.CSS_SELECTOR, f'#root > div.App-content > section > div > div > div > div > div > ul > li:nth-child({i}) > div > div > div.ProductsListItem-price-container > div.ProductsListItem-price.font-proxima').text

        except NoSuchElementException:
            break

        price_clean = int(price.replace('원', '').replace(',', '').strip())
        Name.append(nameInfo)
        Price.append(price_clean)
        Platform.append('FruitsFamily')
        i += 1

def getJoongna(itemname):
    url = f'https://web.joongna.com/search/{itemname}?sort=RECENT_SORT'
    driver.get(url)

    i=1
    while True:
        try:
            nameInfo = driver.find_element(By.XPATH, f'//*[@id="__next"]/div/main/div[1]/div/ul[2]/li[{i}]/a/div[2]/h2').text
            price = driver.find_element(By.XPATH, f'//*[@id="__next"]/div/main/div[1]/div/ul[2]/li[{i}]/a/div[2]/div[1]').text
        except NoSuchElementException:
            break

        price_clean = int(price.replace('원', '').replace(',', '').strip())
        Name.append(nameInfo)
        Price.append(price_clean)
        Platform.append('Joongna')
        i += 1


#검색어 입력
itemname = input("검색어 입력 : ")

#번장 가져오기
getBunjang(itemname)
#getFruits(itemname)
getJoongna(itemname)

df = ps.DataFrame({
    'Name' : Name,
    'Price' : Price,
    'Platform' : Platform
})

df.to_csv('products.csv', index=False)

print(df)