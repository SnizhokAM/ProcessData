# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

from datetime import datetime
import sqlite3
import webbrowser
import tkinter
import tkinter.messagebox as msg
import tkinter.ttk as ttk
import actiondb

def callback_cbx_report(event):
    if (cbx_report.current() == 1) or (cbx_report.current() == 3) or (cbx_report.current() == 5):
        lbl_date.place_forget()
        ent_date.place_forget()
    else:
        lbl_date.place(x=20, y=60)
        ent_date.place(x=20, y=80)
    pgb_apply['value'] = 0

def click_btn_apply():
    pgb_apply['value'] = 0
    if (cbx_report.current() == 0):
        report_date = ent_date.get()
        try:
            testdate = datetime.strptime(report_date, '%d-%m-%Y')
            create_report0(testdate.strftime("%Y-%m-%d"))
        except ValueError:
            msg.showwarning("Помилка", "Невірно введена дата!")     
    elif (cbx_report.current() == 1):
        create_report1()    
    elif (cbx_report.current() == 2):
        report_date = ent_date.get()
        try:
            rd = datetime.strptime(report_date, '%d-%m-%Y')
            create_report2(rd.strftime("%Y-%m-%d"))
        except ValueError:
            msg.showwarning("Помилка", "Невірно введена дата!")     
    elif (cbx_report.current() == 3):
        create_report3()
    elif (cbx_report.current() == 4):
        report_date = ent_date.get()
        try:
            rd = datetime.strptime(report_date, '%d-%m-%Y')
            create_report4(rd.strftime("%Y-%m-%d"))
        except ValueError:
            msg.showwarning("Помилка", "Невірно введена дата!")
    elif (cbx_report.current() == 5):
        create_report5()

def create_report0(report_date):
    answer = actiondb.get_reportday(report_date)
    pgb_apply['value'] = 60
    with open("tmp\\report0.txt", "w") as file:
        file.write(answer)    
    pgb_apply['value'] = 80
    webbrowser.open('tmp\\report0.txt')
    pgb_apply['value'] = 100
    
def create_report1():
    answer = actiondb.get_reporttotal_detail()
    pgb_apply['value'] = 60
    with open("tmp\\report1.txt", "w") as file:
        file.write(answer)    
    pgb_apply['value'] = 80
    webbrowser.open('tmp\\report1.txt')
    pgb_apply['value'] = 100
    
def create_report2(report_date):
    answer = actiondb.get_reportday_full(report_date)
    pgb_apply['value'] = 60
    with open("tmp\\report2.txt", "w") as file:
        file.write(answer)    
    pgb_apply['value'] = 80
    webbrowser.open('tmp\\report2.txt')
    pgb_apply['value'] = 100
    
def create_report3():
    answer = actiondb.get_reporttotal_full()
    pgb_apply['value'] = 60
    with open("tmp\\report3.txt", "w") as file:
        file.write(answer)    
    pgb_apply['value'] = 80
    webbrowser.open('tmp\\report3.txt')
    pgb_apply['value'] = 100
    
def create_report4(report_date):
    answer = actiondb.issued_day(report_date)
    pgb_apply['value'] = 60
    with open("tmp\\report4.txt", "w") as file:
        file.write(answer)    
    pgb_apply['value'] = 80
    webbrowser.open('tmp\\report4.txt')
    pgb_apply['value'] = 100
    
def create_report5():
    answer = actiondb.issued_total()
    pgb_apply['value'] = 60
    with open("tmp\\report5.txt", "w") as file:
        file.write(answer)    
    pgb_apply['value'] = 80    
    webbrowser.open('tmp\\report5.txt')
    pgb_apply['value'] = 100

if __name__=="__main__":
    main_form = tkinter.Tk()
    main_form.title("Формування звіту")
    main_form.geometry("282x186")
    main_form.resizable(width=False, height=False)
    main_form.iconbitmap("report.ico")
    lbl_report = tkinter.Label(text="Тип звіту:")
    lbl_report.place(x=20, y=10)
    cbx_report = ttk.Combobox(main_form, values=["Звіт по отримувачах на дату", "Кількість отримувачів всього", "Звіт по отримувачах на дату (детально)", "Кількість отримувачів всього (детально)", "Видано пакетів за день", "Видано пакетів усього"],
                              state="readonly", width=37)
    cbx_report.place(x=20, y=30)
    cbx_report.current(0)
    cbx_report.bind("<<ComboboxSelected>>", callback_cbx_report)
    lbl_date = tkinter.Label(text="Дата в форматі ДД-ММ-РРРР:")
    lbl_date.place(x=20, y=60)
    report_date = tkinter.StringVar()
    ent_date = tkinter.Entry(textvariable=report_date, width="40")
    nowtime = datetime.now()
    ent_date.insert(0, nowtime.strftime("%d-%m-%Y"))
    ent_date.place(x=20, y=80)
    pgb_apply = ttk.Progressbar(main_form, length=245)
    pgb_apply.place(x=20, y=110)
    btn_apply = tkinter.Button(text="Виконати", height="1", width="15", command=click_btn_apply)
    btn_apply.place(x=20, y=144)
    btn_exit = tkinter.Button(text="Вихід", height="1", width="15", command=main_form.destroy)
    btn_exit.place(x=150, y=144)
    main_form.mainloop()
