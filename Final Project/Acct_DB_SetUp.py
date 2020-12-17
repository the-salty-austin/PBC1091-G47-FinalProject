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
    ymd TEXT,
    price INTEGER,
    method INTEGER,
    record_time TEXT,
    SubCat_id INTEGER
);

CREATE TABLE IF NOT EXISTS Income(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    description TEXT,
    ymd TEXT,
    price INTEGER,
    method INTEGER,
    record_time TEXT,
    SubCat_id INTEGER
);
''')

cur.executescript('''
INSERT OR IGNORE INTO
    MainCat(MainCat)
    VALUES
        ('食品酒水'),
        ('居家物業'),
        ('行車交通'),
        ('交流通訊'),
        ('休閒娛樂'),
        ('進修學習'),
        ('醫療保健'),
        ('投資發財'),
        ('其他雜項')
    ;
''')

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
        ('日常用品',2),
        ('水電瓦斯',2),
        ('房租',2)
    ;

INSERT OR IGNORE INTO
    SubCat(SubCat,MainCat_id)
    VALUES
        ('公共交通',3),
        ('計程車',3),
        ('加油',3)
    ;

INSERT OR IGNORE INTO
    SubCat(SubCat,MainCat_id)
    VALUES
        ('公共交通',3),
        ('計程車',3),
        ('加油',3)
    ;

INSERT OR IGNORE INTO
    SubCat(SubCat,MainCat_id)
    VALUES
        ('通話費',4),
        ('有線電視費',4),
        ('網路費',4)
    ;

INSERT OR IGNORE INTO
    SubCat(SubCat,MainCat_id)
    VALUES
        ('朋友聚餐',5),
        ('休閒玩樂',5),
        ('運動健身',5),
        ('旅遊度假',5)
    ;

INSERT OR IGNORE INTO
    SubCat(SubCat,MainCat_id)
    VALUES
        ('書報雜誌',6),
        ('上課進修',6),
        ('學雜費',6)
    ;

INSERT OR IGNORE INTO
    SubCat(SubCat,MainCat_id)
    VALUES
        ('生病醫療',7),
        ('保險費用',7),
        ('美容養生',7)
    ;

INSERT OR IGNORE INTO
    SubCat(SubCat,MainCat_id)
    VALUES
        ('建置中1',8),
        ('建置中2',9)
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
''')
