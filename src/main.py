#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.
#from _overlapped import NULL

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
from Handlers.SQLiteHandler import SQLiteHandler  
from Handlers.WeatherApiHandler import WeatherApiHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# MAIN is the main menu
# LEVEL1 are the 3 states that we get to from the main menu (viewing resources, etc)
# LEVEL2 are the states that we cat to from LEVEL1 states

(MAIN_MENU, LEVEL1, VIEW_RESOURCES_LEVEL, VIEW_BOOKINGS_LEVEL, SUPPORT_LEVEL, LEVEL3, DATE_SELECTED, TIME_ENTERED, DATE_SELECTED_LATER, 
    DELETE_BOOKING, MODIFY_BOOKING, TIME_MODIFIED, DATE_SELECTED_LATER_MODIFIED, ERROR)  = range(14)

# These are the names of our session-specific variables (i.e., the indices of the stuff we want to be able to store in context.user_data array
(FIRST_TIME, CURRENT_BOOKING, CURRENT_RESOURCE, DATE, TIME_START, TIME_END) = range(100, 106)

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

allResources = {}
yourResources = {}
timeSlots: List[str] = ["9:00-11:00", "11:00-13:00", "13:00-15:00", "15:00-17:00", "17:00-19:00", "19:00-21:00"]
    
def composeWeatherForecast (booking_date : datetime.date) -> str:
    api: WeatherApiHandler = WeatherApiHandler()
    weather: Dict = api.get_weather_by_date(booking_date.day, booking_date.month, booking_date.year)
    return ('The weather forecast for the date of your reservation is: _between ' 
            + str(weather['minimum']) + '°C and ' + str(weather['maximum']) + '°C, ' + str(weather['dayMessage']) + ' during the day, ' 
            + str(weather['nightMessage']) + ' at night._') if weather else ''
    

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
    logger.info('RUBOT session started.');
    context.user_data[FIRST_TIME] = True

    resources: List[Dict] = SQLiteHandler().get_all_Resources()
    for r in resources:
        allResources[r['name']] = r['id']

    main_menu(update, context)
    context.user_data[FIRST_TIME] = False
    return LEVEL1

