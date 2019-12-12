#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
This is the RUBOT Telegram bot by the CL3 group of 2019W Cooperative Systems
"""
import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from typing import Any

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def start(update, context):
    keyboard = [[InlineKeyboardButton("View and book resources", callback_data='1')],
                [InlineKeyboardButton("View and modify your bookings", callback_data='2')],
                [InlineKeyboardButton("Send a message to support", callback_data='3')]],
                #[InlineKeyboardButton("Exit", callback_data='4')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Hello dear resident!  What would you like to do?', reply_markup=reply_markup)


def button(update, context):
    query = update.callback_query

    query.edit_message_text(text="Selected option: {}".format(query.data))
    print(" \nUser ID 1" + str(update.effective_user.id) + " \nUser ID 2" + str(query.from_user.id))
    
    if query.data == '3': 
        query.edit_message_text(text="Please give us your question or complaint")
        

def help(update, context):
    update.message.reply_text("Use /start to test this bot.")


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("916689078:AAFfFObZ4jgmKGmMmjjmAyNgJfVP0X-qa6o", use_context=True)

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_handler(CommandHandler('help', help))
    updater.dispatcher.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()