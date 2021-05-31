from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from datetime import datetime
import json, os, string, sys, threading, logging, time, re, random
import openai

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


#OpenAI API key
openai.api_key = "OPENAI API KEY"
#Telegram bot key
tgkey = "TELEGRAM BOT KEY"

# Lots of console output
debug = True
# User Session timeout
timstart = 1500

#Learning context (optional)
learning = ""
# End settings

#Defaults
chatbot = True
learn = True
user = ""
cache = ""
running = False

##################
#Command handlers#
##################
def start(bot, update):
    """Send a message when the command /start is issued."""
    global running
    global chatbot
    global learn
    global user
    global tim
    global learning
    global cache
    if user == "":
        user = update.message.from_user.id
        chatbot = True
        learn = True
        learning = ""
        cache = ""
        if chatbot == True and learn == True:
            update.message.reply_text('Send a message! Get it computed! GPT-3. I am in the learning chatbot mode.')
        if chatbot == True and learn == False:
            update.message.reply_text('Send a message! Get it computed! GPT-3 I am in the chatbot mode.')
        if chatbot == False:
            update.message.reply_text('Send a message! Get it computed! GPT-3 I am in the finishsentence mode.')
        return
    if user == update.message.from_user.id:
        chatbot = True
        learn = True
        learning = ""
        cache = ""
        if chatbot == True and learn == True:
            update.message.reply_text('Send a message! Get it computed! GPT-3. I am in the learning chatbot mode.')
        if chatbot == True and learn == False:
            update.message.reply_text('Send a message! Get it computed! GPT-3 I am in the chatbot mode.')
        if chatbot == False:
            update.message.reply_text('Send a message! Get it computed! GPT-3 I am in the finishsentence mode.')
        return
    else:
        left = str(tim)
        update.message.reply_text('Bot is currently in use, make sure to set your settings when their timer runs down. ' + left + ' seconds.')

def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Just type a message... It could be lagged out. /chatbot goes into Me: You: mode. /finish just finishes the text /learnon for conversation learning mode.')

def chat(bot, update):
    """Send a message when the command /chatbot is issued."""
    global running
    global chatbot
    global learn
    global user
    global tim
    global learning
    global cache
    if user == "":
        user = update.message.from_user.id
        chatbot = True
        learn = False
        learning = ""
        cache = ""
        if chatbot == True and learn == True:
            update.message.reply_text('Send a message! Get it computed! GPT-3. I am in the learning chatbot mode.')
        if chatbot == True and learn == False:
            update.message.reply_text('Send a message! Get it computed! GPT-3 I am in the chatbot mode.')
        if chatbot == False:
            update.message.reply_text('Send a message! Get it computed! GPT-3 I am in the finishsentence mode.')
        return
    if user == update.message.from_user.id:
        chatbot = True
        learn = False
        learning = ""
        cache = ""
        if chatbot == True and learn == True:
            update.message.reply_text('Send a message! Get it computed! GPT-3. I am in the learning chatbot mode.')
        if chatbot == True and learn == False:
            update.message.reply_text('Send a message! Get it computed! GPT-3 I am in the chatbot mode.')
        if chatbot == False:
            update.message.reply_text('Send a message! Get it computed! GPT-3 I am in the finishsentence mode.')
        return
    else:
        left = str(tim)
        update.message.reply_text('Bot is currently in use, make sure to set your settings when their timer runs down. ' + left + ' seconds.')

def finish(bot, update):
    """Send a message when the command /finish is issued."""
    global running
    global chatbot
    global learn
    global user
    global tim
    global learning
    global cache
    if user == "":
        user = update.message.from_user.id
        chatbot = False
        learn = False
        learning = ""
        cache = ""
        if chatbot == True and learn == True:
            update.message.reply_text('Send a message! Get it computed! GPT-3. I am in the learning chatbot mode.')
        if chatbot == True and learn == False:
            update.message.reply_text('Send a message! Get it computed! GPT-3 I am in the chatbot mode.')
        if chatbot == False:
            update.message.reply_text('Send a message! Get it computed! GPT-3 I am in the finishsentence mode.')
        return
    if user == update.message.from_user.id:
        chatbot = False
        learn = False
        learning = ""
        cache = ""
        if chatbot == True and learn == True:
            update.message.reply_text('Send a message! Get it computed! GPT-3. I am in the learning chatbot mode.')
        if chatbot == True and learn == False:
            update.message.reply_text('Send a message! Get it computed! GPT-3 I am in the chatbot mode.')
        if chatbot == False:
            update.message.reply_text('Send a message! Get it computed! GPT-3 I am in the finishsentence mode.')
        return
    else:
        left = str(tim)
        update.message.reply_text('Bot is currently in use, make sure to set your settings when their timer runs down. ' + left + ' seconds.')

