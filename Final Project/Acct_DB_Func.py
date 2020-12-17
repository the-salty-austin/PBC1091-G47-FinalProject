import sqlite3
from datetime import datetime as dt
import random as rdm

conn = sqlite3.connect('Database\\book_keeping.sqlite')
cur = conn.cursor()

class Entry():
    #def __init__(self, in_ex, description, ymd, price, account, record_time, sub_id):
    #def __init__(self):
        #self.conn = sqlite3.connect('Database\\book_keeping.sqlite')
        #self.cur = self.conn.cursor()
        #self.in_ex = in_ex  # income or expense?
        #self.description = description  # str
        #self.ymd = ymd  # Format: 2020-12-12
        #self.price = price
        #self.account = account  # cash / credit
        #self.record_time = record_time  # str: YYYY-MM-DD HH:MM:SS.SSS
        #self.sub_id = sub_id
        #self.main_id = main_id

    def parse_ymd(self, ymd):
        '''
        returns a <class: datetime.datetime> object
        '''
        # covert ymd(str) into datetime obj:
        dt_obj = dt.strptime(ymd, '%Y-%m-%d')
        return dt_obj

    def add_entry(self, in_ex, description, ymd, price, account, record_time, sub_id):
        '''
        Takes 7 params: in_ex, description, ymd, price, account, record_time, sub_id
        '''
        sqlstr = f'''
        INSERT INTO {in_ex}
                (description,ymd,price,account,record_time,SubCat_id)
            VALUES
                (?,?,?,?,?,?);
        '''
        cur.execute(sqlstr, (description, ymd, price,
                             account, record_time, sub_id))
        conn.commit()

    def delete_entry(self, id, in_ex):
        '''
        Takes 2 params: id, in_ex
        Deletes one entry from DB with specified id
        '''
        sqlstr = f'DELETE FROM {in_ex} WHERE id=?'
        cur.execute(sqlstr, (id, ))
        conn.commit()

    def get_entry(self, id, in_ex):
        '''
        Takes 2 params: id, in_ex
        Returns a tuple containing 7 elements:
        id,description,ymd,price,account,record_time,SubCat_id
        '''
        sqlstr = f'''SELECT id,description,ymd,price,account,record_time,SubCat_id
                    FROM {in_ex} WHERE id=?'''

        for entry in cur.execute(sqlstr, (id, )):
            search = entry  # returns a tuple

        return search

    def update_entry(self, id, in_ex):
        '''
        Takes 2 params: id, in_ex
        '''
        # get old info
        old = self.get_entry(id, in_ex)

        # to be connected to User Interface
        new = input('description, ymd, price, account, subcat: ').split(',')

        # either inputs new data or keeps old data
        description = new[0] if len(new[0]) > 0 else old[1]
        ymd = new[1] if len(new[1]) > 0 else old[2]
        price = int(new[2]) if len(new[2]) > 0 else old[3]
        account = int(new[3]) if len(new[3]) > 0 else old[4]
        sub_id = int(new[4]) if len(new[4]) > 0 else old[6]

        sqlstr = f'''UPDATE {in_ex} SET
                    (description,ymd,price,account,SubCat_id)=(?,?,?,?,?)
                    WHERE id=?'''

        cur.execute(sqlstr, (description, ymd, price,
                             account, sub_id, old[0]))
        conn.commit()

        
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
test = Entry()

num = 1
for i in range(1000):

    num += 1
    description = 'EX-' + str(num)
    month = rdm.randint(1,12)
    month = str(month) if month >= 10 else '0'+str(month)
    day = rdm.randint(1,28)
    day = str(day) if day >= 10 else '0'+str(day)
    date = '2020-' + month + '-' + day
    price = rdm.randint(10,10000)
    payment = rdm.randint(1,4)
    timenow = dt.strptime(dt.now().isoformat(), '%Y-%m-%dT%H:%M:%S.%f')  # YYYY-MM-DD HH:MM:SS.SSS
    while True:
        cat = rdm.randint(1,27)
        if 12<=cat<=14:
            continue
        else:
            break

    test.add_entry('Expense',description,date,price,payment,timenow,cat)
'''
# should return a tuple
#x = test.get_entry(1, 'Expense')
#print(x)

#test.update_entry(1, 'Expense')

#test.add_entry('Income','test-100','1980-01-01',25,1,'N\\A',5)

#test.delete_entry(1, 'Income')
cur.close()
