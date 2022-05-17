import sqlite3
from datetime import datetime

def add_recipient(nowtime, chat_id, name, pib):
    try:
        conn = sqlite3.connect("db\\database.sqlite3")
        cur = conn.cursor()
        cur.execute("INSERT INTO recipients(date, time, chat_id, name, recipient) VALUES(DATE('"+nowtime.strftime("%Y-%m-%d")+"'), '"+nowtime.strftime("%H:%M")+"', '"+str(chat_id)+"', '"+name+"', '"+pib+"');")
        conn.commit()
        cur.close()
        conn.close()
        return True
    except sqlite3.Error as error:
        if (conn):
            conn.close()
        return False    

def get_count(input_text):
    if input_text is None or input_text == "":
        return 0
    count = ""
    for s in input_text:
        if s.isdigit():
            count += s
    if count == "":
        return 1
    if int(count)>8:
        return 1
    else:
        return int(count)

def find_full(pib):
    conn = sqlite3.connect("db\\database.sqlite3")
    cur = conn.cursor()
    cur.execute("SELECT recipient, date, name FROM recipients WHERE recipient LIKE '"+pib+"%';")
    found = False
    answer = "Дані не знайдено"
    work = True    
    while work: 
        row = cur.fetchone()
        if row:
            if found == False:
                found = True
                answer = ""
            else:
                answer += "\n"
            answer += row[0]+" створено "+datetime.strptime(row[1], "%Y-%m-%d").strftime("%d-%m-%Y")+" "+row[2]
        else:
            work = False
    cur.close()
    conn.close()
    return answer

def find_pib(pib):
    conn = sqlite3.connect("db\\database.sqlite3")
    cur = conn.cursor()
    cur.execute("SELECT recipient FROM recipients WHERE recipient LIKE '"+pib+"%';")
    found = False
    answer = "Дані не знайдено"
    work = True    
    while work: 
        row = cur.fetchone()
        if row:
            if found == False:
                found = True
                answer = ""
            else:
                answer += "\n"
            answer += row[0]
        else:
            work = False
    cur.close()
    conn.close()
    return answer    

def get_5last(chat_id):
    conn = sqlite3.connect("db\\database.sqlite3")
    cur = conn.cursor()
    cur.execute("SELECT time, recipient FROM recipients WHERE chat_id = '"+str(chat_id)+"' ORDER BY id DESC LIMIT 5;")
    found = False
    answer = "Дані не знайдено"
    work = True    
    while work: 
        row = cur.fetchone()
        if row:
            if found == False:
                found = True
                answer = ""
            else:
                answer += "\n"
            answer += row[0]+" | "+row[1]
        else:
            work = False
    cur.close()
    conn.close()
    return answer

def get_reporttotal():
    conn = sqlite3.connect("db\\database.sqlite3")
    cur = conn.cursor()
    cur.execute("SELECT recipient FROM recipients;")
    count = 0
    work = True    
    while work: 
        row = cur.fetchone()
        if row:
            count += 1
        else:
            work = False
    cur.close()
    conn.close()
    answer = "Всього: "+str(count)+" отримувачів" 
    return answer

def get_reporttotal_detail():
    conn = sqlite3.connect("db\\database.sqlite3")
    cur = conn.cursor()
    cur.execute("SELECT date, time, recipient FROM recipients;")
    count_r = 0
    count_p = 0
    found = False
    answer = "Звіт по отримувачах\nДані не знайдено\n"
    work = True    
    while work: 
        row = cur.fetchone()
        if row:
            if found == False:
                found = True
                answer = "Звіт по отримувачах\n"
            answer += datetime.strptime(row[0], "%Y-%m-%d").strftime("%d-%m-%Y")+" | "+row[1]+" | "+row[2]+"\n"
            count_r += 1
            count_p += get_count(row[2])
        else:
            work = False
    cur.close()
    conn.close()
    answer += "------------\nВидано "+str(count_p)+" пакетів "+str(count_r)+" отримувачам"
    return answer

