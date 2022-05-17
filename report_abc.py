#Звіт відсортований за алфавітом

import sqlite3
from datetime import datetime
import webbrowser

def get_count(input_text):
    if input_text is None or input_text == "":
        return 0
    count = ""
    for s in input_text:
        if s.isdigit():
            count += s
    if count == "":
        return 1
    if int(count)>6:
        return 1
    else:
        return int(count)

def get_report():
    conn = sqlite3.connect("db\\database.sqlite3")
    cur = conn.cursor()    
    cur.execute("SELECT date, time, chat_id, name, recipient FROM recipients ORDER BY recipient ASC;")
    count_r = 0
    count_p = 0
    found = False
    answer = "Звіт відсортований за алфавітом\nДані не знайдено\n"
    work = True    
    while work: 
        row = cur.fetchone()
        if row:
            if found == False:
                found = True
                answer = "Звіт відсортований за алфавітом\n"
            answer += datetime.strptime(row[0], "%Y-%m-%d").strftime("%d-%m-%Y")+" | "+row[1]+" | "+'{:<10}'.format(row[2])+" | "+ '{:<20}'.format(row[3])[:20]+" | "+row[4]+"\n"
            count_r += 1
            count_p += get_count(row[4])
        else:
            work = False
    cur.close()
    conn.close()
    answer += f"------------\nВидано {count_p} пакетів {count_r} отримувачам"
    return answer

if __name__ == "__main__":
    with open("tmp\\report_abc.txt", "w") as file:
        file.write(get_report())
    webbrowser.open("tmp\\report_abc.txt")
