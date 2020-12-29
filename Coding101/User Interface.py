import tkinter as tk
from tkinter import ttk
from tkinter import Tk, Canvas
import tkinter.messagebox
from PIL import Image, ImageTk
from datetime import datetime as dt
from matplotlib import pyplot
import time

import Acct_DB_Func as db
import functions


database = db.Entry()
func = functions.Insights()

food = database.output_cuisine_categories()
pure_food_list = []
pure_food_number_list = []
for i in food:
    pure_food_list += [i[1]]
    pure_food_number_list += [i[0]]
food_list = ['無 / 不適用'] + pure_food_list

in_sort_match = database.output_income_categories() #income

in_sort = []
in_sort_number_list = []
for i in in_sort_match:
    in_sort += [i[0]]
    in_sort_number_list += [i[1]]

sort_dict = database.output_expense_categories()
out_sort = [x for x in sort_dict.keys()]
sort = ['-----------收入-----------'] + in_sort + ['-----------支出-----------', ] + out_sort
sort_for_check = ['全部', '收入', '支出']
out_sort_match = database.output_cuisine_categories()
out_sort_number_list = [1,2,3,4,5,6,7,8]

sort_dict_simple = {}
for i in sort_dict:
    sort_dict_simple[i] = []
    for j in sort_dict[i]:
        sort_dict_simple[i] += [j[0]]

small_sort = ['收入', '--------------------------']
pure_small_sort = []
pure_small_sort_number = []
for i in out_sort:
    for j in sort_dict[i]:
        small_sort += [j[0]]
        pure_small_sort += [j[0]]
        pure_small_sort_number += [j[1]]
    small_sort += ['--------------------------']

way = database.output_paymethod_categories() #paymethod

way_list = []
way_number_list = []
for i in way:
    way_list += [i[0]]
    way_number_list += [i[1]]

MAT_FONT = ('UD Digi Kyokasho NK-R', 22, 'bold')
LARGE_FONT = ('UD Digi Kyokasho NK-R', 18, 'bold')
MEDIUM_FONT = ('UD Digi Kyokasho NK-R', 15, 'bold')
SMALL_FONT = ('UD Digi Kyokasho NK-R', 11)
SMALLER_FONT = ('UD Digi Kyokasho NK-R', 9)
CONGRATS_FONT = ('UD Digi Kyokasho NK-R', 20)

year_list = []
for i in range(2019, 2026):
    year_list += [str(i)]
month_list = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
the_thirties = ['Apr', 'Jun', 'Sep', 'Nov']
day_list = []
for i in range(1,32):
    day_list += [str(i)]


Main_id_dict = {'食品酒水': 1, '行車交通': 2, '交流通訊': 3, 
                '休閒娛樂': 4, '進修學習': 5, '醫療保健': 6,
                '金融服務': 7, '其他支出': 8}

in_sort_english = ['salary', 'allowance', 'investment']
out_sort_english = ['food', 'transportation', 'communication', 'leisure', 'education', 'medical service', 'financial service', 'others']


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.wm_title('MY ACCOUNTING TREE')
        
        container = tk.Frame(self)
        
        container.pack(side="top", fill='both', expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, InputPage, GoalPage,CheckPage, RewardPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame(StartPage)
    
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, root):
        super().__init__(parent)
        label = tk.Label(self, text='MY ACCOUNTING TREE', font=MAT_FONT, bg='Thistle')
        label.pack(pady=20,padx=10)

        button1 = tk.Button(self, text='輸入收支', font=SMALL_FONT, command=lambda: root.show_frame(InputPage)).pack()
        button2 = tk.Button(self, text='設定花費預算', font=SMALL_FONT, command=lambda: root.show_frame(GoalPage)).pack()
        button3 = tk.Button(self, text='檢視收支狀況', font=SMALL_FONT, command=lambda: root.show_frame(CheckPage)).pack()
        button4 = tk.Button(self, text='好好犒賞自己吧！', font=SMALL_FONT, command=lambda: root.show_frame(RewardPage)).pack()

