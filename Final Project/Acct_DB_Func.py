import sqlite3
from datetime import datetime as dt
import random as rdm

#self.conn = sqlite3.connect('Database\\book_keeping.sqlite')
#self.cur = self.conn.cursor()



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

        for i in range(1000,1003):
            sqlstr = f'''SELECT MainCat.MainCat, MainCat.id
                        FROM MainCat
                        WHERE MainCat.id = {i}'''

            for output in self.cur.execute(sqlstr):
                cat_lst.append((output[0],output[1]))

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
    def __init__(self):
        self.conn = sqlite3.connect('Database\\scores.sqlite')
        self.cur = self.conn.cursor()
  
    def get_restaurants(self, id=1):
        #conn = sqlite3.connect('C:\\Users\\user\\Downloads\\scores.sqlite')
        #cur = conn.cursor()
        out = []
        sqlstr = f'''SELECT Data.name, Data.score, Data.price, Data.geo, Cuisine
                     FROM Data JOIN Cuisine ON Cuisine.id = Data.cuisineID
                     WHERE Cuisine.id = {id}
                     ORDER BY Data.score DESC LIMIT 20'''
        for row in self.cur.execute(sqlstr):
            out.append(row)

        return out
