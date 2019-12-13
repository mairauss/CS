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

import logging, unittest, datetime
from typing import Any, List, Dict
from SQLiteHandler import SQLiteHandler  
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# MAIN is the main menu
# LEVEL1 are the 3 states that we get to from the main menu (viewing resources, etc)
# LEVEL2 are the states that we cat to from LEVEL1 states

(MAIN_MENU, LEVEL1, VIEW_RESOURCES_LEVEL, VIEW_BOOKINGS_LEVEL, SUPPORT_LEVEL, LEVEL3, DATE_SELECTED, TIME_ENTERED, DATE_SELECTED_LATER, 
    DELETE_BOOKING, ERROR)  = range(11)

# These are the names of our session-specific variables (i.e., the indices of the stuff we want to be able to store in context.user_data array
(FIRST_TIME, CURRENT_BOOKING, CURRENT_RESOURCE, DATE, TIME_START, TIME_END) = range(100, 103)

# Main menu options
VIEW_RESOURCES = 'View and book resources'
VIEW_BOOKINGS = 'View and modify your bookings'
SUPPORT = 'Send a message to support'
END = 'End'
# Lower-level menu options
BACK_TO_MAIN = 'Back to main menu'
VIEW_S_D = 'View status and description'
VIEW_SCHEDULE = 'View schedule'
BOOK_R = 'Book this resource'
MODIFY_B = 'Modify'
DELETE_B = 'Delete'
TODAY = 'Today'
TOMORROW = 'Tomorrow'
LATER_DATE = 'Later date'
YES = 'Yes'
NO = 'No'

# This function implements the main menu and gets called every time we get to the top level of our conversation
def main_menu(update, context):
    user = update.message.from_user
    logger.info("User %s is at the main menu, the user name is %s, the user id is %s", user.first_name, user.username, user.id)
    keyboard = [[VIEW_RESOURCES],[VIEW_BOOKINGS],[SUPPORT],[END]]
    greeting = ''
    if context.user_data.get(FIRST_TIME): # If this is the first time we're showing the main menu in this session, greet the user.
        greeting = 'Hello, dear resident! I\'m RUBOT and I\'m here to help you book the resources of our community.\n\n'        
    update.message.reply_text(greeting + 'What would you like to do?', reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True))

# This is the start function.It gets called only once in the beginning of each session.
def start(update, context):
    logger.info('=== RUBOT session started. Using the database %s', SQLiteHandler().pathToDBFile);
    context.user_data[FIRST_TIME] = True
    main_menu(update, context)
    context.user_data[FIRST_TIME] = False
    return LEVEL1

