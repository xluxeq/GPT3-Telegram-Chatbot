from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from datetime import datetime
import json, os, string, sys, threading, logging, time, re, random
import openai

##########
#Settings#
##########
#OpenAI API key
openai.api_key = "OPENAI API KEY"
#Telegram bot key
tgkey = "TELEGRAM BOT KEY"

# Lots of console output
debug = True
# User Session timeout
timstart = 300


#Defaults
user = ""
running = False
cache = None
qcache = None
chat_log = None
start_chat_log = '''Human: Hello, how are you?\n
AI: I am doing great. How can I help you today?\n
'''

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

completion = openai.Completion()

##################
#Command handlers#
##################
def start(bot, update):
    """Send a message when the command /start is issued."""
    global user
    global chat_log
    global qcache
    global cache
    global tim
    if user == "":
        user = update.message.from_user.id
        chat_log = None
        cache = None
        qcache = None
        update.message.reply_text('Send a message!')
        return
    if user == update.message.from_user.id:
        chat_log = None
        cache = None
        qcache = None
        update.message.reply_text('Send a message!')
        return
    else:
        left = str(tim)
        update.message.reply_text('Bot is currently in use, make sure to set your settings when their timer runs down. ' + left + ' seconds.')

def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('/reset resets the conversation, /retry retries the last output.')

def reset(bot, update):
    """Send a message when the command /reset is issued."""
    global user
    global chat_log
    global cache
    global qcache
    global tim
    if user == "":
        user = update.message.from_user.id
        chat_log = None
        cache = None
        qcache = None
        update.message.reply_text('Send a message! Get it computed! GPT-3. I am in the learning chatbot mode.')
        return
    if user == update.message.from_user.id:
        chat_log = None
        cache = None
        qcache = None
        update.message.reply_text('Conversation reset...')
        return
    else:
        left = str(tim)
        update.message.reply_text('Bot is currently in use, make sure to set your settings when their timer runs down. ' + left + ' seconds.')

def retry(bot, update):
    """Send a message when the command /retry is issued."""
    new = True
    comput = threading.Thread(target=wait, args=(bot, update, new,))
    comput.start()

def runn(bot, update):
    """Send a message when a message is received."""
    new = False
    comput = threading.Thread(target=wait, args=(bot, update, new,))
    comput.start()



def wait(bot, update, new):
    global user
    global chat_log
    global cache
    global qcache
    global tim
    global running
    if user == "":
        user = update.message.from_user.id
    if user == update.message.from_user.id:
        user = update.message.from_user.id
        tim = timstart
        compute = threading.Thread(target=interact, args=(bot, update, new,))
        compute.start()
        if running == False:
            while tim > 1:
                running = True
                time.sleep(1)
                tim = tim - 1
            if running == True:
                chatbot = False
                learn = False
                learning = ""
                cache = ""
                user = ""
                update.message.reply_text('Timer has run down, bot has been reset into the default mode.')
                running = False
    else:
        left = str(tim)
        update.message.reply_text('Bot is in use, current cooldown is: ' + left + ' seconds.')

################
#Main functions#
################
def ask(question, chat_log=None):
    if chat_log is None:
        chat_log = start_chat_log
    prompt = f'{chat_log}Human: {question}\nAI:'
    response = completion.create(
        prompt=prompt, engine="davinci", stop=['\n'], temperature=0.9,
        top_p=1, frequency_penalty=7, presence_penalty=0.1, best_of=1,
        max_tokens=150)
    answer = response.choices[0].text.strip()
    return answer

def append_interaction_to_chat_log(question, answer, chat_log=None):
    if chat_log is None:
        chat_log = start_chat_log
    return f'{chat_log}Human: {question}\nAI: {answer}\n'
	
def interact(bot, update, new):
    global chat_log
    global cache
    global qcache
    print("==========START==========")
    tex = update.message.text
    text = str(tex)
    analyzer = SentimentIntensityAnalyzer()
    if new != True:
        vs = analyzer.polarity_scores(text)
        if debug == True:
            print("Sentiment of input:\n")
            print(vs)
        if vs['neg'] > 0:
            update.message.reply_text('Input text is not positive. Input text must be of positive sentiment/emotion.')
            return
    if new == True:
        if debug == True:
            print("Chat_LOG Cache is...")
            print(cache)
            print("Question Cache is...")
            print(qcache)
        chat_log = cache
        question = qcache
    if new != True:
        question = text
        qcache = question
        cache = chat_log
    update.message.reply_text('Computing...')
    try:
        answer = ask(question, chat_log)
        if debug == True:
            print("Input:\n" + question)
            print("Output:\n" + answer)
            print("====================")
        stripes = answer.encode(encoding=sys.stdout.encoding,errors='ignore')
        decoded	= stripes.decode("utf-8")
        out = str(decoded)
        vs = analyzer.polarity_scores(out)
        if debug == True:
            print("Sentiment of output:\n")
            print(vs)
        if vs['neg'] > 0:
            update.message.reply_text('Output text is not positive. Censoring. Use /retry to get positive output.')
            return
        update.message.reply_text(out)
        chat_log = append_interaction_to_chat_log(question, answer, chat_log)
    except Exception as e:
            print(e)
            errstr = str(e)
            update.message.reply_text(errstr)
#####################
# End main functions#
#####################

def error(bot, update):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update)

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(tgkey, use_context=False)
    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("reset", reset))
    dp.add_handler(CommandHandler("retry", retry))
    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, runn))
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