# This function processes the choice made at the main menu
def level1(update, context):
    user = update.message.from_user
    selected = update.message.text
    logger.info("User %s selected option %s", user.first_name, selected)
    if selected == VIEW_RESOURCES:
        resources: List[Dict] = SQLiteHandler().get_all_Resources()
        reply_keyboard: ReplyKeyboardMarkup = []
        for r in resources:
            reply_keyboard.append([r['name']])

        reply_keyboard.append([BACK_TO_MAIN])
        update.message.reply_text('Please select a resource:', reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return VIEW_RESOURCES_LEVEL
    if selected == VIEW_BOOKINGS:
        bookings: List[Dict] = SQLiteHandler().get_resources_by_user_id(user.id)
        reply_keyboard: ReplyKeyboardMarkup = []
        yourResources.clear()
        if len(bookings) > 0 and (type(bookings) == list):
            for b in bookings:
                reply_keyboard.append([b['name'] + ' on ' + b['date'] + ', ' + b['time']])
                shownBooking = b['name'] + ' on ' + b['date'] + ', ' + b['time']
                yourResources[shownBooking] = b['reservationId']

            reply_keyboard.append([BACK_TO_MAIN])

            update.message.reply_text('Please select a booking: ', reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            return VIEW_BOOKINGS_LEVEL
        else:
            update.message.reply_text('You have no reservations.')
            main_menu(update, context)
            return LEVEL1
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
        update.message.reply_text('Your booking ' + selected + '\n' +
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
        resId = allResources[context.user_data[CURRENT_RESOURCE]]
        update.message.reply_text('Description of \'' + context.user_data[
            CURRENT_RESOURCE] + '\': ' + SQLiteHandler().get_resource_description(resId), parse_mode=ParseMode.MARKDOWN)
        main_menu(update, context)
        return LEVEL1
    elif selected == VIEW_SCHEDULE:
        resId = allResources[context.user_data[CURRENT_RESOURCE]]
        resourceSchedule: List[Dict] = SQLiteHandler().get_resource_schedule(resId)
        strTimes = ""
        for rs in resourceSchedule:
            strTimes += str(rs['date']) + ", " + str(rs['time']) + '\n'

        update.message.reply_text('\'' + context.user_data[CURRENT_RESOURCE] + '\' is booked:\n' + strTimes +
                                  '\n' + 'Now back to main menu...')
        main_menu(update, context)
        return LEVEL1
    elif selected == BOOK_R:
        reply_keyboard = [[TODAY,TOMORROW],[LATER_DATE],[BACK_TO_MAIN]]
        update.message.reply_text('Please provide a date:', reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return DATE_SELECTED
    elif selected == MODIFY_B:
        reply_keyboard = [[TODAY,TOMORROW],[LATER_DATE],[BACK_TO_MAIN]]
        update.message.reply_text('Please provide a date:', reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        #return DATE_SELECTED #should be modify
        return MODIFY_BOOKING
    elif selected == DELETE_B:
        reply_keyboard = [[YES],[NO]]
        update.message.reply_text('Delete booking \'' + context.user_data[CURRENT_BOOKING] + '\'?', reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return DELETE_BOOKING


def build_timeslot_keyboard(date: str) -> ReplyKeyboardMarkup:
    bookedTimeSlots: List[str] = SQLiteHandler().get_booked_time_slots(date)
    reply_keyboard: ReplyKeyboardMarkup = []
    for timeSlot in timeSlots:
        if timeSlot not in bookedTimeSlots:
            reply_keyboard.append([timeSlot])
    reply_keyboard.append([BACK_TO_MAIN])
    return reply_keyboard

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
        update.message.reply_text('Please select time slot: ',
                                  reply_markup=ReplyKeyboardMarkup(build_timeslot_keyboard(date_selected), one_time_keyboard=True))
        return TIME_ENTERED
    elif selected == TOMORROW:
        date_selected = datetime.date.today() + datetime.timedelta(days=1)
        context.user_data[DATE] = date_selected
        update.message.reply_text('Please select time slot: ',
                                  reply_markup=ReplyKeyboardMarkup(build_timeslot_keyboard(date_selected), one_time_keyboard=True))
        return TIME_ENTERED
    elif selected == LATER_DATE:
        update.message.reply_text('Please enter the date as *dd.mm* (for example, 01.12 or 15.03):', parse_mode=ParseMode.MARKDOWN)
        return DATE_SELECTED_LATER


def time_entered(update, context):
    user = update.message.from_user
    logger.info(context.user_data[DATE])
    selected = update.message.text

    if selected == BACK_TO_MAIN:
        main_menu(update, context)
        return LEVEL1

    if selected not in timeSlots:
        update.message.reply_text("Wrong input!", parse_mode=ParseMode.MARKDOWN)
        main_menu(update, context)
        return LEVEL1


    logger.info("User %s entered the following time: %s", update.message.from_user.first_name, selected)

	# NTLK Example: https://medium.com/analytics-vidhya/building-a-simple-chatbot-in-python-using-nltk-7c8c8215ac6e
	# General approach: Preprocess input (Special Characters/Delimiters, Tokenize), compare with synonyms
	# Check if time input format is valid 
	#   false: "Bad Format"
	#     a) Did u mean ...?
	#     b) Try again
	#   true: as before (book, msg, main menu, return LEVEL1)
    if selected == "1234":
        update.message.reply_text('Your time input could not be processed' + selected + '\n' + 'Try again..')
        return TIME_ENTERED
    #    
    
    resId = allResources[context.user_data[CURRENT_RESOURCE]]
    isBooked: bool = SQLiteHandler().book_resource(user.id, resId, context.user_data[DATE], selected)
    if isBooked:
        update.message.reply_text('Your reservation made for *' + context.user_data[DATE].strftime('%A, %B %d') + ', ' + selected + '* was successfully saved!',
                              parse_mode=ParseMode.MARKDOWN)
        forecast = composeWeatherForecast(context.user_data[DATE])
        if forecast > '' :
            update.message.reply_text(forecast, parse_mode=ParseMode.MARKDOWN)
    else:
        update.message.reply_text("The resource has already been booked for that time", parse_mode=ParseMode.MARKDOWN)

    main_menu(update, context)
    return LEVEL1


def date_selected_later(update, context):
    selected = update.message.text
    now = datetime.datetime.now()
    selected += "." + str(now.year)
    logger.info("User %s manually entered the following date: %s", update.message.from_user.first_name, selected)
    date_selected = datetime.datetime.strptime(selected, "%d.%m.%Y").date()  # probably won't work
    context.user_data[DATE] = date_selected
    logger.info(date_selected)
    update.message.reply_text('Please select time slot: ',
                              reply_markup=ReplyKeyboardMarkup(build_timeslot_keyboard(date_selected), one_time_keyboard=True))
    #main_menu(update, context)
    #return LEVEL1
    return TIME_ENTERED

def time_entered_modified(update, context):
    user = update.message.from_user
    logger.info(context.user_data[DATE])
    selected = update.message.text

    if selected == BACK_TO_MAIN:
        main_menu(update, context)
        return LEVEL1

    if selected not in timeSlots:
        update.message.reply_text("Wrong input!", parse_mode=ParseMode.MARKDOWN)
        main_menu(update, context)
        return LEVEL1

    logger.info("User %s entered the following time: %s", update.message.from_user.first_name, selected)
    reservationId = yourResources[context.user_data[CURRENT_BOOKING]]
    SQLiteHandler().modify_reservation(user.id, reservationId, context.user_data[DATE], selected)
    update.message.reply_text('Your reservation was successfully modified! The new date is *' + context.user_data[DATE].strftime('%A, %B %d') + '*, the new time is *' + selected + '*',
                              parse_mode=ParseMode.MARKDOWN)
    forecast = composeWeatherForecast(context.user_data[DATE])
    if forecast > '' :
        update.message.reply_text(forecast, parse_mode=ParseMode.MARKDOWN)
    main_menu(update, context)
    return LEVEL1


def date_selected_later_modified(update, context):
    selected = update.message.text
    now = datetime.datetime.now()
    selected += "." + str(now.year)
    logger.info("User %s manually entered the following date: %s", update.message.from_user.first_name, selected)
    date_selected = datetime.datetime.strptime(selected, "%d.%m.%Y").date()  # probably won't work
    context.user_data[DATE] = date_selected
    logger.info(date_selected)
    update.message.reply_text('Please select time slot: ',
                              reply_markup=ReplyKeyboardMarkup(build_timeslot_keyboard(date_selected), one_time_keyboard=True))

    return TIME_MODIFIED

# This function processes the results of "Delete booking?" Yes/No pressed at level3
def delete_booking(update, context):
    selected = update.message.text
    if selected == NO:
        main_menu(update, context)
        return LEVEL1
    if selected == YES:
        user = update.message.from_user
        logger.info("User %s is deleting booking %s.", update.message.from_user.first_name, context.user_data[CURRENT_BOOKING])
        reservationId = yourResources[context.user_data[CURRENT_BOOKING]]
        SQLiteHandler().delete_reservation(user.id, reservationId)
        update.message.reply_text(context.user_data[CURRENT_BOOKING] + ' has been deleted. \n' +
                              'Now back to main menu...');
        main_menu(update, context)
        return LEVEL1


# This function processes the results of "Modify booking" pressed at level3
def modify_booking(update, context):
    selected = update.message.text
    logger.info("User %s selected the date at the first step.", update.message.from_user.first_name)
    if selected == BACK_TO_MAIN:
        main_menu(update, context)
        return LEVEL1
    elif selected == TODAY:
        date_selected = datetime.date.today()
        context.user_data[DATE] = date_selected
        update.message.reply_text('Please select time slot: ',
                                  reply_markup=ReplyKeyboardMarkup(build_timeslot_keyboard(date_selected), one_time_keyboard=True))
        return TIME_MODIFIED
    elif selected == TOMORROW:
        date_selected = datetime.date.today() + datetime.timedelta(days=1)
        context.user_data[DATE] = date_selected
        update.message.reply_text('Please select time slot: ',
                                  reply_markup=ReplyKeyboardMarkup(build_timeslot_keyboard(date_selected), one_time_keyboard=True))
        return TIME_MODIFIED
    elif selected == LATER_DATE:
        update.message.reply_text('Please enter the date as *dd.mm* (for example, 01.12 or 15.03):',
                                  parse_mode=ParseMode.MARKDOWN)
        return DATE_SELECTED_LATER_MODIFIED


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
    update.message.reply_text("Wrong input!", parse_mode=ParseMode.MARKDOWN)
    logger.warning('Update "%s" caused error "%s"', update, context.error)
    return LEVEL1


def main():
    logger.info('======= RUBOT server started. Using the database %s =======', SQLiteHandler().pathToDBFile);
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    # Maira 1012496423:AAENENi8eLcMoqd4zrFW95qQ_7YHuY9dwF8
    # updater = Updater("916689078:AAFfFObZ4jgmKGmMmjjmAyNgJfVP0X-qa6o", use_context=True)
    updater = Updater("1012496423:AAENENi8eLcMoqd4zrFW95qQ_7YHuY9dwF8", use_context=True)
    #updater = Updater("866551704:AAHAe01RPGg4caLlEGs3GkbpTK1eF-szyAs", use_context=True)


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

            MODIFY_BOOKING: [MessageHandler(Filters.update.message, modify_booking)],

            TIME_MODIFIED: [MessageHandler(Filters.update.message, time_entered_modified)],

            DATE_SELECTED_LATER_MODIFIED: [MessageHandler(Filters.update.message, date_selected_later_modified)],

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
