import logging
from collections import defaultdict
from typing import Dict

import telegram

# Local imports
from tgbot import localization
from tgbot.models import User, Category, Product, Text

log = logging.getLogger('User menu')
loc = localization.Localization(
    language='ru',
    fallback='ru'
)


def receiver(update, context):
    if update.callback_query is not None:
        update.callback_query.answer()

    if len(context.user_data) == 0:
        context.user_data[0] = {'current_menu': loc.get('button_main_menu'),
                                'current_kb': {loc.get('button_some_menu'): 'some_menu'},
                                'last_msg_id': None}

    if update.message.text in context.user_data[0]['current_kb']:
        pressed = update.message.text
        next_menu = context.user_data[0]['current_kb'].get(update.message.text)
        possibles = globals().copy()
        possibles.update(locals())
        method = possibles.get(next_menu)
        if not method:
            raise NotImplementedError("Method %s not implemented" % next_menu)
        if context.user_data[0]['last_msg_id'] is not None:
            context.bot.delete_message(update.message.chat.id, context.user_data[0]['last_msg_id'])
            context.user_data[0]['last_msg_id'] = None
        method(update, context)


def main_menu(update, context):
    context.user_data[0] = {'current_menu': loc.get('button_main_menu'),
                            'current_kb': {
                                loc.get('button_settings_menu'): 'settings_menu',
                                loc.get('button_products_menu'): 'products_menu'
                            },
                            'last_msg_id': None}
    buttons = [[telegram.KeyboardButton(loc.get('button_products_menu'))],
               [telegram.KeyboardButton(loc.get('button_settings_menu'))]]
    reply_markup = telegram.ReplyKeyboardMarkup(buttons, resize_keyboard=True)

    user = User.get_user(update, context)
    message = context.bot.send_message(update.message.chat.id, loc.get('conv_opened_main_menu',
                                                                       first_name=user.first_name),
                                       reply_markup=reply_markup)
    context.user_data[0]['last_msg_id'] = message.message_id


def products_menu(update, context):
    buttons = []
    user = User.get_user(update, context)
    categories = Category.objects.all()
    names = Text.objects.all()
    for name in names:
        print(name.item)
    for category in categories:
        print(category.name)
    #     buttons.append([telegram.KeyboardButton(category.name.filter(lang='ru'))])
    # message = context.bot.send_message(update.message.chat.id, 'test',
    #                                    reply_markup=telegram.ReplyKeyboardMarkup(buttons,
    #                                                                              resize_keyboard=True))
    # context.user_data[0] = {
    #     'current_menu': loc.get('button_products_menu'),
    #     'current_kb': {
    #         loc.get()
    #     }
    # }


def settings_menu(update, context):
    context.user_data[0] = {'current_menu': loc.get('button_settings_menu'),
                            'current_kb': {
                                loc.get('button_back'): 'main_menu',
                                loc.get('button_lang_settings_menu'): 'lang_settings_menu',
                                loc.get('button_name_settings_menu'): 'name_settings_menu'
                            },
                            'last_msg_id': None}
    buttons = [[telegram.KeyboardButton(loc.get('button_back'))],
               [telegram.KeyboardButton(loc.get('button_lang_settings_menu')),
                telegram.KeyboardButton(loc.get('button_name_settings_menu'))]]
    reply_markup = telegram.ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    user = User.get_user(update, context)
    message = context.bot.send_message(user.user_id, loc.get('conv_settings_menu'),
                                       reply_markup=reply_markup)
    context.user_data[0]['last_msg_id'] = message.message_id
