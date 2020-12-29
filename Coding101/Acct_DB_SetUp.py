'''
This file sets up the necessary database in SQLite.
'''
import sqlite3
import os

curdir = os.getcwd()
#filepath = curdir+'\\files\\book_keeping.sqlite'

print(sqlite3.sqlite_version)

if not os.path.exists('Database'):
    os.makedirs('Database')

conn = sqlite3.connect('Database\\book_keeping.sqlite')
cur = conn.cursor()

# Do some setup
cur.executescript('''
CREATE TABLE IF NOT EXISTS MainCat(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    MainCat TEXT UNIQUE
);

CREATE TABLE IF NOT EXISTS SubCat(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    SubCat TEXT UNIQUE,
    MainCat_id INTEGER
);

CREATE TABLE IF NOT EXISTS Method(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    PayMethod TEXT UNIQUE
);

CREATE TABLE IF NOT EXISTS Expense(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    description TEXT,
    cuisine_id INTEGER,
    ymd TEXT,
    price INTEGER,
    method INTEGER,
    record_time TEXT,
    SubCat_id INTEGER
);

CREATE TABLE IF NOT EXISTS Income(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    description TEXT,
    cuisine_id INTEGER,
    ymd TEXT,
    price INTEGER,
    method INTEGER,
    record_time TEXT,
    MainCat_id INTEGER
);

CREATE TABLE IF NOT EXISTS Cuisine(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    cuisine TEXT UNIQUE
);

CREATE TABLE IF NOT EXISTS Budget(
    year INTEGER,
    month INTEGER,
    amt INTEGER
);
''')

cur.executescript('''
INSERT OR IGNORE INTO
    MainCat(MainCat)
    VALUES
        ('食品酒水'),
        ('行車交通'),
        ('交流通訊'),
        ('休閒娛樂'),
        ('進修學習'),
        ('醫療保健'),
        ('金融服務'),
        ('其他支出'),
        ('薪水'),
        ('零用錢'),
        ('投資')
    ;
''')

# cur.executescript('''
# INSERT OR IGNORE INTO
#     SubCat(SubCat,MainCat_id)
#     VALUES
#         ('早餐',1),
#         ('午餐',1),
#         ('晚餐',1),
#         ('菸酒茶飲料',1),
#         ('水果零食',1)
#     ;

# INSERT OR IGNORE INTO
#     SubCat(SubCat,MainCat_id)
#     VALUES
#         ('日常用品',2),
#         ('水電瓦斯',2),
#         ('房租',2)
#     ;

# INSERT OR IGNORE INTO
#     SubCat(SubCat,MainCat_id)
#     VALUES
#         ('公共交通',3),
#         ('計程車',3),
#         ('加油',3)
#     ;

# INSERT OR IGNORE INTO
#     SubCat(SubCat,MainCat_id)
#     VALUES
#         ('公共交通',3),
#         ('計程車',3),
#         ('加油',3)
#     ;

# INSERT OR IGNORE INTO
#     SubCat(SubCat,MainCat_id)
#     VALUES
#         ('通話費',4),
#         ('有線電視費',4),
#         ('網路費',4)
#     ;

# INSERT OR IGNORE INTO
#     SubCat(SubCat,MainCat_id)
#     VALUES
#         ('朋友聚餐',5),
#         ('休閒玩樂',5),
#         ('運動健身',5),
#         ('衣物配件',5),
#         ('旅遊度假',5)
#     ;

# INSERT OR IGNORE INTO
#     SubCat(SubCat,MainCat_id)
#     VALUES
#         ('書報雜誌',6),
#         ('上課進修',6),
#     ;

# INSERT OR IGNORE INTO
#     SubCat(SubCat,MainCat_id)
#     VALUES
#         ('生病醫療',7),
#         ('保險費用',7),
#         ('美容養生',7)
#     ;

# INSERT OR IGNORE INTO
#     SubCat(SubCat,MainCat_id)
#     VALUES
#         ('手續費',8),
#         ('分期付款',8),
#         ('投資損益',8),
#         ('',8)
#     ;

# ''')

cur.executescript('''
INSERT OR IGNORE INTO
    SubCat(SubCat,MainCat_id)
    VALUES
        ('早餐',1),
        ('午餐',1),
        ('晚餐',1),
        ('菸酒茶飲料',1),
        ('水果零食',1)
    ;

INSERT OR IGNORE INTO
    SubCat(SubCat,MainCat_id)
    VALUES
        ('通勤',2)
    ;

INSERT OR IGNORE INTO
    SubCat(SubCat,MainCat_id)
    VALUES
        ('通話費',3)
    ;

INSERT OR IGNORE INTO
    SubCat(SubCat,MainCat_id)
    VALUES
        ('聚餐',4),
        ('休閒',4),
        ('旅遊',4),
        ('衣物',4)
    ;

INSERT OR IGNORE INTO
    SubCat(SubCat,MainCat_id)
    VALUES
        ('上課進修',5)
    ;

INSERT OR IGNORE INTO
    SubCat(SubCat,MainCat_id)
    VALUES
        ('看診',6),
        ('保險',6)
    ;

INSERT OR IGNORE INTO
    SubCat(SubCat,MainCat_id)
    VALUES
        ('投資損失',7),
        ('稅捐支出',7),
        ('保險費用',7)
    ;

INSERT OR IGNORE INTO
    SubCat(SubCat,MainCat_id)
    VALUES
        ('其他',8)
    ;

INSERT OR IGNORE INTO
    SubCat(SubCat,MainCat_id)
    VALUES
        ('收入',100)
    ;

''')

cur.executescript('''
INSERT OR IGNORE INTO
    Method(PayMethod)
    VALUES
        ('現金'),
        ('信用卡'),
        ('Debit卡'),
        ('行動支付')
    ;

INSERT OR IGNORE INTO
    Cuisine(cuisine)
    VALUES
        ('東南亞料理'),('中式料理'),('早午餐'),('小吃'),('港式料理'),
        ('日式料理'),('韓式料理'),('素食'),('西式料理'),('飯店酒店'),
        ('速食'),('酒吧餐酒館'),('飲料甜品糕點'),('火鍋'),('其他'),('Bad Data')
    ;
''')

for year in range(2000,2031):
    for month in range(1,13):
        cur.executescript(f'INSERT OR IGNORE INTO Budget(year,month,amt) VALUES ({year},{month},0)')