#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
This is the RUBOT Telegram bot by the CL3 group of 2019W Cooperative Systems

First, a few callback functions are defined. Then those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot-user conversation using nested ConversationHandlers.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging

from telegram import (InlineKeyboardMarkup, InlineKeyboardButton)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler, CallbackQueryHandler)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# State definitions for top level conversation
MAIN_MENU, VIEW_ALL_RESOURCES, VIEW_MY_BOOKINGS, SUPPORT = map(chr, range(4))
# State definitions for second level conversation
VIEWING_RESOURCES, VIEWING_BOOKINGS, WRITING_TO_SUPPORT = map(chr, range(4, 7))
# State definitions for descriptions conversation
SELECTING_FEATURE, TYPING = map(chr, range(7, 9))
# Meta states
STOPPING, SHOWING = map(chr, range(9, 11))
# Shortcut for ConversationHandler.END
EXIT = ConversationHandler.END

# Different constants for this example
(B1, PARENTS, CHILDREN, SELF, GENDER, MALE, FEMALE, AGE, NAME, START_OVER, FEATURES,
 CURRENT_FEATURE, CURRENT_LEVEL) = map(chr, range(11, 24))


# Helper
def _name_switcher(level):
    if level == PARENTS:
        return ('Father', 'Mother')
    elif level == CHILDREN:
        return ('Brother', 'Sister')