class InputPage(tk.Frame):
    def __init__(self, parent, root):
        super().__init__(parent)
        topic = tk.Label(self, text='輸入收支', font=LARGE_FONT)
        topic.pack(pady=20) # 上下留空間

        # 日期
        date_topic = tk.Label(self, text='*選擇日期（年月日)：', font=SMALL_FONT).pack()

        year_box = ttk.Combobox(self)
        year_box['values'] = tuple(year_list)
        year_box.pack()
        month_box = ttk.Combobox(self)
        month_box['values'] = tuple(month_list)
        month_box.pack()
        day_box = ttk.Combobox(self)
        day_box['values'] = tuple(day_list)
        day_box.pack()


        # 收或支多少、取得類別(有互動)
        space1 = tk.Label(self, text='').pack()
        money_topic = tk.Label(self, text='*金額：', font=SMALL_FONT).pack()

        radioValue = tk.IntVar()
        income_box = tk.Radiobutton(self, text='收入', font=SMALLER_FONT, variable=radioValue, value=0).pack()
        expense_box = tk.Radiobutton(self, text='支出', font=SMALLER_FONT, variable=radioValue, value=1).pack()

        amount_var = tk.StringVar()
        amount_box = tk.Entry(self, textvariable=amount_var, bd=1).pack() # bd = 邊框


        # 類別
        space2 = tk.Label(self, text='').pack()
        sort_topic = tk.Label(self, text='*主分類：', font=SMALL_FONT).pack()

        sort_box = ttk.Combobox(self)
        sort_box['values'] = tuple(sort)
        sort_box.pack()
        
        #子類別
        space13 = tk.Label(self, text='').pack()
        small_sort_topic = tk.Label(self, text='*子分類：', font = SMALL_FONT).pack()

        small_sort_box = ttk.Combobox(self)
        small_sort_box['values'] = tuple(small_sort)
        small_sort_box.pack()
        
        # 飲食類別
        space12 = tk.Label(self, text='').pack()
        food_topic = tk.Label(self, text='飲食類別：', font=SMALL_FONT).pack()
        
        food_box = ttk.Combobox(self)
        food_box['values'] = tuple(food_list)
        food_box.pack()

        # 金融方式
        space3 = tk.Label(self, text='').pack()
        way_topic = tk.Label(self, text='*方式：', font=SMALL_FONT).pack()

        way_box = ttk.Combobox(self)
        way_box['values'] = tuple(way_list)
        way_box.pack()

        # 備註
        space4 = tk.Label(self, text='').pack()
        btw_topic = tk.Label(self, text='備註：', font=SMALL_FONT).pack()

        btw_var = tk.StringVar()
        btw = tk.Entry(self, textvariable=btw_var, bd=1).pack()

        def confirm_everything_func():
            # =0：正確、=-1：錯誤
            def confirm_date_func(): 
                test_temp = 0 
                if (year_box.get()== '') or (month_box.get()=='') or (day_box.get()==''):
                    test_temp = -1
                if month_box.get() in the_thirties:
                    if day_box.get() == '31':
                        test_temp = -1
                elif month_box.get() == 'Feb':
                    if (int(year_box.get()) == 2100) or (int(year_box.get())%4 != 0):
                        if int(day_box.get()) > 28:
                            test_temp = -1
                    elif int(year_box.get())%4 == 0: 
                        if int(day_box.get()) > 29:
                            test_temp = -1
                return test_temp
            
            def confirm_amount_func():
                test_temp = 0
                if (amount_var.get()).isdigit() == False:
                    test_temp = -1
                elif int(amount_var.get()) <= 0:
                    test_temp = -1
                return test_temp

            def confirm_sort_func():
                test_temp = 0
                if sort_box.get() == '':
                    test_temp = -1
                if sort_box.get() == '-----------收入-----------':
                    test_temp = -1
                if sort_box.get() == '-----------支出-----------':
                    test_temp = -1
                return test_temp

            def confirm_small_sort_func():
                test_temp = 0
                if radioValue.get() == 0 and small_sort_box.get() != '收入':
                    test_temp = -1
                if small_sort_box.get() == '--------------------------':
                    test_temp = -1
                if (sort_box.get() in out_sort) and (small_sort_box.get() not in sort_dict_simple[sort_box.get()]):
                    test_temp = -1
                return test_temp
            
            def confirm_food_func():
                test_temp = 0
                if (sort_box.get() == '食品酒水') and (food_box.get() == ''):
                    test_temp = -1
                elif (sort_box.get() != '食品酒水') and (food_box.get() != '無 / 不適用'):
                    test_temp = -1
                return test_temp

            def confirm_inex_sort_match_func():
                test_temp = 0
                if radioValue.get() == 0:
                    if sort_box.get() not in in_sort:
                        test_temp = -1
                if radioValue.get() == 1:
                    if sort_box.get() not in out_sort:
                        test_temp = -1
                return test_temp
            
            def confirm_way_func():
                test_temp = 0
                if way_box.get() == '':
                    test_temp = -1
                return test_temp
            
            error = 0 # 檢測各項是否有效。若無效，按確認輸入不會收取值
            error += confirm_date_func()
            error += confirm_amount_func()
            error += confirm_sort_func()
            error += confirm_small_sort_func()
            error += confirm_food_func()
            error += confirm_inex_sort_match_func()
            error += confirm_way_func()
            if error != 0:
                tkinter.messagebox.showinfo('錯誤','有什麼沒寫或寫錯囉！')
            elif error ==0:
                tkinter.messagebox.showinfo('已輸入','已輸入')
            
                in_ex = ''

                if radioValue.get() == 0:
                    in_ex = 'Income'
                elif radioValue.get() == 1:
                    in_ex = 'Expense'
                
                if food_box.get() == '無 / 不適用':
                    food_number = 16
                else:
                    food_number = pure_food_number_list[pure_food_list.index(food_box.get())]

                if month_list.index(month_box.get())+1<10 and int(day_box.get())<10:
                    date_str = year_box.get()+'-0'+str(month_list.index(month_box.get())+1)+'-0'+day_box.get()
                elif month_list.index(month_box.get())+1<10 and int(day_box.get())>=10:
                    date_str = year_box.get()+'-0'+str(month_list.index(month_box.get())+1)+'-'+day_box.get()
                elif month_list.index(month_box.get())+1>=10 and int(day_box.get())<10:
                    date_str = year_box.get()+'-'+str(month_list.index(month_box.get())+1)+'-0'+day_box.get()
                elif month_list.index(month_box.get())+1>=10 and int(day_box.get())>=10:
                    date_str = year_box.get()+'-'+str(month_list.index(month_box.get())+1)+'-'+day_box.get()
                
                way_number = way_number_list[way_list.index(way_box.get())]
                
                if small_sort_box.get() == '收入':
                    small_or_in_sort_number = in_sort_number_list[in_sort.index(sort_box.get())]
                else:
                    small_or_in_sort_number = pure_small_sort_number[pure_small_sort.index(small_sort_box.get())]
     
                r = [in_ex, btw_var.get(), food_number, date_str, int(amount_var.get()),way_number, small_or_in_sort_number]

                store = db.Entry()
                timenow = dt.strptime(dt.now().isoformat(), '%Y-%m-%dT%H:%M:%S.%f')  # YYYY-MM-DD HH:MM:SS.SSS
                in_ex, description, cui_id, ymd, price, method, id = r[0], r[1], r[2], r[3], r[4], r[5], r[6]
                store.add_entry(in_ex, description, cui_id, ymd, price, method, timenow, id)

        # 完成
        space5 = tk.Label(self, text='').pack()
        confirm_everything_button = tk.Button(self, text='確認輸入', font=SMALL_FONT, fg='red', command=confirm_everything_func).pack()

        back = tk.Button(self, text='返回', font=SMALL_FONT, command=lambda: root.show_frame(StartPage)).place(x=40,y=590)


