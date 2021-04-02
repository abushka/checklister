import datetime
import threading
import logging
from typing import Any, Dict, List

from django.utils.timezone import now

# Telegram imports
import telegram

# Local imports
from tgbot.handlers import static_text
from tgbot.models import User

log = logging.getLogger('User menu')


def receiver(update, context):
    if update.callback_query is not None:
        update.callback_query.answer()
    if update.message.text in context.user_data['menu'][1]:
        pressed = update.message.text
        next_menu = context.user_data['menu'][1].get(update.message.text)
        possibles = globals().copy()
        possibles.update(locals())
        method = possibles.get(next_menu)
        if not method:
            raise NotImplementedError("Method %s not implemented" % next_menu)
        if context.user_data['menu'][2] is not None:
            context.bot.delete_message(update.message.chat.id, context.user_data['menu'][2])
            context.user_data['menu'][2] = None
        method(update, context)


def main_menu(update, context):
    context.user_data['menu'] = ['Main menu', {'Some menu': 'some_menu'}, None]
    buttons = [[telegram.KeyboardButton('Some menu')]]
    reply_markup = telegram.ReplyKeyboardMarkup(buttons, resize_keyboard=True)

    user = User.get_user(update, context)
    message = context.bot.send_message(update.message.chat.id, f'Hello, {user.first_name}!\n'
                                                               f'You opened the main menu.', reply_markup=reply_markup)
    context.user_data['menu'][2] = message.message_id


def some_menu(update, context):
    context.user_data['menu'] = ['Some menu', {'Go back': 'main_menu'}, None]
    buttons = [[telegram.KeyboardButton('Go back')]]
    reply_markup = telegram.ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    message = context.bot.send_message(update.message.chat.id, 'Some menu', reply_markup=reply_markup)
    context.user_data['menu'][2] = message.message_id

