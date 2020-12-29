from datetime import datetime as dt
import sqlite3

class Insights():
    def __init__(self):
        self.conn = sqlite3.connect('Database\\book_keeping.sqlite')
        self.cur = self.conn.cursor()

    def expense_entry_day(self, date):
        meat_list = []
        
        sqlstr = f'''SELECT Expense.ymd, Expense.price, MainCat.MainCat, SubCat.SubCat,
        Cuisine.cuisine, Method.PayMethod, Expense.description FROM Expense, SubCat 
        JOIN MainCat, Cuisine, Method ON Expense.SubCat_id = SubCat.id 
        AND SubCat.MainCat_id = MainCat.id 
        AND Expense.cuisine_id = Cuisine.id 
        AND Expense.method = Method.id
        WHERE Expense.ymd = '{date}'
        '''
        for meat in self.cur.execute(sqlstr):
            #print(meat)
            if meat[4]=='Bad Data':
                meat_list.append([meat[0]]+['支出']+[x for x in meat[1:4]]+['']+[x for x in meat[5:]])
            else:
                meat_list.append([meat[0]]+['支出']+[x for x in meat[1:]])
        return meat_list


    def expense_entry_day_cat(self, date, MainCat_id):
        meat_list = []
        
        
        sqlstr = f'''SELECT Expense.ymd, Expense.price, MainCat.MainCat, SubCat.SubCat,
        Cuisine.cuisine, Method.PayMethod, Expense.description FROM Expense, SubCat 
        JOIN MainCat, Cuisine, Method ON Expense.SubCat_id = SubCat.id 
        AND SubCat.MainCat_id = MainCat.id 
        AND Expense.cuisine_id = Cuisine.id 
        AND Expense.method = Method.id
        WHERE (Expense.ymd, MainCat.id) = ('{date}', {MainCat_id})
        '''
        for meat in self.cur.execute(sqlstr):
            #print(meat)
            if meat[4]=='Bad Data':
                meat_list.append([meat[0]]+['支出']+[x for x in meat[1:4]]+['']+[x for x in meat[5:]])
            else:
                meat_list.append([meat[0]]+['支出']+[x for x in meat[1:]])
        return meat_list


    def income_entry_day(self, date):
        meat_list = []
        
        
        sqlstr = f'''SELECT Income.ymd, Income.price, MainCat.MainCat, Cuisine.cuisine, 
        Method.PayMethod, Income.description FROM Income 
        JOIN MainCat, Cuisine, Method 
        ON Income.MainCat_id = MainCat.id 
        AND Income.cuisine_id = Cuisine.id 
        AND Income.method = Method.id
        WHERE Income.ymd = '{date}'
        '''
        for meat in self.cur.execute(sqlstr):
            #print(meat)
            if meat[3] == 'Bad Data':
                meat_list.append([meat[0]]+['收入']+[x for x in meat[1:3]]+['', '']+[x for x in meat[4:]])
            #else:
             #   meat_list.append([meat[0]]+['收入']+[x for x in meat[1:4]+['']+[x for x in meat[4:]]])
        #print(meat_list)
        return meat_list


    def income_entry_day_cat(self, date, category):
        meat_list = []
        
        
        sqlstr = f'''SELECT Income.ymd, Income.price, MainCat.MainCat, Cuisine.cuisine, 
        Method.PayMethod, Income.description FROM Income 
        JOIN MainCat, Cuisine, Method 
        ON Income.MainCat_id = MainCat.id 
        AND Income.cuisine_id = Cuisine.id 
        AND Income.method = Method.id
        WHERE (Income.ymd, MainCat.id) = ('{date}', {category})
        '''
        for meat in self.cur.execute(sqlstr):
            #print(meat)
            if meat[3]=='Bad Data':
                meat_list.append([meat[0]]+['收入']+[x for x in meat[1:3]]+['', '']+[x for x in meat[4:]])
            else:
                meat_list.append([meat[0]]+['收入']+[x for x in meat[1:4]+['']+[x for x in meat[4:]]])
        return meat_list


    def all_entry_day(self, date):
        tmp = self.expense_entry_day(date)
        tmp2 = self.income_entry_day(date)
        _sum = tmp + tmp2
        return _sum


    def expense_entry_period(self, date1, date2): # 全部支出
        date = date1
        stop_date = self.count_date(date2)
        _sum = []
        while True:
            _tmp = self.expense_entry_day(date)
            _sum += _tmp
            date = self.count_date(date)
            if date == stop_date:
                break
        return _sum


    def expense_entry_period_cat(self, date1, date2, MainCat_id): # 種類支出
        date = date1
        stop_date = self.count_date(date2)
        _sum = []
        while True:
            _tmp = self.expense_entry_day_cat(date, MainCat_id)
            #print(_tmp)
            #if len(_tmp) != 0:
            _sum += _tmp
            date = self.count_date(date)
            if date == stop_date:
                break
        return _sum


    def SubCat_expense_pie(self, date1, date2, MainCat_id): #種類支出 pie
        tmp = self.expense_entry_period_cat(date1, date2, MainCat_id)
        _dict = dict()
        for i in tmp:
            if i[4] not in _dict.keys():
                _dict[i[4]] = i[2]
            else:
                _dict[i[4]] += i[2]
        #print(_dict)
        total = self.period_MainCat_sum(date1, date2, MainCat_id)
        pie_list = []
        for i in _dict.items():
            a = i[1]/total
            pie_list.append([i[0], a])
        #print(pie_list)
        return pie_list


    def income_entry_period(self, date1, date2): # 全部收入
        date = date1
        stop_date = self.count_date(date2)
        _sum = []
        while True:
            _tmp = self.income_entry_day(date)
            #print(_tmp)
            #if len(_tmp) != 0:
            _sum += _tmp
            date = self.count_date(date)
            if date == stop_date:
                break
        return _sum


    def income_entry_period_cat(self, date1, date2, category): # 種類收入
        date = date1
        stop_date = self.count_date(date2)
        _sum = []
        while True:
            _tmp = self.income_entry_day_cat(date, category)
            #print(_tmp)
            #if len(_tmp) != 0:
            _sum += _tmp
            date = self.count_date(date)
            if date == stop_date:
                break
        return _sum


    def all_entry_period(self, date1, date2):# 全部
        tmp = self.expense_entry_period(date1, date2)
        tmp1 = self.income_entry_period(date1, date2)
        _sum = tmp + tmp1
        return _sum


    def day_sum(self, date):
        _sum = []
        
        
        sqlstr = ("SELECT ymd, price, SubCat_id FROM Expense WHERE ymd = "+"'"+ date +"'")
        for meat in self.cur.execute(sqlstr):
            _sum.append(meat[1])
        return sum(_sum)


    def cat_day_sum(self, date, category): # <date: str, category: int>
        _sum = []
        
        
        sqlstr = ("SELECT ymd, price, SubCat_id FROM Expense WHERE (ymd, SubCat_id) = ("
                        +"'"+ date +"'"+ ',' + str(category) + ')')
        for meat in self.cur.execute(sqlstr):
            _sum.append(meat[1])
        return sum(_sum)


    def MainCat_row(self, date, MainCat_id):
        meat_list = []
        _sum = []
        
        
        sqlstr = ("SELECT Expense.ymd, Expense.price, Expense.SubCat_id, SubCat.SubCat, MainCat.MainCat "+
                  "FROM Expense, SubCat JOIN MainCat ON Expense.SubCat_id = SubCat.id AND SubCat.MainCat_id = MainCat.id "+
                  "WHERE (MainCat.id, Expense.ymd) = (" +str(MainCat_id)+ ',' +"'"+ date +"')")
        for meat in self.cur.execute(sqlstr):
            meat_list.append(meat)
        return meat_list


    def MainCat_day_sum(self, date, MainCat_id):
        _sum = []
        meat = self.MainCat_row(date, MainCat_id)
        for i in meat:
            _sum.append(i[1])
        #print(sum(_sum))
        return sum(_sum)


    def MainCat_day_percent(self, date, category):
        a = self.MainCat_day_sum(date, category)
        b = self.day_sum(date)
        c = a/b
        #print(c)
        return c


    def count_date(self, date): # <yyyy-mm-dd>
        #print(date)
        tmp = date.split('-')
        tmp[2] = int(tmp[2]) + 1
        if len(str(tmp[2])) == 1:
            new_date = tmp[0] + '-' + tmp[1] + '-0' + str(tmp[2])
        elif len(str(tmp[2])) != 1 and tmp[2] <= 31:
            new_date = tmp[0] + '-' + tmp[1] + '-' + str(tmp[2])
        else:
            tmp[1] = int(tmp[1]) + 1
            if len(str(tmp[1])) == 1:
                new_date = tmp[0] + '-0' + str(tmp[1]) + '-01'
            elif len(str(tmp[1])) != 1 and tmp[1] <= 12:
                new_date = tmp[0] + '-' + str(tmp[1]) + '-01'
            else:
                tmp[0] = int(tmp[0]) + 1
                new_date = str(tmp[0]) + '-01-01'
        return new_date


    def period_sum(self, date1, date2):
        date = date1
        stop_date = self.count_date(date2)
        _sum = []
        while True:
            _tmp = self.day_sum(date)
            _sum.append(_tmp)
            date = self.count_date(date)
            if date == stop_date:
                break
        return sum(_sum)


    def period_avg(self, date1, date2):
        date = date1
        stop_date = self.count_date(date2)
        _sum = []
        count = 0
        while True:
            _tmp = self.day_sum(date)
            _sum.append(_tmp)
            date = self.count_date(date)
            if date == stop_date:
                break
            count += 1
        a = sum(_sum)/count
        return a


    def period_cat_sum(self, date1, date2, category):
        date = date1
        stop_date = self.count_date(date2)
        _sum = []
        while True:
            _tmp = self.cat_day_sum(date, category)
            _sum.append(_tmp)
            date = self.count_date(date)
            if date == stop_date:
                break
        return sum(_sum)


    def period_MainCat_sum(self, date1, date2, category):  # 種類支出和
        date = date1
        stop_date = self.count_date(date2)
        _sum = []
        while True:
            _tmp = self.MainCat_day_sum(date, category)
            _sum.append(_tmp)
            date = self.count_date(date)
            if date == stop_date:
                break
        return sum(_sum)


    def MainCat_period_percent(self, date1, date2, category):
        a = self.period_MainCat_sum(date1, date2, category)
        b = self.period_sum(date1, date2)
        c = a/b
        #print(c)
        return c
 
    def MainCat_day_pie(self, date, category_list):
        pie_chart = []

        for i in category_list:
            _tmp = self.MainCat_day_percent(date, i)
            tmp_list = [i, _tmp]
            #print(tmp_list)
            pie_chart.append(tmp_list)
        return pie_chart

    def MainCat_expense_pie(self, date1, date2, category_list):  # 全部 expense pie_chart
        pie_chart = []

        MainCat_dict = {1: 'food', 2: 'transportation', 3: 'communication', 4: 'leisure', 5: 'education', 6: 'medical service',
                        7: 'financial service', 8: 'others'}

        others = 0
        for i in category_list:
            _percent = self.MainCat_period_percent(date1, date2, i)
            _tmp = self.period_MainCat_sum(date1, date2, i)
            if _percent >= 0.01 and i != 8:
                pie_chart.append([MainCat_dict[i], _tmp])
            elif i == 8 and others + _tmp != 0:
                others += _tmp
                pie_chart.append([MainCat_dict[i], others])
            else:
                others += _tmp
        return pie_chart
    # def MainCat_expense_pie(self, date1, date2, category_list):  # 全部 expense pie_chart
    #     pie_chart = []
    #     for i in category_list:
    #         _tmp = self.period_MainCat_sum(date1, date2, i)
    #         tmp_list = [i, _tmp]
    #         #print(tmp_list)
    #         pie_chart.append(tmp_list)
    #     return pie_chart


    def income_day_sum(self, date):
        _sum = []
        
        sqlstr = ("SELECT ymd, price FROM Income WHERE ymd = "+"'"+ date +"'")
        for meat in self.cur.execute(sqlstr):
            _sum.append(meat[1])
        return sum(_sum)


    def income_MainCat_row(self, date, MainCat_id):
        meat_list = []
        _sum = []

        sqlstr = f'''SELECT Income.ymd, Income.price, MainCat.MainCat FROM Income 
        JOIN MainCat ON Income.MainCat_id = MainCat.id
        WHERE (MainCat.id, Income.ymd) = ({MainCat_id}, '{date}')
        '''
        for meat in self.cur.execute(sqlstr):
            meat_list.append(meat)
        return meat_list


    def income_MainCat_day_sum(self, date, MainCat_id):
        _sum = []
        meat = self.income_MainCat_row(date, MainCat_id)
        for i in meat:
            _sum.append(i[1])
        #print(sum(_sum))
        return sum(_sum)


    def income_period_sum(self, date1, date2):
        date = date1
        stop_date = self.count_date(date2)
        _sum = []
        while True:
            _tmp = self.income_day_sum(date)
            _sum.append(_tmp)
            date = self.count_date(date)
            if date == stop_date:
                break
        return sum(_sum)


    def income_period_MainCat_sum(self, date1, date2, category):  # 種類 income 和
        date = date1
        stop_date = self.count_date(date2)
        _sum = []
        while True:
            _tmp = self.income_MainCat_day_sum(date, category)
            _sum.append(_tmp)
            date = self.count_date(date)
            if date == stop_date:
                break
        return sum(_sum)


    def income_MainCat_period_percent(self, date1, date2, category):
        a = self.income_period_MainCat_sum(date1, date2, category)
        b = self.income_period_sum(date1, date2)
        c = a/b
        #print(c)
        return c


    def MainCat_income_pie(self, date1, date2, category_list):  # 全部 income pie_chart
        pie_chart = []
        for i in category_list:
            _tmp = self.income_period_MainCat_sum(date1, date2, i)
            tmp_list = [i, _tmp]
            #print(tmp_list)
            pie_chart.append(tmp_list)
        return pie_chart


    def highest_cuisine(self):
        cui_expense = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0, 13:0, 14:0, 15:0}

        for cui in range(1,16):
            sqlstr = f'SELECT Expense.price FROM Expense WHERE Expense.cuisine_id = {cui}'
            for row in self.cur.execute(sqlstr):
                cui_expense[cui] += int(row[0])

        highest_id = 1
        highest_expense = 0

        for cui, expense in cui_expense.items():
            if expense > highest_expense:
                highest_expense = expense
                highest_id = cui

        return highest_id


    def check_budget(self, year, month):
        md = {1:31, 2:28, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 12:31}
        Lmd = {1:31, 2:29, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 12:31}

        sqlstr = f'''SELECT amt FROM Budget WHERE year={year} AND month={month} LIMIT 1'''
        for row in self.cur.execute(sqlstr):
            budget = int(row[0])

        isLeap = False
        if (year % 4) == 0:
            if (year % 100) == 0:
                if (year % 400) == 0:
                    isLeap = True
            else:
                isLeap = True

        m = str(month)
        if len(str(month)) == 1:
            m = '0'+str(month)
        beg = f'{str(year)}-{m}-01'
        end = f'{str(year)}-{m}-{Lmd[month]}' if isLeap else f'{str(year)}-{m}-{md[month]}'

        beg = dt.strptime(beg, '%Y-%m-%d')
        end = dt.strptime(end, '%Y-%m-%d')

        sqlstr = f'SELECT Expense.ymd, Expense.price FROM Expense'

        _sum = 0
        for row in self.cur.execute(sqlstr):
            ymd = dt.strptime(row[0], '%Y-%m-%d')
            if end>=ymd>=beg:
                _sum += row[1]
            else:
                continue

        if _sum>budget:
            overBudget = True
        elif _sum<=budget:
            overBudget = False
        try:
            percentage = f'{(round(_sum/float(budget),3))*100}%'
        except:
            percentage = '0%'
        return budget, _sum, percentage, overBudget