class GoalPage(tk.Frame):
    def __init__(self, parent, root):
        super().__init__(parent)
        label = tk.Label(self, text='設定花費預算', font=LARGE_FONT)
        label.pack(pady=20)
        
        # 輸入月份
        which_month_topic = tk.Label(self, text='*選擇月份（年月)：', font=SMALL_FONT).pack()
        year_box = ttk.Combobox(self)
        year_box['values']=tuple(year_list)
        year_box.pack()
        month_box = ttk.Combobox(self)
        month_box['values'] = tuple(month_list)
        month_box.pack()
        
        # 輸入目標金額
        space7 = tk.Label(self, text='').pack()
        goal_topic = tk.Label(self, text='*本月預定支出預算：', font=SMALL_FONT).pack()
        goal_var = tk.StringVar()
        goal_box = tk.Entry(self, textvariable=goal_var, bd=1).pack()
        
        def confirm_everything_func():
            def confirm_which_month_func():
                test_temp = 0
                if (year_box.get() == '') or (month_box.get() == ''):
                    test_temp = -1
                return test_temp
                
            def confirm_goal_func():
                test_temp = 0
                if (goal_var.get()).isdigit() == False:
                    test_temp = -1
                elif int(goal_var.get()) < 0:
                    test_temp = -1
                return test_temp

            error = 0
            error += confirm_which_month_func()
            error += confirm_goal_func()
            if error != 0:
                tkinter.messagebox.showinfo('錯誤','有什麼沒寫或寫錯囉！')
            else:
                tkinter.messagebox.showinfo('已輸入','已輸入')
                goal_result = [int(year_box.get()), month_list.index(month_box.get())+1, int(goal_var.get())]
                database.update_budget(goal_result[0],goal_result[1],goal_result[2])
        
        space8 = tk.Label(self, text='').pack()
        confirm_everything_button = tk.Button(self,text='確認輸入',font=SMALL_FONT,fg='red',command=confirm_everything_func).pack()

        back = tk.Button(self, text='返回', font=SMALL_FONT, command=lambda: root.show_frame(StartPage)).place(x=40,y=590)