def learnon(bot, update):
    """Send a message when the command /learnon is issued."""
    global running
    global chatbot
    global learn
    global user
    global tim
    global learning
    global cache
    if user == "":
        user = update.message.from_user.id
        chatbot = True
        learn = True
        learning = ""
        cache = ""
        if chatbot == True and learn == True:
            update.message.reply_text('Send a message! Get it computed! GPT-3. I am in the learning chatbot mode.')
        if chatbot == True and learn == False:
            update.message.reply_text('Send a message! Get it computed! GPT-3 I am in the chatbot mode.')
        if chatbot == False:
            update.message.reply_text('Send a message! Get it computed! GPT-3 I am in the finishsentence mode.')
        return
    if user == update.message.from_user.id:
        chatbot = True
        learn = True
        learning = ""
        cache = ""
        if chatbot == True and learn == True:
            update.message.reply_text('Send a message! Get it computed! GPT-3. I am in the learning chatbot mode.')
        if chatbot == True and learn == False:
            update.message.reply_text('Send a message! Get it computed! GPT-3 I am in the chatbot mode.')
        if chatbot == False:
            update.message.reply_text('Send a message! Get it computed! GPT-3 I am in the finishsentence mode.')
        return
    else:
        left = str(tim)
        update.message.reply_text('Bot is currently in use, make sure to set your settings when their timer runs down. ' + left + ' seconds.')

def learnoff(bot, update):
    """Send a message when the command /learnoff is issued."""
    global running
    global chatbot
    global learn
    global user
    global tim
    global learning
    global cache
    if user == "":
        user = update.message.from_user.id
        chatbot = True
        learn = False
        learning = ""
        cache = ""
        if chatbot == True and learn == True:
            update.message.reply_text('Send a message! Get it computed! GPT-3. I am in the learning chatbot mode.')
        if chatbot == True and learn == False:
            update.message.reply_text('Send a message! Get it computed! GPT-3 I am in the chatbot mode.')
        if chatbot == False:
            update.message.reply_text('Send a message! Get it computed! GPT-3 I am in the finishsentence mode.')
        return
    if user == update.message.from_user.id:
        chatbot = True
        learn = False
        learning = ""
        cache = ""
        if chatbot == True and learn == True:
            update.message.reply_text('Send a message! Get it computed! GPT-3. I am in the learning chatbot mode.')
        if chatbot == True and learn == False:
            update.message.reply_text('Send a message! Get it computed! GPT-3 I am in the chatbot mode.')
        if chatbot == False:
            update.message.reply_text('Send a message! Get it computed! GPT-3 I am in the finishsentence mode.')
        return
    else:
        left = str(tim)
        update.message.reply_text('Bot is currently in use, make sure to set your settings when their timer runs down. ' + left + ' seconds.')

def learnreset(bot, update):
    """Send a message when the command /learnreset is issued."""
    global running
    global chatbot
    global learn
    global user
    global tim
    global learning
    global cache
    if user == "":
        user = update.message.from_user.id
        chatbot = True
        learn = True
        learning = ""
        cache = ""
        if chatbot == True and learn == True:
            update.message.reply_text('Send a message! Get it computed! GPT-3. I am in the learning chatbot mode.')
        if chatbot == True and learn == False:
            update.message.reply_text('Send a message! Get it computed! GPT-3 I am in the chatbot mode.')
        if chatbot == False:
            update.message.reply_text('Send a message! Get it computed! GPT-3 I am in the finishsentence mode.')
        return
    if user == update.message.from_user.id:
        chatbot = True
        learn = True
        learning = ""
        cache = ""
        if chatbot == True and learn == True:
            update.message.reply_text('Send a message! Get it computed! GPT-3. I am in the learning chatbot mode.')
        if chatbot == True and learn == False:
            update.message.reply_text('Send a message! Get it computed! GPT-3 I am in the chatbot mode.')
        if chatbot == False:
            update.message.reply_text('Send a message! Get it computed! GPT-3 I am in the finishsentence mode.')
        return
    else:
        left = str(tim)
        update.message.reply_text('Bot is currently in use, make sure to set your settings when their timer runs down. ' + left + ' seconds.')

