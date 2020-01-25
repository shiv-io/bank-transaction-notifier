import telegram
import config

bot = telegram.Bot(token=config.BOT_TOKEN)

def push_msg(msg):
    bot.send_message(chat_id=config.CHAT_ID, text=msg)

push_msg('hello')