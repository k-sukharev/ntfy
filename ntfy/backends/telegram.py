import os

import telebot
from telebot import apihelper


def notify(title, message, retcode=None):
    token = os.environ.get('NTFY_TELEGRAM_TOKEN')
    chat_id = os.environ.get('NTFY_TELEGRAM_CHAT_ID')
    proxy = os.environ.get('NTFY_SOCKS_PROXY')

    if not token or not chat_id:
        raise ValueError(
            'Set NTFY_TELEGRAM_TOKEN and NTFY_TELEGRAM_CHAT_ID '
            'environment variables.'
        )

    if proxy:
        apihelper.proxy = {'https': proxy}

    bot = telebot.TeleBot(token)
    bot.send_message(chat_id, message)
