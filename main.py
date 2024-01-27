import telebot
import logging
import os
import cups

conn = cups.Connection()
printer = '' # ur printer 
title = ''
print_options = {}


logging.basicConfig(level=logging.INFO)
logging.info(f" Beep-boop")
bot = telebot.TeleBot('') # tg token
allowed_user_id =  [1] # chat IDs
DOWNLOADS_FOLDER = os.path.join(os.path.expanduser('~'), 'Downloads')


@bot.message_handler(commands=['start'])
def handle_start(message):
    '''/start'''
    logging.info(f" [Start message for {message.from_user.id}]")
    if message.from_user.id in allowed_user_id:
        bot.send_message(message.chat.id, """Telegram: printing assistant.

Supported formats: .pdf .jpg .txt and idk

Microsoft(docx,doc) are not supported""")
    else:
        bot.send_message(message.chat.id, "Invalid user")


@bot.message_handler(commands=['print'])
def handle_print(message):
    '''/print'''
    logging.info(f" [Print request from {message.from_user.id}]")
    if message.from_user.id in allowed_user_id:
        bot.send_message(message.chat.id, "Send a file to print.")
        bot.register_next_step_handler(message, process_print_command)
    else:
        bot.send_message(message.chat.id, "Invalid user")


def process_print_command(message):
    '''printing'''
    logging.info(f" [Printing for {message.from_user.id}]")
    if message.content_type == 'document':
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        file_name = message.document.file_name
        save_path = os.path.join(DOWNLOADS_FOLDER, file_name)
        with open(save_path, 'wb') as new_file:
            new_file.write(downloaded_file)
        try:
            to_print = str(save_path)
            conn.printFile(printer, to_print, title, print_options)
            bot.send_message(message.chat.id, f"Printing: {file_name}")
        except Exception as e:
            bot.send_message(message.chat.id, f"Cups doesnt support: {file_name}.\nDetails:\n{e}")
    else:
        handle_print(message)


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    logging.info(f" [Message from: {message.from_user.id}]")
    if message.from_user.id not in allowed_user_id:
        bot.send_message(message.chat.id, "Invalid.")


bot.polling()
