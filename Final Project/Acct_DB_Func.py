import sqlite3
from datetime import datetime as dt
import random as rdm

conn = sqlite3.connect('Database\\book_keeping.sqlite')
cur = conn.cursor()


class Entry():
    def __init__(self, in_ex, description, ymd, price, account, record_time, sub_id):
        self.in_ex = in_ex  # income or expense?
        self.description = description  # str
        self.ymd = ymd  # Format: 2020-12-12
        self.price = price
        self.account = account  # cash / credit
        self.record_time = record_time  # str: YYYY-MM-DD HH:MM:SS.SSS
        self.sub_id = sub_id
        #self.main_id = main_id

    def parse_ymd(self):
        '''
        returns a <class: datetime.datetime> object
        '''
        ymd = self.ymd
        # covert ymd(str) into datetime obj:
        dt_obj = dt.strptime(ymd, '%Y-%m-%d')
        return dt_obj

    def add_entry(self):
        sqlstr = ''

        if self.in_ex == 'Income':
            sqlstr = '''
            INSERT INTO Income
                    (description,ymd,income,account,record_time,SubCat_id)
                VALUES
                    (?,?,?,?,?,?);
            '''
        elif self.in_ex == 'Expense':
            sqlstr = '''
            INSERT INTO Expense
                    (description,ymd,expense,account,record_time,SubCat_id)
                VALUES
                    (?,?,?,?,?,?);
            '''
        cur.execute(sqlstr, (self.description,
                             self.ymd, self.price, self.account, self.record_time, self.sub_id))
        conn.commit()

    def delete_entry(self):
        if self.in_ex == 'Income':
            sqlstr = 'DELETE FROM Income WHERE record_time=?'
        elif self.in_ex == 'Expense':
            sqlstr = 'DELETE FROM Expense WHERE record_time=?'
        cur.execute(sqlstr, (self.record_time, ))
        conn.commit()


class Expense(Entry):
    pass


class Income(Entry):
    pass


class Insights():
    def get_sum(self, timespan, category):
        pass

    def get_avg(self, timespan, category):
        pass

    def get_percentage(self, what_kind):
        pass

    def set_budget_constraint(self, timespan):
        pass


class Visualization():
    def show_bar_chart(self):
        pass

    def show_pie_chart(self):
        pass

    def show_tree(self):
        # IMPORTANT: import png
        pass


class GoogleReview():
    # goal [1]: 從地區選出好的店，再建議給使用者 (爬 店家評分 和 評論的文字)
    # goal [2]: 提供客製化的建議 (從消費習慣之類的分析... 要再討論)

    # import: bs4, requests, selenium

    # goal[2] may need to do the ones below:
    # use data from class: Insights()

    pass


def select_main_cat():
    maincats = {}
    sqlstr = 'SELECT id, MainCat FROM MainCat'
    for cat in cur.execute(sqlstr):
        cat_id = cat[0]
        cat_name = cat[1]
        print(cat_id, cat_name)
        if cat_id not in maincats.keys():
            maincats[cat_id] = cat_name

    user_choice = input('選擇記帳主類別：')  # to be replaced with drop down options
    for cat_id, name in maincats.items():
        if name == user_choice:
            return cat_id


def select_sub_cat(chosen_main_id):
    subcats = {}
    sqlstr = 'SELECT id, SubCat, MainCat_id FROM SubCat'

    for subcat in cur.execute(sqlstr):
        maincat_id = subcat[2]
        if chosen_main_id == maincat_id:
            subcat_id = subcat[0]
            subcat_name = subcat[1]
            print(subcat_id, subcat_name, maincat_id)
            if subcat_id not in subcats.keys():
                subcats[subcat_id] = subcat_name

    user_choice = input('選擇記帳子類別：')  # to be replaced with drop down options
    for sub_id, subname in subcats.items():
        if subname == user_choice:
            return sub_id


# Below only for testing: to add new record entries...
'''
num = 0
for i in range(1):
    if i==0 or 12<=i<=14:
        continue
    else:
        num += 1
        month = rdm.randint(1,12)
        month = str(month) if month >= 10 else '0'+str(month)
        day = rdm.randint(1,28)
        day = str(day) if day >= 10 else '0'+str(day)
        date = '2020-' + month + '-' + day
        price = rdm.randint(10,10000)
        timenow = dt.strptime(dt.now().isoformat(), '%Y-%m-%dT%H:%M:%S.%f')  # YYYY-MM-DD HH:MM:SS.SSS
        test = Entry('Income', 'test-'+str(199+num), date, price, 'cash', str(timenow), i)

        test.add_entry()


#test2 = Entry('Income', 'test 003', '2020-02-24', 139, 'cash', 24)

#test4.delete_entry(2)
'''
cur.close()