class CheckPage(tk.Frame):
    def __init__(self, parent, root):
        super().__init__(parent)
        label = tk.Label(self, text='檢視收支狀況', font=LARGE_FONT)
        label.pack(pady=20)

        def disable():
            confirm_check_button.configure(state='disabled')
            #confirm_check_button.destroy()

        def enable():
            confirm_check_button.configure(state='normal')

        # 輸入查看月份
        which_month_topic = tk.Label(self, text='開始日期（年月日）：', font=SMALL_FONT).pack()
        
        from_year_box = ttk.Combobox(self)
        from_year_box['values']=tuple(year_list)
        from_year_box.pack()           
        from_month_box = ttk.Combobox(self)
        from_month_box['values'] = tuple(month_list)
        from_month_box.pack()
        from_day_box = ttk.Combobox(self)
        from_day_box['values'] = tuple(day_list)
        from_day_box.pack()

        to_when = tk.Label(self, text='結束日期（年月日）', font=SMALL_FONT).pack()
        to_year_box = ttk.Combobox(self)
        to_year_box['values']=tuple(year_list)
        to_year_box.pack()           
        to_month_box = ttk.Combobox(self)
        to_month_box['values'] = tuple(month_list)
        to_month_box.pack()
        to_day_box = ttk.Combobox(self)
        to_day_box['values'] = tuple(day_list)
        to_day_box.pack()
        
        # 輸入查看類別
        space10 = tk.Label(self, text='').pack()
        from_which_month_topic = tk.Label(self, text='選擇查看類別：', font=SMALL_FONT).pack()
        which_sort_box = ttk.Combobox(self)
        which_sort_box['values']=tuple(sort_for_check)
        which_sort_box.pack()

        def call_record_func():
            test_temp = 0
            def confirm_from_date_func(): 
                test_temp = 0 
                if (from_year_box.get()== '') or (from_month_box.get()=='') or (from_day_box.get()==''):
                    test_temp = -1
                if from_month_box.get() in the_thirties:
                    if from_day_box.get() == '31':
                        test_temp = -1
                elif from_month_box.get() == 'Feb':
                    if (int(from_year_box.get()) == 2100) or (int(from_year_box.get())%4 != 0):
                        if int(from_day_box.get()) > 28:
                            test_temp = -1
                    elif int(from_year_box.get())%4 == 0: 
                        if int(from_day_box.get()) > 29:
                            test_temp = -1
                return test_temp

            def confirm_to_date_func():  
                test_temp = 0 
                if (to_year_box.get()== '') or (to_month_box.get()=='') or (to_day_box.get()==''):
                    test_temp = -1
                if to_month_box.get() in the_thirties:
                    if to_day_box.get() == '31':
                        test_temp = -1
                elif to_month_box.get() == 'Feb':
                    if (int(to_year_box.get()) == 2100) or (int(to_year_box.get())%4 != 0):
                        if int(to_day_box.get()) > 28:
                            test_temp = -1
                    elif int(to_year_box.get())%4 == 0: 
                        if int(to_day_box.get()) > 29:
                            test_temp = -1
                return test_temp

            def confirm_period_func():  # 月份改數字
                test_temp = 0
                if int(from_year_box.get()) > int(to_year_box.get()):
                    test_temp = -1
                elif from_year_box.get() == to_year_box.get():
                    if month_list.index(from_month_box.get()) > month_list.index(to_month_box.get()):
                        test_temp = -1
                    elif from_month_box.get() == to_month_box.get():
                        if int(from_day_box.get()) > int(to_day_box.get()):
                            test_temp = -1
                return test_temp
            
            def confirm_which_sort_func():
                test_temp = 0
                if which_sort_box.get() == '':
                    test_temp = -1
                return test_temp
            
            error = 0 # 檢測各項是否有效。若無效，按確認輸入不會收取值
            error += confirm_from_date_func()
            error += confirm_to_date_func()
            error += confirm_period_func()
            error += confirm_which_sort_func()
            if error != 0:
                tkinter.messagebox.showinfo('錯誤','有什麼沒寫或寫錯囉！')
            else:
                from_month0 = str(month_list.index(from_month_box.get())+1)
                if month_list.index(from_month_box.get())+1 < 10:
                    from_month0 = '0'+str(month_list.index(from_month_box.get())+1)

                from_day0 = from_day_box.get()
                if int(from_day_box.get()) < 10:
                    from_day0 = '0'+from_day_box.get()

                to_month0 = str(month_list.index(to_month_box.get())+1)
                if month_list.index(to_month_box.get())+1 < 10:
                    to_month0 = '0'+str(month_list.index(to_month_box.get())+1)

                to_day0 = to_day_box.get()
                if int(to_day_box.get()) < 10:
                    to_day0 = '0'+to_day_box.get()

                selected_time1 = from_year_box.get()+'-'+from_month0+'-'+from_day0
                selected_time2 = to_year_box.get()+'-'+to_month0+'-'+to_day0
                selected_sort = which_sort_box.get()

                if selected_sort == '全部':
                    result_list = func.all_entry_period(selected_time1, selected_time2)
                    in_sum = func.income_period_sum(selected_time1, selected_time2)
                    ex_sum = func.period_sum(selected_time1, selected_time2)
                    all_sum = tk.Label(self, text='期間收入總額 = '+str(in_sum)+' 元、期間支出總額 = '+str(ex_sum)+' 元', font = SMALL_FONT, fg='Navy')
                    all_sum.pack()
                if selected_sort == '收入':
                    result_list = func.income_entry_period(selected_time1, selected_time2)
                    money_sum = func.income_period_sum(selected_time1, selected_time2)
                    tk.Label(self, text='').pack()
                    all_sum = tk.Label(self, text='      期間總收入：$'+str(money_sum)+'     ', font=MEDIUM_FONT, fg='azure', bg='deep pink')
                    all_sum.pack()
                    tk.Label(self, text='').pack()
                if selected_sort == '支出':
                    result_list = func.expense_entry_period(selected_time1, selected_time2)
                    money_sum = func.period_sum(selected_time1, selected_time2)
                    tk.Label(self, text='').pack()
                    all_sum = tk.Label(self, text='     期間總支出：$'+str(money_sum)+'     ', font=MEDIUM_FONT, fg='azure', bg='deep pink')
                    all_sum.pack()
                    tk.Label(self, text='').pack()
                
                record_list = ttk.Treeview(self)
                record_list['columns'] = ['日期','收/支','金額','類別','子類別','飲食類別','方式','備註']
                record_list.heading('日期', text='日期')
                record_list.heading('收/支', text='收/支')
                record_list.heading('金額', text='金額')
                record_list.heading('類別', text='類別')
                record_list.heading('子類別', text='子類別')
                record_list.heading('飲食類別', text='飲食類別')
                record_list.heading('方式', text='方式')
                record_list.heading('備註', text='備註')
                
                for i in range(len(result_list)):
                    record_list.insert('', i, text=str(i+1), values=tuple(result_list[i]))
                record_list.pack(padx=30)

                def close_record_func():
                    record_list.destroy()
                    all_sum.pack_forget()

                close_record_button = tk.Button(self, text='關閉此筆紀錄', font=SMALLER_FONT,command=lambda:[close_record_func(),enable()])
                close_record_button.place(x=30,y=200)
                if selected_sort == '收入':
                    colors = ['gold', 'yellowgreen', 'lightcoral']
                    in_percent_match = func.MainCat_income_pie(selected_time1, selected_time2, in_sort_number_list)
                    in_percent = []
                    for i in in_percent_match:
                        in_percent += [i[1]]
                    pyplot.rcParams['font.sans-serif'] = ['SimHei']
                    pyplot.pie(in_percent, labels=in_sort_english, colors=colors, autopct = '%1.1f%%', startangle=0)
                    pyplot.title('INCOME')
                    pyplot.show()

                elif selected_sort == '支出':
                    colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue', 'lavender', 'orange', 'Navy', 'yellow']
                    ex_percent_match = func.MainCat_expense_pie(selected_time1, selected_time2, out_sort_number_list)
                    ex_percent = []
                    out_labels = []
                    for i in ex_percent_match:
                        ex_percent += [i[1]]
                        out_labels += [i[0]]
                        
                    pyplot.rcParams['font.sans-serif'] = ['SimHei']
                    pyplot.pie(ex_percent, labels=out_labels, colors=colors, autopct = '%1.1f%%', startangle=0)
                    pyplot.title('EXPENSE')
                    pyplot.show()
        
        confirm_check_button = tk.Button(self, text='確認查詢', font=SMALLER_FONT, command=lambda:[call_record_func(),disable()])
        confirm_check_button.pack()

        back = tk.Button(self, text='返回', font=SMALL_FONT, command=lambda: root.show_frame(StartPage)).place(x=40,y=690)

        