# Top level conversation callbacks
def start(update, context):
    """Select an action: Adding parent/child or show data."""
    text = 'What would you like to do?'
    buttons = [
        [InlineKeyboardButton(text='View and book resources', callback_data=str(VIEW_ALL_RESOURCES))],
        [InlineKeyboardButton(text='View and modify your bookings', callback_data=str(VIEW_MY_BOOKINGS))],
        [InlineKeyboardButton(text='Send a message to support', callback_data=str(SUPPORT))],
        [InlineKeyboardButton(text='Exit', callback_data=str(EXIT))]
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    # If we're starting over we don't need do send a new message
    if context.user_data.get(START_OVER):
        update.callback_query.edit_message_text(text=text, reply_markup=keyboard)
    else:
        update.message.reply_text('Hello, dear resident! I\'m RUBOT and here to help you book the resources of our community')
        update.message.reply_text(text=text, reply_markup=keyboard)

    context.user_data[START_OVER] = False
    return MAIN_MENU


def view_my_bookings(update, context):
    context.user_data[CURRENT_LEVEL] = SELF
    text = 'Here are your bookings:'
    buttons = [
        [InlineKeyboardButton(text='Booking 1', callback_data=str(B1))],
        [InlineKeyboardButton(text='Back', callback_data=str(MAIN_MENU))]
    ]
    keyboard = InlineKeyboardMarkup.from_button(buttons)

    update.callback_query.edit_message_text(text=text, reply_markup=keyboard)

    return MAIN_MENU


def support(update, context):
    ud = context.user_data
    buttons = [[
        InlineKeyboardButton(text='Back', callback_data=str(MAIN_MENU))
    ]]
    keyboard = InlineKeyboardMarkup(buttons)
    update.callback_query.edit_message_text(text="Please give us your questions or complaints", reply_markup=keyboard)
    ud[START_OVER] = True
    return MAIN_MENU

def stop(update, context):
    """End Conversation by command."""
    update.message.reply_text('Okay, bye.')
    return EXIT

def end(update, context):
    """End conversation from InlineKeyboardButton."""
    update.callback_query.edit_message_text(text='See you around!')
    return EXIT

# Second level conversation callbacks
def select_level(update, context):
    """Choose to add a parent or a child."""
    text = 'You may add a parent or a child. Also you can show the gathered data or go back.'
    buttons = [[
        InlineKeyboardButton(text='Add parent', callback_data=str(PARENTS)),
        InlineKeyboardButton(text='Add child', callback_data=str(CHILDREN))
    ], [
        InlineKeyboardButton(text='Show data', callback_data=str(SHOWING)),
        InlineKeyboardButton(text='Back', callback_data=str(EXIT))
    ]]
    keyboard = InlineKeyboardMarkup(buttons)
    update.callback_query.edit_message_text(text=text, reply_markup=keyboard)

    return VIEWING_RESOURCES


def select_gender(update, context):
    """Choose to add mother or father."""
    level = update.callback_query.data
    context.user_data[CURRENT_LEVEL] = level

    text = 'Please choose, whom to add.'

    male, female = _name_switcher(level)

    buttons = [[
        InlineKeyboardButton(text='Add ' + male, callback_data=str(MALE)),
        InlineKeyboardButton(text='Add ' + female, callback_data=str(FEMALE))
    ], [
        InlineKeyboardButton(text='Show data', callback_data=str(SHOWING)),
        InlineKeyboardButton(text='Back', callback_data=str(EXIT))
    ]]

    keyboard = InlineKeyboardMarkup(buttons)
    update.callback_query.edit_message_text(text=text, reply_markup=keyboard)

    return VIEWING_BOOKINGS


def end_second_level(update, context):
    """Return to top level conversation."""
    context.user_data[START_OVER] = True
    start(update, context)

    return EXIT


# Third level callbacks
def select_feature(update, context):
    """Select a feature to update for the person."""
    buttons = [[
        InlineKeyboardButton(text='Name', callback_data=str(NAME)),
        InlineKeyboardButton(text='Age', callback_data=str(AGE)),
        InlineKeyboardButton(text='Done', callback_data=str(EXIT)),
    ]]
    keyboard = InlineKeyboardMarkup(buttons)

    # If we collect features for a new person, clear the cache and save the gender
    if not context.user_data.get(START_OVER):
        context.user_data[FEATURES] = {GENDER: update.callback_query.data}
        text = 'Please select a feature to update.'
        update.callback_query.edit_message_text(text=text, reply_markup=keyboard)
    # But after we do that, we need to send a new message
    else:
        text = 'Got it! Please select a feature to update.'
        update.message.reply_text(text=text, reply_markup=keyboard)

    context.user_data[START_OVER] = False
    return SELECTING_FEATURE


def ask_for_input(update, context):
    """Prompt user to input data for selected feature."""
    context.user_data[CURRENT_FEATURE] = update.callback_query.data
    text = 'Okay, tell me.'
    update.callback_query.edit_message_text(text=text)

    return TYPING


def save_input(update, context):
    """Save input for feature and return to feature selection."""
    ud = context.user_data
    ud[FEATURES][ud[CURRENT_FEATURE]] = update.message.text

    ud[START_OVER] = True

    return select_feature(update, context)


def end_describing(update, context):
    """End gathering of features and return to parent conversation."""
    ud = context.user_data
    level = ud[CURRENT_LEVEL]
    if not ud.get(level):
        ud[level] = []
    ud[level].append(ud[FEATURES])

    # Print upper level menu
    if level == SELF:
        ud[START_OVER] = True
        start(update, context)
    else:
        select_level(update, context)

    return EXIT


def stop_nested(update, context):
    """Completely end conversation from within nested conversation."""
    update.message.reply_text('Okay, bye.')

    return STOPPING


# Error handler
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

    # Set up third level ConversationHandler (collecting features)
    description_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(select_feature,
                                           pattern='^' + str(MALE) + '$|^' + str(FEMALE) + '$')],

        states={
            SELECTING_FEATURE: [CallbackQueryHandler(ask_for_input,
                                                     pattern='^(?!' + str(EXIT) + ').*$')],
            TYPING: [MessageHandler(Filters.text, save_input)],
        },

        fallbacks=[
            CallbackQueryHandler(end_describing, pattern='^' + str(EXIT) + '$'),
            CommandHandler('stop', stop_nested)
        ],

        map_to_parent={
            # Return to second level menu
            EXIT: VIEWING_RESOURCES,
            # End conversation alltogether
            STOPPING: STOPPING,
        }
    )

    # Set up second level ConversationHandler (adding a person)
    add_member_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(select_level,
                                           pattern='^' + str(VIEW_ALL_RESOURCES) + '$')],

        states={
            VIEWING_RESOURCES: [CallbackQueryHandler(select_gender,
                                                   pattern='^{0}$|^{1}$'.format(str(PARENTS),
                                                                                str(CHILDREN)))],
            VIEWING_BOOKINGS: [description_conv]
        },

        fallbacks=[
            CallbackQueryHandler(support, pattern='^' + str(SUPPORT) + '$'),
            CallbackQueryHandler(end_second_level, pattern='^' + str(EXIT) + '$'),
            CommandHandler('stop', stop_nested)
        ],

        map_to_parent={
            # After showing data return to top level menu
            SHOWING: SHOWING,
            # Return to top level menu
            EXIT: MAIN_MENU,
            # End conversation alltogether
            STOPPING: EXIT,
        }
    )

    # Set up top level ConversationHandler (selecting action)
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            SHOWING: [CallbackQueryHandler(start, pattern='^' + str(EXIT) + '$')],
            MAIN_MENU: [
                add_member_conv,
                CallbackQueryHandler(support, pattern='^' + str(SUPPORT) + '$'),
                CallbackQueryHandler(view_my_bookings, pattern='^' + str(VIEW_MY_BOOKINGS) + '$'),
                CallbackQueryHandler(end, pattern='^' + str(EXIT) + '$'),
            ],
            DESCRIBING_SELF: [description_conv],
        },

        fallbacks=[CommandHandler('stop', stop)],
    )
    # Because the states of the third level conversation map to the ones of the
    # second level conversation, we need to be a bit hacky about that:
    conv_handler.states[VIEWING_BOOKINGS] = conv_handler.states[MAIN_MENU]
    conv_handler.states[STOPPING] = conv_handler.entry_points

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

