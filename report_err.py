#Звіт по даним занесених з помилками

import sqlite3
from datetime import datetime
import re
import webbrowser

def first_symbol_error(input_text):
    if input_text[0].isalpha():
        return False
    else:
        return True

def count_words(input_text):
    return len(re.findall(r"\w\w+", input_text))

def count_packages(input_text):
    if input_text is None or input_text == "":
        return 0
    count = ""
    for s in input_text:
        if s.isdigit():
            count += s
    if count == "":
        return 1
    else:
        return int(count)

def lowercase_error(input_text):
    if (input_text.split()[0][0].isupper()) and (input_text.split()[1][0].isupper()) and (input_text.split()[2][0].isupper()):
        return False
    else:
        return True
    
def count_doublespace(input_text):
    return len(re.findall(r"\s\s+", input_text))   

def find_error(input_text):
    if first_symbol_error(input_text):
        return input_text + " - Попередження @1"
    elif count_words(input_text) != 3:
        return input_text + " - Попередження @2"
    elif count_packages(input_text) > 4:
        return input_text + " - Попередження @3"
    elif lowercase_error(input_text):
        return input_text + " - Попередження @4"
    elif count_doublespace(input_text) != 0:
        return input_text + " - Попередження @5"
    else:
        return ""

def get_report():
    conn = sqlite3.connect("db\\database.sqlite3")
    cur = conn.cursor()    
    cur.execute("SELECT date, time, chat_id, name, recipient FROM recipients ORDER BY recipient ASC;")
    count = 0
    found = False
    answer = "Звіт по даним занесених з помилками\nДані не знайдено\n"
    work = True    
    while work: 
        row = cur.fetchone()
        if row:
            error_str = find_error(row[4])
            if error_str != "":
                if found == False:
                    found = True
                    answer = "Звіт по даним занесених з помилками\n"
                answer += datetime.strptime(row[0], "%Y-%m-%d").strftime("%d-%m-%Y")+" | "+row[1]+" | "+'{:<10}'.format(row[2])+" | "+ '{:<20}'.format(row[3])[:20]+" | "+error_str+"\n"
                count += 1
        else:
            work = False
    cur.close()
    conn.close()
    answer += f"------------\nВсього виявлено {count} помилок"
    return answer

if __name__ == "__main__":
    with open("tmp\\report_err.txt", "w") as file:
        file.write(get_report())
    webbrowser.open("tmp\\report_err.txt")