class RewardPage(tk.Frame):
    
    def __init__(self, parent, root):
        super().__init__(parent)
        label = tk.Label(self, text='好好犒賞自己吧！', font=LARGE_FONT)
        label.pack(pady=20)
        
        def call_reward_func():
            if reward_month_box.get()=='' or reward_year_box.get()=='':
                tkinter.messagebox.showinfo('錯誤','有什麼沒寫或寫錯囉！')
            else:
                budget, paid, percentage, overbudget = func.check_budget(int(reward_year_box.get()), month_list.index(reward_month_box.get())+1)
                diff = budget - paid
                
                restaurant_id = func.highest_cuisine()

                recommend = db.Recommendation()
                restaurant = recommend.get_restaurants(restaurant_id)
                
                congrats1 = tk.Label(self, text=f'這個月總花費：${paid} / 設定的預算：${budget}', font=SMALL_FONT, fg='DeepSkyBlue4')
                congrats1.pack()
                congrats6 = tk.Label(self, text=f'花費佔預算的{percentage}', font=MEDIUM_FONT, fg='cyan4')
                congrats6.pack()
                if overbudget == True :
                    congrats2 = tk.Label(self, text='哎呀，超過預算了 '+str(-diff)+' 元', font=CONGRATS_FONT, fg='OrangeRed3')
                    congrats2.pack()
                elif overbudget == False :
                    congrats2 = tk.Label(self, text='還剩 '+str(diff)+' 元', font=LARGE_FONT, fg='PaleGreen4')
                    congrats2.pack()
                    space9 = tk.Label(self, text='')
                    space9.pack()
                    msg = f'根據您的用餐習慣，我們發現你最愛「{out_sort_match[restaurant_id-1][1]}」。\n\n因此我們推薦以下餐廳：\n'
                    recommend = tk.Label(self,text=msg, font=SMALL_FONT, fg='DodgerBlue4')
                    recommend.pack()
                
                    recommend_list = ttk.Treeview(self)
                    recommend_list['columns'] = ('推薦餐廳','評分','價格指數','Google Plus地址')
                    recommend_list.heading('推薦餐廳', text='推薦餐廳')
                    recommend_list.heading('評分', text='評價')
                    recommend_list.heading('價格指數', text='價格')
                    recommend_list.heading('Google Plus地址', text='Google Plus地址')
                    for i in range(len(restaurant)):
                        val = []
                        # '貳房 頂級鍋物', 4.93, 0, '4GP2+XQ 北投區 台北市', '火鍋'
                        s = restaurant[i]
                        p_dict = {0:'無資料', 1:'$', 2:'$$', 3:'$$$', 4:'$$$$'}
                        name, score, price, geo = s[0], round(s[1],2), p_dict[s[2]], s[3]
                        val = [name,score,price,geo]
                        
                        recommend_list.insert('', i, text=f'{i+1}', values=(val))
                    recommend_list.pack(padx=30)
            
                def close_reward_func():
                    congrats1.destroy()
                    congrats2.destroy()
                    congrats6.destroy()
                    if overbudget == False:
                        space9.destroy()
                        recommend.destroy()
                        recommend_list.destroy()

                close_reward_button = tk.Button(self, text='關閉此筆紀錄', font=SMALLER_FONT,command=lambda:[close_reward_func(),enable(call_reward_button)])
                close_reward_button.place(x=40, y=300)
        

        # 選擇月份
        reward = tk.Label(self, text='選擇月份（年月）：', font=SMALL_FONT)
        reward.pack()
        reward_year_box = ttk.Combobox(self)
        reward_year_box['values']=tuple(year_list)
        reward_year_box.pack()           
        reward_month_box = ttk.Combobox(self)
        reward_month_box['values'] = tuple(month_list)
        reward_month_box.pack()
        
        call_reward_button = tk.Button(self, text='恭喜！', font=SMALL_FONT, command=lambda:[call_reward_func(),disable(call_reward_button)])
        call_reward_button.pack()

        def disable(bt):
            bt.config(state='disabled')

        def enable(bt):
            bt.config(state='normal')

        back = tk.Button(self, text='返回', font=SMALL_FONT, command=lambda: root.show_frame(StartPage)).place(x=40,y=590)


app = Application()
app.geometry('800x800')
store = db.Entry()
app.configure(bg='Thistle')
app.mainloop()
