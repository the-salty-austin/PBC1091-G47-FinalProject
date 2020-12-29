# import numpy
# from pandas import DataFrame
# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.naive_bayes import MultinomialNB
import random
from math import exp
import sqlite3
from selenium import webdriver
#import requests
#from bs4 import BeautifulSoup
import time

goods = "道地,貼心,大推,愉快,滿意,嫩,好吃,推薦,驚豔,精緻,親切,優,cp值高,特色,方便,氣氛佳,主動,適合,濃郁,不錯,讚,正宗,美味,細心,絕配,清爽,很棒,舒服,讚讚,再去一次,滿足,👍,😋,😍"
goods = goods.split(',')
bads = "速度慢,份量少,不怎麼樣,差,擁擠,傻眼,雷,硬,柴,難吃,失望,不新鮮,不會再來,爛,油,膩,腥,落差,惡劣,生氣,久,不配,浪費,趕人,口氣,普普,發票,拉肚子,囂張,乾,偏高,反感,服務差,吵,亂"
bads = bads.split(',')

se = '越南菜 泰國菜 印尼菜 馬來西亞菜 印度菜 新加坡菜 現代印度餐廳 越式河粉'
se = se.split(' ')
cn = '上海料理 中菜 客家料理 四川料理 餃子 台灣菜 中菜館 中國菜 粥餐廳 中式麵食 浙菜/浙江菜館 中式茶館 京菜/北京菜館 湘菜館 湯羹'
cn = cn.split(' ')
brunch = ['早午餐']
street = ['豆腐','冷麵店','麵店','熟食店']
hk = ['粵式點心','廣東料理','港式快餐店']
jp = '日式串燒 牛丼餐廳 壽司 海鮮丼餐廳 日本菜 正宗日式料理 日式牛扒餐廳 拉麵 天婦羅丼餐廳 和菓子餐廳 日式燒肉 日式炸豬扒餐廳 日式咖哩 日本地方料理餐廳'
jp = jp.split(' ')
kr = ['韓國菜', '韓式烤肉']
veg = ['嚴格素食料理', '素食料理']
wes = '傳統美式料理 現代歐洲料理 現代英國料理 法國菜 比利時菜 土耳其菜 歐陸餐廳 墨西哥菜 歐式料理 各種意大利麵 夏威夷料理 美式扒房 西班牙開胃菜 高級法式料理 拉丁美洲料理 西班牙菜 西部料理 地中海菜 德國菜 美式餐車店 意式薄餅 南義大利料理 法式餐廳 葡萄牙菜 美國菜 地中海菜 現代美式料理 意大利菜 現代法式料理牛扒 融合菜式餐廳'
wes = wes.split( )
hotel = ['酒店', '5 星級飯店', '4 星級飯店', '溫泉酒店', '3 星級飯店']
fast = ['速食']
bar = ['小餐館 (Bistro)', '啤酒花園', '居酒屋', '酒吧', '酒吧雅座', '圖書館']
sweet = ['咖啡廳', '咖啡店', '甜品店', '點心', '冰品飲料店', '觀景台', '法式糕餅店']
hotpot = ['壽喜燒餐廳', '涮涮鍋', '火鍋']

cuisine_lst = [se, cn, brunch, street, hk, jp, kr, veg, wes, hotel, fast, bar, sweet, hotpot]

driver = webdriver.Chrome()
driver.maximize_window()

def curve(x, k=0.12):
    '''
    Calculate individual score of every matched keyword
    '''
    # y=\frac{e^{ax}}{1+e^{ax}}-0.5
    score = exp(k*x)-1
    if score > 1:
        score = 1
    return score


def evaluate_review(score, review, goods, bads):
    '''
    Calculate the final score the entire comment
    new score = old score +- adjustments made by curve()
    '''
    for positive in goods:
        if positive in review:
            score += curve(len(positive))

    for negative in bads:
        if negative in review:
            score -= curve(len(negative))

    return score


def setupDB(cursor):
    cursor.executescript('''
    CREATE TABLE IF NOT EXISTS Data(
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        name TEXT UNIQUE,
        score REAL,
        cuisineID INTEGER,
        price INTEGER,
        geo TEXT
    );

    CREATE TABLE IF NOT EXISTS Cuisine(
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        cuisine TEXT UNIQUE
    );

    INSERT OR IGNORE INTO
        Cuisine(cuisine)
        VALUES
            ('東南亞料理'),('中式料理'),('早午餐'),('小吃'),('港式料理'),
            ('日式料理'),('韓式料理'),('素食'),('西式料理'),('飯店酒店'),
            ('速食'),('酒吧餐酒館'),('飲料甜品糕點'),('火鍋'),('其他'),('Bad Data')
        ;
    ''')


def write_toDB(connection, cursor, data):
    name, score, cuisine, price, geo = data[0], data[1], data[2], data[3], data[4]
    sqlstr = 'INSERT OR IGNORE INTO Data (name,score,cuisineID,price,geo) VALUES (?,?,?,?,?);'
    cursor.execute(sqlstr, (name, score, cuisine, price, geo))
    connection.commit()

def getGeo(url):
    #print('getting geo...', url)
    RETRY_LIM = 20
    driver.get(url)
    time.sleep(5)

    geo = ''
    for i in range(RETRY_LIM):
        try:
            # xpath = '//div[@jsan=\'7.ugiz4pqJLAG__primary-text,7.gm2-body-2\'][@class=\'ugiz4pqJLAG__primary-text gm2-body-2\']'
            xpath = '//button[@data-item-id=\'oloc\'][@data-tooltip=\'複製 plus code\']'
            geo = driver.find_element_by_xpath(xpath).text
            break
        except:
            time.sleep(0.5)
            continue

    #print(geo)
    
    return geo
    


conn = sqlite3.connect('Database\\scores.sqlite')
cur = conn.cursor()
setupDB(cur)

urls_csv = open(file='cleaned_urls.csv', mode='r', encoding='utf-8')

filecnt = 0
for urls_row in urls_csv:
    #print(urls_row)
    filecnt += 1

    if filecnt == 1 or urls_row.startswith('Center at'):
        continue

    else:
        urls_row = urls_row.split('"')
        url = urls_row[1]
        theRest = urls_row[2].split(',')
        #print(urls_row)
        try:
            price = int(theRest[2])
            name = theRest[3].strip()
            
            cui = theRest[1]
            for i in range(0,14):
                if cui in cuisine_lst[i]:
                    cuisine = i+1
                    break
                else:
                    cuisine = 15  # others
            
        except:
            name = 'N/A'
            price = -1
            cuisine = 16

        
        try:
            infile = open(file=f'.\\review_data\\cleaned\\cleaned_{filecnt-1}.csv', mode='r', encoding='utf-8')
            total = 0
            cnt = 0
            for line in infile:
                cnt += 1
                if cnt == 1:
                    org_avg = float(line.split(',')[-2])
                    continue

                line = line.split(',')
                r = line[0:-1]
                review = ''
                for part in r:
                    review += part

                if len(review) == 0:
                    continue

                rating = float(line[-1].strip())
                old_rating = rating

                new_rating = evaluate_review(old_rating, review, goods, bads)

                total += new_rating

                #print(review, old_rating, new_rating)

            new_avg = total/cnt
            new_avg = (0.75)*org_avg + (0.25)*new_avg

            #print(org_avg, new_avg)

            geo = getGeo(url)
            data = [name,new_avg,cuisine,price,geo]

            #print(data)
            write_toDB(conn, cur, data)
        except:
            geo = getGeo(url)
            data = [name,-1,cuisine,price,geo]
            write_toDB(conn, cur, data)


print(filecnt)