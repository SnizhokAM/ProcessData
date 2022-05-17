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

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import time
import datetime
import config as cfg

def on_message(update, context):
    nowtime = datetime.datetime.now()
    chat = update.effective_chat
    text = update.message.text.strip()
    print(nowtime.strftime("%d-%m-%Y %H:%M"), 'ID='+str(chat.id)+" -> "+text)
    context.bot.send_message(chat_id=chat.id, text="Сервіс тимчасово не працює")
    print(nowtime.strftime("%d-%m-%Y %H:%M"), 'ID='+str(chat.id)+" -> Надіслано повідомлення")

if __name__ == "__main__":
    updater = Updater(cfg.token, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text & (~Filters.command), on_message))
    print("Telegram бота 'Сервіс тимчасово не працює' запущено, для завершення роботи натисніть Ctrl+C")
    updater.start_polling()
    updater.idle()