def retry(bot, update):
    new = True
    comput = threading.Thread(target=wait, args=(bot, update, new,))
    comput.start()

def runn(bot, update):
    new = False
    comput = threading.Thread(target=wait, args=(bot, update, new,))
    comput.start()

def wait(bot, update, new):
    global tim
    global user
    global running
    global chatbot
    global learn
    global learning
    global cache
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

########START MAIN HANDLER########
def interact(bot, update, new):
    global learning
    global learn
    global chatbot
    global cache
    tex = update.message.text
    text = str(tex)
    analyzer = SentimentIntensityAnalyzer()
    if new != True:
        # Input sentiment analysis
        vs = analyzer.polarity_scores(text)
        print(vs['neg'])
        if vs['neg'] > 1:
            update.message.reply_text('Input text is not positive. Censoring.')
            return
    if chatbot == True:
        textlength = len(text.split())
        #Retry cached text and process length
        if new == True and cache:
            user = update.message.from_user
            name = str(user['username'])
            if ' AM' in cache:
                m = re.search('.* AM', cache)
            else:
                raw_text = cache
                raw_text = m.group(0)
            if ' PM' in cache:
                m = re.search('.* PM', cache)
                raw_text = m.group(0)
            else:
                raw_text = cache
            if debug == True:
                print("Cache is...")
                print(raw_text)
        #Run on new text and process length
        if new != True:
            user = update.message.from_user
            name = str(user['username'])
            begin = name + ' — Today at '
            now = datetime.now()
            clock = now.strftime('%I:%M %p')
            joined = begin + clock + "\n"
            userin = joined + text + "\n\n"
            userout = userin + 'user2 — Today at ' + clock + "\n"
            initial = userout
            raw_text = learning + initial
            cache = initial
    ####Text Completion Mode####
    if chatbot == False:
        textlength = len(text.split())
        length = textlength
        if length > 300:
            update.message.reply_text('Input text is too long.')
            return
        if new != True:
            cache = text
        if new == True and cache:
            text = cache
            if debug == True:
                print("Cache is...")
                print(text)
        raw_text = text
#############################################
    update.message.reply_text('Computing...')
    try:
        response = openai.Completion.create(engine="davinci", prompt=raw_text, max_tokens=64, temperature=1, top_p=0.7)
        text = response['choices'][0]['text']
        if debug == True:
            print("Raw output:\n" + text)
            print("====================")
        stripes = text.encode(encoding=sys.stdout.encoding,errors='ignore')
        tigger = stripes.decode("utf-8")
        mew = str(tigger)
        string = mew.splitlines()[0]
        ##Chatbot text filter.##
        if chatbot == True:
            data = " ".join(re.split("[^a-zA-Z.,?!'*]+", string))
            if name in data:
                m = re.search(name, data)
                data = m.group(0)  
        else:
            data = string
        if learn == True:
            learning = raw_text + data + "\n\n"
        vs = analyzer.polarity_scores(data)
        print(vs['neg'])
        if vs['neg'] > 1:
            update.message.reply_text('Output text is not positive. Censoring.')
            return
        update.message.reply_text(data)
        if debug == True:
            mod = str(chatbot)
            print("chatbot: " + mod)
            lear = str(learn)
            print("Learn: " + lear)
            print("====================")
            print("Raw_text or Original:\n" + raw_text)
            print("====================")
            print("Learning text or Next:\n" + learning)
            print("==========END==========")
    except Exception as e:
            print(e)
            errstr = str(e)
            update.message.reply_text(errstr)
########END MAIN HANDLER########

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
    dp.add_handler(CommandHandler("chatbot", chat))
    dp.add_handler(CommandHandler("finish", finish))
    dp.add_handler(CommandHandler("learnon", learnon))
    dp.add_handler(CommandHandler("learnoff", learnoff))
    dp.add_handler(CommandHandler("learnreset", learnreset))
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
