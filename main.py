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

from telegram import ParseMode, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from datetime import datetime
import time
import config as cfg
import backup as bkp
import actiondb

def on_start(update, context):
    nowtime = datetime.now()
    chat = update.effective_chat
    message = cfg.greeting1+". "+cfg.greeting2+" "+cfg.organization+". Команди бота:\nПІБ (3-5 букв) - пошук;\n+ПІБ - додати одержувача;\n?ПІБ - про одержувача;\n*дд-мм-рррр - звіт на дату;\n* - звіт за сьогодні;\n&дд-мм-рррр - звіт на дату (всі);\n& - звіт за сьогодні (всі);\n! - крайні 5 доданих;\n# - всього видано;\n/id - показати userID;\n/backup - виконати резервне копіювання;\n/info - довідка."
    context.bot.send_message(chat_id=chat.id, text=message)
    print(nowtime.strftime("%d-%m-%Y %H:%M"), 'ID='+str(chat.id)+" "+get_name(chat.last_name, chat.first_name)+" Розпочато чат")

def on_id(update, context):
    nowtime = datetime.now()
    chat = update.effective_chat
    message = "Ваш userID: "+str(chat.id)
    context.bot.send_message(chat_id=chat.id, text=message)
    print(nowtime.strftime("%d-%m-%Y %H:%M"), 'ID='+str(chat.id)+" "+get_name(chat.last_name, chat.first_name)+" Запит userID")

def on_backup(update, context):
    nowtime = datetime.now()
    chat = update.effective_chat
    if chat.id not in cfg.admins:
        context.bot.send_message(chat_id=chat.id, text="В доступі відмовлено")
        print(nowtime.strftime("%d-%m-%Y %H:%M"), 'ID='+str(chat.id)+" <- В доступі відмовлено")
        return
    if bkp.make_backup():
        context.bot.send_message(chat_id=chat.id, text="Резервну копію створено")
        print(nowtime.strftime("%d-%m-%Y %H:%M"), 'ID='+str(chat.id)+" <- Резервну копію створено")
    else:
        context.bot.send_message(chat_id=chat.id, text="Помилка створення резервної копії")
        print(nowtime.strftime("%d-%m-%Y %H:%M"), 'ID='+str(chat.id)+" <- Помилка створення резервної копії")

def on_info(update, context):
    nowtime = datetime.now()
    chat = update.effective_chat
    message = cfg.info
    context.bot.send_message(chat_id=chat.id, text=message)
    print(nowtime.strftime("%d-%m-%Y %H:%M"), 'ID='+str(chat.id)+" "+get_name(chat.last_name, chat.first_name)+" Запит info")

