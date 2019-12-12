#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
This is the RUBOT Telegram bot by the CL3 group of 2019W Cooperative Systems

First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# MAIN is the main menu
# LEVEL1 are the 3 states that we get to from the main menu (viewing resources, etc)
# LEVEL2 are the states that we cat to from LEVEL1 states

START, LEVEL1, VIEW_RESOURCES_LEVEL, VIEW_BOOKINGS_LEVEL, SUPPORT_LEVEL, LEVEL3, BIO, ERROR = range(8)

VIEW_RESOURCES = 'View and book resources'
VIEW_BOOKINGS = 'View and modify your bookings'
SUPPORT = 'Send a message to support'
END = 'End'
BACK_TO_MAIN = 'Back to main menu'

def start(update, context):
    logger.info("User %s is at the main menu", update.message.from_user.first_name);
    reply_keyboard = [[VIEW_RESOURCES], [VIEW_BOOKINGS], [SUPPORT], [END]]

    update.message.reply_text(
        'Hello, dear resident! I\'m RUBOT and here to help you book the resources of our community.\n\n'
        'What would you like to do?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return LEVEL1


def level1(update, context):
    user = update.message.from_user
    selected = update.message.text
    logger.info("User %s selected option %s", user.first_name, selected)
    if selected == VIEW_RESOURCES:
        reply_keyboard = [['Resource 1'], ['Resource 2'], [BACK_TO_MAIN]]
        update.message.reply_text('Please select a resource:', reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return VIEW_RESOURCES_LEVEL
    if selected == VIEW_BOOKINGS:
        reply_keyboard = [['Booking 1'], ['Booking 2'], [BACK_TO_MAIN]]
        update.message.reply_text('Please select a booking: ', reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return VIEW_BOOKINGS_LEVEL
    if selected == SUPPORT:
        update.message.reply_text('Please give us your questions or complaints: ');
        return SUPPORT_LEVEL
    if selected == END:
        update.message.reply_text('Bye!')
        return ConversationHandler.END

    return ERROR


def view_resources(update, context):
    user = update.message.from_user
    selected = update.message.text
    logger.info("User %s selected option %s", user.first_name, selected)
    update.message.reply_text('We are now at the View Resources level')
    if selected == BACK_TO_MAIN:
        return START

    return LEVEL3

def view_bookings(update, context):
    user = update.message.from_user
    selected = update.message.text
    logger.info("User %s selected option %s", user.first_name, selected)
    update.message.reply_text('We are at the View Bookings level')
    if selected == BACK_TO_MAIN:
        return START

    return LEVEL3

def support(update, context):
    user = update.message.from_user
    selected = update.message.text
    logger.info("User %s selected option %s", user.first_name, selected)
    update.message.reply_text('We are now at the Support level')
    if selected == BACK_TO_MAIN:
        return START

    return LEVEL3


def level3(update, context):
    user = update.message.from_user
    text = update.message.text
    logger.info('User %s said ', user.first_name, text)
    update.message.reply_text('Thank you! You said ' + text)

    return BIO


"""def skip_location(update, context):
    user = update.message.from_user
    logger.info("User %s did not send a level3.", user.first_name)
    update.message.reply_text('You seem a bit paranoid! At last, tell me something about yourself.')
    return BIO"""


def bio(update, context):
    user = update.message.from_user
    logger.info("User %s said %s", user.first_name, update.message.text)
    update.message.reply_text('Thank you! You said ' + update.message.text)

    return START


def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.', reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("916689078:AAFfFObZ4jgmKGmMmjjmAyNgJfVP0X-qa6o", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LEVEL3 and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            START: [MessageHandler(Filters.update.message, start)],
            
            LEVEL1: [MessageHandler(Filters.update.message, level1)],

            VIEW_BOOKINGS_LEVEL: [MessageHandler(Filters.update.message, view_bookings)],
            
            VIEW_RESOURCES_LEVEL: [MessageHandler(Filters.update.message, view_resources)],

            LEVEL3: [MessageHandler(Filters.update.message, level3)], #CommandHandler('skip', skip_location)],

            BIO: [MessageHandler(Filters.text, bio)],
            
            ERROR: [MessageHandler(Filters.update.message, error)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