def get_userslist_total():
    conn = sqlite3.connect("db\\database.sqlite3")
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT chat_id FROM recipients;")
    userslist = list()
    work = True    
    while work: 
        row = cur.fetchone()
        if row:
            userslist.append(row[0])
        else:
            work = False
    cur.close()
    conn.close()
    return userslist

def get_reporttotal_full():
    count_all_r = 0
    count_all_p = 0
    answer = "Детальний звіт по отримувачах"
    userslist = get_userslist_total()
    for user in userslist:
        answer += "\n"+"Ідентифікатор користувача: "+user+"\n"
        conn = sqlite3.connect("db\\database.sqlite3")
        cur = conn.cursor()
        cur.execute("SELECT date, time, recipient FROM recipients WHERE chat_id = '"+user+"';")
        count_r = 0
        count_p = 0   
        work = True    
        while work: 
            row = cur.fetchone()
            if row:
                answer += row[0]+" | "+row[1]+" | "+str(get_count(row[2]))+" | "+row[2]+"\n"
                count_r += 1
                count_p += get_count(row[2])
                count_all_r += 1
                count_all_p += get_count(row[2])
            else:
                work = False
        cur.close()
        conn.close()
        answer += "------------\nВидано "+str(count_p)+" пакетів "+str(count_r)+" отримувачам\n"
    if count_all_r != 0:
        answer += "------------\nВсього видано "+str(count_all_p)+" пакетів "+str(count_all_r)+" отримувачам"
    else:
        answer += "\n------------\nВсього видано "+str(count_all_p)+" пакетів "+str(count_all_r)+" отримувачам"
    return answer

def get_reportday(report_date):
    conn = sqlite3.connect("db\\database.sqlite3")
    cur = conn.cursor()
    cur.execute("SELECT time, recipient FROM recipients WHERE date = DATE('"+report_date+"');")
    count_r = 0
    count_p = 0
    found = False
    answer = "Звіт по отримувачах за "+datetime.strptime(report_date, "%Y-%m-%d").strftime("%d-%m-%Y")+"\nДані не знайдено\n"
    work = True    
    while work: 
        row = cur.fetchone()
        if row:
            if found == False:
                found = True
                answer = "Звіт по отримувачах за "+datetime.strptime(report_date, "%Y-%m-%d").strftime("%d-%m-%Y")+"\n"
            answer += row[0]+" | "+row[1]+"\n"
            count_r += 1
            count_p += get_count(row[1])
        else:
            work = False
    cur.close()
    conn.close()
    answer += "------------\nВидано "+str(count_p)+" пакетів "+str(count_r)+" отримувачам"
    return answer

def get_reportday_user(report_date, chat_id):
    conn = sqlite3.connect("db\\database.sqlite3")
    cur = conn.cursor()
    cur.execute("SELECT time, recipient FROM recipients WHERE date = DATE('"+report_date+"') AND chat_id = '"+str(chat_id)+"';")
    count_r = 0
    count_p = 0
    found = False
    answer = "Звіт по отримувачах за "+datetime.strptime(report_date, "%Y-%m-%d").strftime("%d-%m-%Y")+"\nДані не знайдено\n"
    work = True    
    while work: 
        row = cur.fetchone()
        if row:
            if found == False:
                found = True
                answer = "Звіт по отримувачах за "+datetime.strptime(report_date, "%Y-%m-%d").strftime("%d-%m-%Y")+"\n"
            answer += row[0]+" | "+row[1]+"\n"
            count_r += 1
            count_p += get_count(row[1])
        else:
            work = False
    cur.close()
    conn.close()
    answer += "------------\nВидано "+str(count_p)+" пакетів "+str(count_r)+" отримувачам"
    return answer

def get_userslist_day(report_date):
    conn = sqlite3.connect("db\\database.sqlite3")
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT chat_id FROM recipients WHERE date = DATE('"+report_date+"');")
    userslist = []
    work = True    
    while work: 
        row = cur.fetchone()
        if row:
            userslist.append(row[0])
        else:
            work = False
    cur.close()
    conn.close()
    return userslist