def on_message(update, context):
    nowtime = datetime.now()
    chat = update.effective_chat
    text = update.message.text.strip()
    text = text.replace("'", "")
    print(nowtime.strftime("%d-%m-%Y %H:%M"), 'ID='+str(chat.id)+" -> "+text)
    if chat.id not in cfg.users:
        context.bot.send_message(chat_id=chat.id, text="В доступі відмовлено")
        print(nowtime.strftime("%d-%m-%Y %H:%M"), 'ID='+str(chat.id)+" <- В доступі відмовлено")
        return    
    if len(text)>0: 
        if text[0] == "+":
            pib = text[1:].strip()
            if len(pib) > 5:
                if (actiondb.add_recipient(nowtime, chat.id, get_name(chat.last_name, chat.first_name), pib)):
                    context.bot.send_message(chat_id=chat.id, text="Дані додано до бази даних")
                    print(nowtime.strftime("%d-%m-%Y %H:%M"), 'ID='+str(chat.id)+" <- Дані додано до бази даних")
                else:
                    context.bot.send_message(chat_id=chat.id, text="Помилка відкриття бази даних")
                    print(nowtime.strftime("%d-%m-%Y %H:%M"), 'ID='+str(chat.id)+" <- Помилка відкриття бази даних")
            else:
                context.bot.send_message(chat_id=chat.id, text="Помилковий запит")
                print(nowtime.strftime("%d-%m-%Y %H:%M"), 'ID='+str(chat.id)+" <- Помилковий запит")
        elif text[0] == "*":
            if len(text.strip()) > 1:
                report_date = text[1:].strip()
            else:
                report_date = nowtime.strftime("%d-%m-%Y")
            try:
                testdate = datetime.strptime(report_date, '%d-%m-%Y')
                report_date = testdate.strftime("%Y-%m-%d")
                answer = actiondb.get_reportday_user(report_date, chat.id)
                with open("tmp\\report.txt", "w") as file:
                    file.write(answer)
                context.bot.send_document(chat_id=chat.id, document=open('tmp\\report.txt', 'rb'))
                context.bot.send_message(chat_id=chat.id, text="Звіт надіслано")    
                print(nowtime.strftime("%d-%m-%Y %H:%M"), 'ID='+str(chat.id)+" <- Створено та надіслано звіт")
            except ValueError:
                context.bot.send_message(chat_id=chat.id, text="Помилковий запит")
                print(nowtime.strftime("%d-%m-%Y %H:%M"), 'ID='+str(chat.id)+" <- Звіт не створено")                
        elif text[0] == "&":
            if len(text.strip()) > 1:
                report_date = text[1:].strip()
            else:
                report_date = nowtime.strftime("%d-%m-%Y")
            try:
                testdate = datetime.strptime(report_date, '%d-%m-%Y')
                report_date = testdate.strftime("%Y-%m-%d")
                answer = actiondb.get_reportday(report_date)                
                with open("tmp\\report.txt", "w") as file:
                    file.write(answer)
                context.bot.send_document(chat_id=chat.id, document=open('tmp\\report.txt', 'rb'))
                context.bot.send_message(chat_id=chat.id, text="Звіт надіслано")    
                print(nowtime.strftime("%d-%m-%Y %H:%M"), 'ID='+str(chat.id)+" <- Створено та надіслано звіт")
            except ValueError:
                context.bot.send_message(chat_id=chat.id, text="Помилковий запит")
                print(nowtime.strftime("%d-%m-%Y %H:%M"), 'ID='+str(chat.id)+" <- Звіт не створено")
        elif text[0] == "!":
            answer = actiondb.get_5last(chat.id)
            context.bot.send_message(chat_id=chat.id, text=answer)
            print(nowtime.strftime("%d-%m-%Y %H:%M"), 'ID='+str(chat.id)+" <- Сформовано вибірку")            
        elif text[0] == "#":
            answer = actiondb.issued_total()
            context.bot.send_message(chat_id=chat.id, text=answer)
            print(nowtime.strftime("%d-%m-%Y %H:%M"), 'ID='+str(chat.id)+" <- Створено звіт")
        elif text[0] == "?":
            pib = text[1:].strip()
            if len(pib) > 0:
                answer = actiondb.find_full(pib)
                context.bot.send_message(chat_id=chat.id, text=answer)
                print(nowtime.strftime("%d-%m-%Y %H:%M"), 'ID='+str(chat.id)+" <- Сформовано вибірку")
            else:
                context.bot.send_message(chat_id=chat.id, text="Помилковий запит")
                print(nowtime.strftime("%d-%m-%Y %H:%M"), 'ID='+str(chat.id)+" <- Помилковий запит")
        else:
            answer = actiondb.find_pib(text)
            context.bot.send_message(chat_id=chat.id, text=answer)
            print(nowtime.strftime("%d-%m-%Y %H:%M"), 'ID='+str(chat.id)+" <- Сформовано вибірку")

def get_name(last_name, first_name):
    try:
        return str(last_name)+" "+str(first_name)
    except:
        return "Unknown name" 

if __name__ == "__main__":
    updater = Updater(cfg.token, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", on_start))
    dp.add_handler(CommandHandler("id", on_id))
    dp.add_handler(CommandHandler("backup", on_backup))    
    dp.add_handler(CommandHandler("info", on_info))
    dp.add_handler(MessageHandler(Filters.text & (~Filters.command), on_message))
    print("Telegram бота для "+cfg.organization+" запущено, для завершення роботи натисніть Ctrl+C")
    updater.start_polling()
    updater.idle()
