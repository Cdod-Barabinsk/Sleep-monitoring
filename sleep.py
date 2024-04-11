from datetime import datetime
import telebot

bot = telebot.TeleBot('TOKEN')

users_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет! Я буду помогать тебе отслеживать параметры сна. '
                                      'Используй команды /sleep, /wake, /quality и /notes.')

@bot.message_handler(commands=['sleep'])
def sleepin(message):
    chat_id = message.from_user.id
    if chat_id not in users_data:
        users_data[chat_id] = {}
    start_time = datetime.now()
    users_data[chat_id]['start_time'] = start_time
    bot.reply_to(message, "Спокойной ночи! Не забудь сообщить мне, когда проснешься командой /wake.")

@bot.message_handler(commands=['wake'])
def wake(message):
    chat_id = message.from_user.id
    if chat_id in users_data and 'start_time' in users_data[chat_id]:
        time_diff = datetime.now() - users_data[chat_id]['start_time']
        format_time = datetime(1, 1, 1) + time_diff
        wake_time = format_time.strftime("%H:%M")
        users_data[chat_id]['end_time'] = wake_time
        bot.reply_to(message,
                     f'Доброе утро! Твой сон составил около {wake_time} часов. Не забудь оценить качество '
                     f'сна командой /quality и оставить заметки командой /notes.')
    else:
        bot.reply_to(message, 'Извини, я не вижу, что ты сообщил мне о начале сна. Используй команду /sleep.')

@bot.message_handler(commands=['quality'], content_types=["text"])
def quality(message):
    chat_id = message.from_user.id
    if chat_id in users_data:
        quality_value = message.text
        users_data[chat_id]['quality'] = quality_value
        bot.reply_to(message, "Спасибо за оценку качества сна!")
    else:
        bot.reply_to(message, "Начните пожалуйста с команды /sleep, чтобы добавлять оценку сна.")

@bot.message_handler(commands=['notes'], content_types=["text"])
def notes(message):
    chat_id = message.from_user.id
    if chat_id in users_data:
        note_text = message.text
        users_data[chat_id]['notes'] = note_text
        bot.reply_to(message, "Заметка успешно сохранена!")
    else:
        bot.reply_to(message, "Начните пожалуйста с команды /sleep, чтобы добавлять заметки о сне.")

bot.polling(none_stop=True, interval=0)