# This function processes the choice made at the main menu
def level1(update, context):
    user = update.message.from_user
    selected = update.message.text
    logger.info("User %s selected option %s", user.first_name, selected)
    if selected == VIEW_RESOURCES:
        resources: List[Dict] = SQLiteHandler().getAllResources()
        reply_keyboard: ReplyKeyboardMarkup = []
        for r in resources:
            reply_keyboard.append([r['name']])
        reply_keyboard.append([BACK_TO_MAIN])
        update.message.reply_text('Please select a resource:', reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return VIEW_RESOURCES_LEVEL
    if selected == VIEW_BOOKINGS:
        bookings: List[Dict] = SQLiteHandler().getResourcesByUserId(user.id)
        reply_keyboard: ReplyKeyboardMarkup = []
        for b in bookings:
            reply_keyboard.append([b['name'] + ' on ' + b['date']])
        reply_keyboard.append([BACK_TO_MAIN])
        update.message.reply_text('Please select a booking: ', reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return VIEW_BOOKINGS_LEVEL
    if selected == SUPPORT:
        update.message.reply_text('Please give us your questions or complaints: ');
        return SUPPORT_LEVEL
    if selected == END:
        update.message.reply_text('Bye!')
        return ConversationHandler.END

    return ERROR

# This function processes the choice of resource made at level1
def view_resources(update, context):
    user = update.message.from_user
    selected = update.message.text
    logger.info("User %s selected option %s", user.first_name, selected)
    if selected == BACK_TO_MAIN:
        main_menu(update, context)
        return LEVEL1
    else:
        reply_keyboard = [[VIEW_S_D], [VIEW_SCHEDULE], [BOOK_R], [BACK_TO_MAIN]]
        update.message.reply_text('What would you like to do with ' + selected + '?', reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        context.user_data[CURRENT_RESOURCE] = selected
        return LEVEL3

# This function processes the choice of booking made at level1
def view_bookings(update, context):
    user = update.message.from_user
    selected = update.message.text
    logger.info("User %s selected option %s", user.first_name, selected)
    if selected == BACK_TO_MAIN:
        main_menu(update, context)
        return LEVEL1
    else:
        reply_keyboard = [[MODIFY_B], [DELETE_B], [BACK_TO_MAIN]]
        update.message.reply_text('Your booking \'' + selected + '\' is for Resource 1 on 31.12 20:00-03:00.\n'
            'What would you like to do with it?', reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        context.user_data[CURRENT_BOOKING] = selected
        return LEVEL3

# This function processes the message to support entered by the user at level1
def support(update, context):
    logger.info("User %s has sent the following message to support: %s", update.message.from_user.first_name, update.message.text)
    update.message.reply_text('Thank you for your message, we will get back to you soon! ' + chr(128235)) 
    main_menu(update, context)
    return LEVEL1

# This function processes the choice of resource made in view_resources, OR the choice of booking made at view_bookings, OR goes back to main menu
def level3(update, context):
    user = update.message.from_user
    selected = update.message.text
    logger.info('User %s selected %s', user.first_name, selected)
    if selected == BACK_TO_MAIN:
        main_menu(update, context)
        return LEVEL1
    elif selected == VIEW_S_D:
        update.message.reply_text('\'' + context.user_data[CURRENT_RESOURCE] + '\' is a washing machine located in the Room 2 in the cellar. It costs €2 per a washload up to 7 kg\n'
                                  'This resource is _operational_.\n'
                                  'Now back to main menu...', parse_mode=ParseMode.MARKDOWN)
        main_menu(update, context)
        return LEVEL1
    elif selected == VIEW_SCHEDULE:
        update.message.reply_text('\'' + context.user_data[CURRENT_RESOURCE] + '\' is booked:\n'
                                  '20.12 15:00-20:00\n21.12 09:00-10:30\n21.12 20:00-22:00\n'
                                  'Now back to main menu...')
        main_menu(update, context)
        return LEVEL1
    elif selected == BOOK_R: #booking
        reply_keyboard = [[TODAY,TOMORROW],[LATER_DATE],[BACK_TO_MAIN]]
        logger.info(CURRENT_BOOKING)
        SQLiteHandler().bookResource(user.id, CURRENT_BOOKING, '20.11.2019')
        logger.info("Booked")
        #update.message.reply_text('Please provide a date:', reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        update.message.reply_text('Booked', reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return DATE_SELECTED
    elif selected == MODIFY_B:
        reply_keyboard = [[TODAY,TOMORROW],[LATER_DATE],[BACK_TO_MAIN]]
        update.message.reply_text('Please provide a date:', reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return DATE_SELECTED
    elif selected == DELETE_B:
        reply_keyboard = [[YES],[NO]]
        update.message.reply_text('Delete booking \'' + context.user_data[CURRENT_BOOKING] + '\'?', reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return DELETE_BOOKING
    
        
# This function processes the result of the 1st step of date selection made at level3
def date_selected(update, context):
    selected = update.message.text
    logger.info("User %s selected the date at the first step.", update.message.from_user.first_name)
    if selected == BACK_TO_MAIN:
        main_menu(update, context)
        return LEVEL1
    elif selected == TODAY:
        date_selected = datetime.date.today()
        context.user_data[DATE] = date_selected
        update.message.reply_text('Please enter the time as *hh:mm* (for example, 09:00 or 22:15):', parse_mode=ParseMode.MARKDOWN)
        return TIME_ENTERED
    elif selected == TOMORROW:
        date_selected = datetime.date.today() + datetime.timedelta(days=1)
        context.user_data[DATE] = date_selected
        update.message.reply_text('Please enter the time as *hh:mm* (for example, 09:00 or 22:15):', parse_mode=ParseMode.MARKDOWN)
        return TIME_ENTERED
    elif selected == LATER_DATE:
        update.message.reply_text('Please enter the date as *dd.mm* (for example, 01.12 or 15.03):', parse_mode=ParseMode.MARKDOWN)
        return DATE_SELECTED_LATER


def time_entered(update, context):
    selected = update.message.text
    logger.info("User %s entered the following time: %s", update.message.from_user.first_name, selected)
    update.message.reply_text('You have entered the following time: ' + selected + '\n' 
                              'From now on our bot is TBD\n'
                              'Now back to main menu...')
    main_menu(update, context)
    return LEVEL1


def date_selected_later(update, context):
    selected = update.message.text
    logger.info("User %s manually entered the following date: %s", update.message.from_user.first_name, selected)
    date_selected = datetime.datetime.strptime(selected, "%d.%m").date()  # probably won't work
    context.user_data[DATE] = date_selected
    update.message.reply_text('You have entered the following date: ' + selected + '\n' 
                              'From now on our bot is TBD\n'
                              'Now back to main menu...')
    main_menu(update, context)
    return LEVEL1

# This function processes the results of "Delete booking?" Yes/No pressed at level3
def delete_booking(update, context):
    selected = update.message.text
    if selected == NO:
        main_menu(update, context)
        return LEVEL1
    if selected == YES:
        logger.info("User %s is deleting booking %s.", update.message.from_user.first_name, context.user_data[CURRENT_BOOKING])
        update.message.reply_text(context.user_data[CURRENT_BOOKING] + ' has been deleted at your request (WELL, NOT YET, THIS IS STILL TBD).\n'
                              'Now back to main menu...');
        main_menu(update, context)
        return LEVEL1

"""def skip_location(update, context):
    user = update.message.from_user
    logger.info("User %s did not send a level3.", user.first_name)
    update.message.reply_text('You seem a bit paranoid! At last, tell me something about yourself.')
    return BIO"""

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
            #MAIN_MENU: [MessageHandler(Filters.update.message, do_nothing)],
            
            LEVEL1: [MessageHandler(Filters.update.message, level1)],

            VIEW_BOOKINGS_LEVEL: [MessageHandler(Filters.update.message, view_bookings)],
            
            VIEW_RESOURCES_LEVEL: [MessageHandler(Filters.update.message, view_resources)],

            LEVEL3: [MessageHandler(Filters.update.message, level3)], #CommandHandler('skip', skip_location)],
        
            SUPPORT_LEVEL: [MessageHandler(Filters.update.message, support)],
            
            DATE_SELECTED: [MessageHandler(Filters.update.message, date_selected)],
            
            TIME_ENTERED: [MessageHandler(Filters.update.message, time_entered)],
            
            DATE_SELECTED_LATER: [MessageHandler(Filters.update.message, date_selected_later)],
            
            DELETE_BOOKING: [MessageHandler(Filters.update.message, delete_booking)],
            
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
