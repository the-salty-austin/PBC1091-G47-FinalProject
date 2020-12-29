import sqlite3
from datetime import datetime as dt
import random as rdm

class Entry():
    def __init__(self):
        self.conn = sqlite3.connect('Database\\book_keeping.sqlite')
        self.cur = self.conn.cursor()

    def parse_ymd(self, ymd):
        '''
        returns a <class: datetime.datetime> object
        '''
        # covert ymd(str) into datetime obj:
        dt_obj = dt.strptime(ymd, '%Y-%m-%d')
        return dt_obj

    def add_entry(self, in_ex, description, cui_id, ymd, price, method, record_time, id):
        '''
        Takes 7 params: in_ex, description, ymd, price, method, record_time, sub_id
        '''
        if in_ex == 'Expense':
            sqlstr = '''
            INSERT INTO Expense
                    (description,cuisine_id,ymd,price,method,record_time,SubCat_id)
                VALUES
                    (?,?,?,?,?,?,?);
            '''
            self.cur.execute(sqlstr, (description, cui_id, ymd, price,
                                method, record_time, id))
        elif in_ex == 'Income':
            sqlstr = '''
            INSERT INTO Income
                    (description,cuisine_id,ymd,price,method,record_time,MainCat_id)
                VALUES
                    (?,?,?,?,?,?,?);
            '''
            self.cur.execute(sqlstr, (description, cui_id, ymd, price,
                                method, record_time, id))
        self.conn.commit()

    def delete_entry(self, id, in_ex):
        '''
        Takes 2 params: id, in_ex
        Deletes one entry from DB with specified id
        '''
        sqlstr = f'DELETE FROM {in_ex} WHERE id=?'
        self.cur.execute(sqlstr, (id, ))
        self.conn.commit()

    def get_entry(self, id, in_ex):
        '''
        Takes 2 params: id, in_ex
        Returns a tuple containing 7 elements:
        id,description,ymd,price,method,record_time,SubCat_id
        '''
        sqlstr = f'''SELECT id,description,cuisine_id,ymd,price,method,record_time,SubCat_id
                    FROM {in_ex} WHERE id=?'''

        for entry in self.cur.execute(sqlstr, (id, )):
            search = entry  # returns a tuple

        return search

    def update_entry(self, id, in_ex):
        '''
        Takes 2 params: id, in_ex
        '''
        # get old info
        old = self.get_entry(id, in_ex)

        # to be DBconnected to User Interface
        new = input('description, cuisine, ymd, price, method, subcat: ').split(',')

        # either inputs new data or keeps old data
        description = new[0] if len(new[0]) > 0 else old[1]
        cui_id = int(new[1]) if len(new[1]) > 0 else old[2]
        ymd = new[2] if len(new[2]) > 0 else old[3]
        price = int(new[3]) if len(new[3]) > 0 else old[4]
        method = int(new[4]) if len(new[4]) > 0 else old[5]
        sub_id = int(new[5]) if len(new[5]) > 0 else old[7]

        sqlstr = f'''UPDATE {in_ex} SET
                    (description,cuisine_id,ymd,price,method,SubCat_id)=(?,?,?,?,?,?)
                    WHERE id=?'''

        self.cur.execute(sqlstr, (description, cui_id, ymd, price,
                             method, sub_id, old[0]))
        self.conn.commit()

    def update_budget(self, year, month, budget):
        '''
        Takes 2 params: year, month
        '''

        sqlstr = f'''UPDATE Budget SET
                    amt=? WHERE year=? AND month=?'''

        self.cur.execute(sqlstr, (budget,year,month))
        self.conn.commit()

    def output_expense_categories(self):
        cat_dict = {}

        for i in range(1,9):
            sqlstr = f'''SELECT MainCat.MainCat, SubCat.SubCat, SubCat.id
                        FROM SubCat
                        JOIN MainCat ON SubCat.MainCat_id = MainCat.id
                        WHERE MainCat.id = {i}'''

            for output in self.cur.execute(sqlstr):
                #output[0]: MainCat /  output[1]: SubCat
                maincat, subcat, subcat_id = output[0], output[1], output[2]
                if maincat not in cat_dict.keys():
                    cat_dict[maincat] = [(subcat, subcat_id)]
                else:
                    cat_dict[maincat].append((subcat, subcat_id))
        
        return cat_dict

    def output_income_categories(self):
        cat_lst = []

        for i in range(9,12):
            sqlstr = f'''SELECT MainCat.MainCat, MainCat.id
                        FROM MainCat
                        WHERE MainCat.id = {i}'''

            for output in self.cur.execute(sqlstr):
                cat_lst.append((output[0],output[1]))
        print(cat_lst)
        return cat_lst


    def output_cuisine_categories(self):
        cui_lst = []

        for i in range(1,16):
            sqlstr = f'''SELECT id, cuisine
                        FROM Cuisine
                        WHERE Cuisine.id = {i}'''

            for output in self.cur.execute(sqlstr):
                cui_lst.append((output[0],output[1]))
        
        return cui_lst

    def output_paymethod_categories(self):
        pay_lst = []

        for i in range(1,5):
            sqlstr = f'''SELECT Paymethod, id FROM Method
                        WHERE Method.id = {i}'''

            for output in self.cur.execute(sqlstr):
                pay_lst.append((output[0],output[1]))
        
        return pay_lst

    


class Recommendation():
  
    def get_restaurants(id=1):
        conn = sqlite3.connect('Database\\scores.sqlite')
        cur = conn.cursor()
        
        out = []
        
        sqlstr = f'''SELECT Data.name, Data.score, Data.price, Data.geo, Cuisine
                     FROM Data JOIN Cuisine ON Cuisine.id = Data.cuisineID
                     WHERE Cuisine.id = {id}
                     ORDER BY Data.score DESC LIMIT 20'''
        for row in cur.execute(sqlstr):
            out.append(row)

        return out


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
    for cat in self.cur.execute(sqlstr):
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

    for subcat in self.cur.execute(sqlstr):
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

# test = Entry()

# num = 0
# for i in range(150):

#     num += 1
#     description = 'EX-' + str(num)
#     month = rdm.randint(1,12)
#     month = str(month) if month >= 10 else '0'+str(month)
#     day = rdm.randint(1,28)
#     day = str(day) if day >= 10 else '0'+str(day)
#     date = '2020-' + month + '-' + day
#     price = rdm.randint(10,10000)
#     method = rdm.randint(1,4)
#     timenow = dt.strptime(dt.now().isoformat(), '%Y-%m-%dT%H:%M:%S.%f')  # YYYY-MM-DD HH:MM:SS.SSS
#     cui_id = rdm.randint(1,15)
#     #cui_id = 16
#     # while True:
#     #     cat = rdm.randint(1,23)
#     #     if 12<=cat<=14:
#     #         continue
#     #     else:
#     #         break
#     cat = rdm.randint(1,18)

#     test.add_entry('Expense',description,cui_id,date,price,method,timenow,cat)

# should return a tuple
#x = test.get_entry(1, 'Expense')
#print(x)

#test.update_entry(1, 'Expense')

#test.add_entry('Income','test-100','1980-01-01',25,1,'N\\A',5)

#test.delete_entry(1, 'Income')
# test = Entry()
# cats = test.output_paymethod_categories()
# print(cats)
# #test.update_budget(2020,12,10300)

# test2 = Recommendation()
# test2.get_restaurants(1)