def get_reportday_full(report_date):
    count_all_r = 0
    count_all_p = 0
    answer = "Детальний звіт по отримувачах за "+datetime.strptime(report_date, "%Y-%m-%d").strftime("%d-%m-%Y")
    userslist = get_userslist_day(report_date)
    for user in userslist:
        answer += "\n"+"Ідентифікатор користувача: "+user+"\n"
        conn = sqlite3.connect("db\\database.sqlite3")
        cur = conn.cursor()
        cur.execute("SELECT time, recipient FROM recipients WHERE date = DATE('"+report_date+"') AND chat_id = '"+user+"';")
        count_r = 0
        count_p = 0   
        work = True    
        while work: 
            row = cur.fetchone()
            if row:
                answer += row[0]+" | "+str(get_count(row[1]))+" | "+row[1]+"\n"
                count_r += 1
                count_p += get_count(row[1])
                count_all_r += 1
                count_all_p += get_count(row[1])
            else:
                work = False
        cur.close()
        conn.close()
        answer += "------------\nВидано "+str(count_p)+" пакетів "+str(count_r)+" отримувачам\n"
    if count_all_r != 0:
        answer += "------------\nВсього видано "+str(count_all_p)+" пакетів "+str(count_all_r)+" отримувачам\n"
    else:
        answer += "\n------------\nВсього видано "+str(count_all_p)+" пакетів "+str(count_all_r)+" отримувачам\n"
    return answer

def issued_total():
    conn = sqlite3.connect("db\\database.sqlite3")
    cur = conn.cursor()
    cur.execute("SELECT recipient FROM recipients;")
    count_r = 0
    count_p = 0
    work = True    
    while work: 
        row = cur.fetchone()
        if row:
            count_r += 1
            count_p += get_count(row[0])
        else:
            work = False
    cur.close()
    conn.close()
    answer = "Видано "+str(count_p)+" пакетів "+str(count_r)+" отримувачам" 
    return answer

def issued_day(report_date):
    conn = sqlite3.connect("db\\database.sqlite3")
    cur = conn.cursor()
    cur.execute("SELECT recipient FROM recipients WHERE date = DATE('"+report_date+"');")
    count_r = 0
    count_p = 0
    work = True    
    while work: 
        row = cur.fetchone()
        if row:
            count_r += 1
            count_p += get_count(row[0])
        else:
            work = False
    cur.close()
    conn.close()
    answer = "За "+datetime.strptime(report_date, "%Y-%m-%d").strftime("%d-%m-%Y")+" видано "+str(count_p)+" пакетів "+str(count_r)+" отримувачам"
    return answer

if __name__ == "__main__":
    print("**Тест для get_count:\n"+str(get_count("Петров Іван Сидорович (3)")))
    print("**Тест для find_full:\n"+find_full("Іва"))
    print("**Тест для find_pib:\n"+find_pib("Іва"))
    print("**Тест для get_5last:\n"+get_5last(570673186))
    print("**Тест для get_reporttotal:\n"+get_reporttotal())
    print("**Тест для get_reporttotal_detail:\n"+get_reporttotal_detail())
    print("**Тест для get_userslist_total:")
    print(get_userslist_total())
    print("**Тест для get_reporttotal_full:\n"+get_reporttotal_full())    
    print("**Тест для get_reportday:\n"+get_reportday(datetime.now().strftime("%Y-%m-%d")))
    print("**Тест для get_reportday_user:\n"+get_reportday_user(datetime.now().strftime("%Y-%m-%d"), 5292748580))    
    print("**Тест для get_userslist_day:")
    print(get_userslist_day(datetime.now().strftime("%Y-%m-%d")))
    print("**Тест для get_reportday_full:\n"+get_reportday_full(datetime.now().strftime("%Y-%m-%d")))
    print("**Тест для issued_total:\n"+issued_total())
    print("**Тест для issued_day:\n"+issued_day(datetime.now().strftime("%Y-%m-%d")))
