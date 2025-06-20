import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
from sqlalchemy import create_engine

def getBunjang(itemname):
    Name, Price, Platform, Img, Url = [], [], [], [], []
    exclude = ['광고', '구매', '삽니다', '판매완료']
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)

    # 1. 번개장터 크롤링
    url = f"https://m.bunjang.co.kr/search/products?order=date&q={itemname}&page=1"
    driver.get(url)
    i = 1
    while True:
        try:
            nameInfo = driver.find_element(By.XPATH, f'//*[@id="root"]/div/div/div[4]/div/div[4]/div/div[{i}]/a/div[2]/div[1]').text
            price = driver.find_element(By.XPATH, f'//*[@id="root"]/div/div/div[4]/div/div[4]/div/div[{i}]/a/div[2]/div[2]/div[1]').text
            img = driver.find_element(By.XPATH, f'//*[@id="root"]/div/div/div[4]/div/div[4]/div/div[{i}]/a/div[1]/img').get_attribute('src')
            url_link = driver.find_element(By.XPATH, f'//*[@id="root"]/div/div/div[4]/div/div[4]/div/div[{i}]/a').get_attribute('href')
        except NoSuchElementException:
            break
        if 'ads' in img or any(keyword in nameInfo for keyword in exclude):
            i += 1
            continue
        Name.append(nameInfo)
        Price.append(price.replace(',', '').strip())
        Platform.append('번개장터')
        Img.append(img)
        Url.append(url_link)
        i += 1

    # 2. 후르츠패밀리 크롤링
    url = f'https://fruitsfamily.com/search/{itemname}'
    driver.get(url)
    i = 1
    while True:
        try:
            nameInfo = driver.find_element(By.XPATH, f'//*[@id="root"]/div[1]/section/div/div/div/div/div/ul/li[{i}]/div/div/p').text
            price = driver.find_element(By.CSS_SELECTOR, f'#root > div.App-content > section > div > div > div > div > div > ul > li:nth-child({i}) > div > div > div.ProductsListItem-price-container > div.ProductsListItem-price.font-proxima').text
            img = driver.find_element(By.XPATH, f'//*[@id="root"]/div[1]/section/div/div/div/div/div/ul/li[{i}]/div/div/div[1]/div/a/img').get_attribute('src')
            url_link = driver.find_element(By.XPATH, f'//*[@id="root"]/div[1]/section/div/div/div/div/div/ul/li[{i}]/div/div/div[1]/div/a').get_attribute('href')
        except NoSuchElementException:
            break
        if any(keyword in nameInfo for keyword in exclude):
            i += 1
            continue
        price_clean = int(price.replace('원', '').replace(',', '').strip())
        Name.append(nameInfo)
        Price.append(price_clean)
        Platform.append('후르츠패밀리')
        Img.append(img)
        Url.append(url_link)
        i += 1

    driver.quit()
    return Name, Price, Platform, Img, Url

if __name__ == '__main__':
    itemname = sys.argv[1]

    Name, Price, Platform, Img, Url = getBunjang(itemname)

    data = {
        'Name': Name,
        'Price': Price,
        'Platform': Platform,
        'Img': Img,
        'Url': Url
    }
    df = pd.DataFrame(data)
    engine = create_engine("mysql+pymysql://root:1234@localhost:3306/finy")
    db_imgs = pd.read_sql("SELECT Img FROM item", con=engine)
    db_img_set = set(db_imgs['Img'])
    df = df[~df['Img'].isin(db_img_set)]
    df = df[~df['Img'].astype(str).str.contains('ads')]
    if not df.empty:
        df.to_sql('item', con=engine, if_exists='append', index=False)