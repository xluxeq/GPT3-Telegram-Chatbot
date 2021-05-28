from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import json, os, string, sys, threading, logging, time, re
import openai
import nltk

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
# Model thinking per word 0.66 or 0.77 work well. 
top = 0.7
# Temperature (refer to gpt-2 documentation)
temp = 1
# top_p multiplier - add to top_p per word, these were originally for gpt-2 bot
# 0.00375‬ - may be shorter
# 0.00400
# 0.00425
# 0.00450
# 0.00475
# 0.00500 - may be longer
mx = 0.00375
# This is the start of the learning context.
learning = ""
# End settings

#Download vader_lexicon if it's not already downloaded.
nltk.download('vader_lexicon')

#Defaults
chatbot = True
learn = True
user = ""
cache = ""
running = False
temps = str(temp)
tpstring = str(top)

# Command handlers
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
            update.message.reply_text('Send a message! Get it computed! Settings: Logic: ' + tpstring + ' Rate:' + temps + ' GPT-3. I am in the learning chatbot mode.')
        if chatbot == True and learn == False:
            update.message.reply_text('Send a message! Get it computed! Settings: Logic: ' + tpstring + ' Rate:' + temps + ' GPT-3 I am in the chatbot mode.')
        if chatbot == False:
            update.message.reply_text('Send a message! Get it computed! Settings: Logic: ' + tpstring + ' Rate:' + temps + ' GPT-3 I am in the finishsentence mode.')
        return
    if user == update.message.from_user.id:
        chatbot = True
        learn = True
        learning = ""
        cache = ""
        if chatbot == True and learn == True:
            update.message.reply_text('Send a message! Get it computed! Settings: Logic: ' + tpstring + ' Rate:' + temps + ' GPT-3. I am in the learning chatbot mode.')
        if chatbot == True and learn == False:
            update.message.reply_text('Send a message! Get it computed! Settings: Logic: ' + tpstring + ' Rate:' + temps + ' GPT-3 I am in the chatbot mode.')
        if chatbot == False:
            update.message.reply_text('Send a message! Get it computed! Settings: Logic: ' + tpstring + ' Rate:' + temps + ' GPT-3 I am in the finishsentence mode.')
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
            update.message.reply_text('Send a message! Get it computed! Settings: Logic: ' + tpstring + ' Rate:' + temps + ' GPT-3. I am in the learning chatbot mode.')
        if chatbot == True and learn == False:
            update.message.reply_text('Send a message! Get it computed! Settings: Logic: ' + tpstring + ' Rate:' + temps + ' GPT-3 I am in the chatbot mode.')
        if chatbot == False:
            update.message.reply_text('Send a message! Get it computed! Settings: Logic: ' + tpstring + ' Rate:' + temps + ' GPT-3 I am in the finishsentence mode.')
        return
    if user == update.message.from_user.id:
        chatbot = True
        learn = False
        learning = ""
        cache = ""
        if chatbot == True and learn == True:
            update.message.reply_text('Send a message! Get it computed! Settings: Logic: ' + tpstring + ' Rate:' + temps + ' GPT-3. I am in the learning chatbot mode.')
        if chatbot == True and learn == False:
            update.message.reply_text('Send a message! Get it computed! Settings: Logic: ' + tpstring + ' Rate:' + temps + ' GPT-3 I am in the chatbot mode.')
        if chatbot == False:
            update.message.reply_text('Send a message! Get it computed! Settings: Logic: ' + tpstring + ' Rate:' + temps + ' GPT-3 I am in the finishsentence mode.')
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
            update.message.reply_text('Send a message! Get it computed! Settings: Logic: ' + tpstring + ' Rate:' + temps + ' GPT-3. I am in the learning chatbot mode.')
        if chatbot == True and learn == False:
            update.message.reply_text('Send a message! Get it computed! Settings: Logic: ' + tpstring + ' Rate:' + temps + ' GPT-3 I am in the chatbot mode.')
        if chatbot == False:
            update.message.reply_text('Send a message! Get it computed! Settings: Logic: ' + tpstring + ' Rate:' + temps + ' GPT-3 I am in the finishsentence mode.')
        return
    if user == update.message.from_user.id:
        chatbot = False
        learn = False
        learning = ""
        cache = ""
        if chatbot == True and learn == True:
            update.message.reply_text('Send a message! Get it computed! Settings: Logic: ' + tpstring + ' Rate:' + temps + ' GPT-3. I am in the learning chatbot mode.')
        if chatbot == True and learn == False:
            update.message.reply_text('Send a message! Get it computed! Settings: Logic: ' + tpstring + ' Rate:' + temps + ' GPT-3 I am in the chatbot mode.')
        if chatbot == False:
            update.message.reply_text('Send a message! Get it computed! Settings: Logic: ' + tpstring + ' Rate:' + temps + ' GPT-3 I am in the finishsentence mode.')
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
            update.message.reply_text('Send a message! Get it computed! Settings: Logic: ' + tpstring + ' Rate:' + temps + ' GPT-3. I am in the learning chatbot mode.')
        if chatbot == True and learn == False:
            update.message.reply_text('Send a message! Get it computed! Settings: Logic: ' + tpstring + ' Rate:' + temps + ' GPT-3 I am in the chatbot mode.')
        if chatbot == False:
            update.message.reply_text('Send a message! Get it computed! Settings: Logic: ' + tpstring + ' Rate:' + temps + ' GPT-3 I am in the finishsentence mode.')
        return
    if user == update.message.from_user.id:
        chatbot = True
        learn = True
        learning = ""
        cache = ""
        if chatbot == True and learn == True:
            update.message.reply_text('Send a message! Get it computed! Settings: Logic: ' + tpstring + ' Rate:' + temps + ' GPT-3. I am in the learning chatbot mode.')
        if chatbot == True and learn == False:
            update.message.reply_text('Send a message! Get it computed! Settings: Logic: ' + tpstring + ' Rate:' + temps + ' GPT-3 I am in the chatbot mode.')
        if chatbot == False:
            update.message.reply_text('Send a message! Get it computed! Settings: Logic: ' + tpstring + ' Rate:' + temps + ' GPT-3 I am in the finishsentence mode.')
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
            update.message.reply_text('Send a message! Get it computed! Settings: Logic: ' + tpstring + ' Rate:' + temps + ' GPT-3. I am in the learning chatbot mode.')
        if chatbot == True and learn == False:
            update.message.reply_text('Send a message! Get it computed! Settings: Logic: ' + tpstring + ' Rate:' + temps + ' GPT-3 I am in the chatbot mode.')
        if chatbot == False:
            update.message.reply_text('Send a message! Get it computed! Settings: Logic: ' + tpstring + ' Rate:' + temps + ' GPT-3 I am in the finishsentence mode.')
        return
    if user == update.message.from_user.id:
        chatbot = True
        learn = False
        learning = ""
        cache = ""
        if chatbot == True and learn == True:
            update.message.reply_text('Send a message! Get it computed! Settings: Logic: ' + tpstring + ' Rate:' + temps + ' GPT-3. I am in the learning chatbot mode.')
        if chatbot == True and learn == False:
            update.message.reply_text('Send a message! Get it computed! Settings: Logic: ' + tpstring + ' Rate:' + temps + ' GPT-3 I am in the chatbot mode.')
        if chatbot == False:
            update.message.reply_text('Send a message! Get it computed! Settings: Logic: ' + tpstring + ' Rate:' + temps + ' GPT-3 I am in the finishsentence mode.')
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
            update.message.reply_text('Send a message! Get it computed! Settings: Logic: ' + tpstring + ' Rate:' + temps + ' GPT-3. I am in the learning chatbot mode.')
        if chatbot == True and learn == False:
            update.message.reply_text('Send a message! Get it computed! Settings: Logic: ' + tpstring + ' Rate:' + temps + ' GPT-3 I am in the chatbot mode.')
        if chatbot == False:
            update.message.reply_text('Send a message! Get it computed! Settings: Logic: ' + tpstring + ' Rate:' + temps + ' GPT-3 I am in the finishsentence mode.')
        return
    if user == update.message.from_user.id:
        chatbot = True
        learn = True
        learning = ""
        cache = ""
        if chatbot == True and learn == True:
            update.message.reply_text('Send a message! Get it computed! Settings: Logic: ' + tpstring + ' Rate:' + temps + ' GPT-3. I am in the learning chatbot mode.')
        if chatbot == True and learn == False:
            update.message.reply_text('Send a message! Get it computed! Settings: Logic: ' + tpstring + ' Rate:' + temps + ' GPT-3 I am in the chatbot mode.')
        if chatbot == False:
            update.message.reply_text('Send a message! Get it computed! Settings: Logic: ' + tpstring + ' Rate:' + temps + ' GPT-3 I am in the finishsentence mode.')
        return
    else:
        left = str(tim)
        update.message.reply_text('Bot is currently in use, make sure to set your settings when their timer runs down. ' + left + ' seconds.')

def regex(mew):
    data = mew
    if "You:" in data:
        data = data[0:data.find('You:')]
        if "Me:" in data:
            data = data[0:data.find('Me:')]
        return data
    if "Me:" in data:
        data = data[0:data.find('Me:')]
        if "You:" in data:
            data = data[0:data.find('You:')]
        return data
    if "?" in data:
        data = data[0:data.find('?')]
        data = data + "?"
        return data
    if "!" in data:
        data = data.rsplit('!', 1)[0]
        data = data + "!"
        return data
    else:
        data = data.rsplit('.', 1)[0]
        data = data + "."
        return data
    data = "Error."
    return data


def retry(bot, update):
    top_p = top
    temperature = temp
    mult = mx
    new = True
    comput = threading.Thread(target=wait, args=(bot, update, top_p, temperature, mult, new,))
    comput.start()

def runn(bot, update):
    top_p = top
    temperature = temp
    mult = mx
    new = False
    comput = threading.Thread(target=wait, args=(bot, update, top_p, temperature, mult, new,))
    comput.start()

def wait(bot, update, top_p, temperature, mult, new):
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
        compute = threading.Thread(target=interact, args=(bot, update, top_p, temperature, mult, new,))
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
def interact(bot, update, top_p, temperature, mult, new):
    global learning
    global learn
    global chatbot
    global cache
    tex = update.message.text
    text = str(tex)
    # Input sentiment analysis
    sentences = []
    sentences.append(text)
    analyzer = SentimentIntensityAnalyzer()
    for sentence in sentences:
        vs = analyzer.polarity_scores(sentence)
        if debug == True:
            print("==========START==========")
            print("INPUT SENTIMENT:")
            print("{:-<65} {}".format(sentence, str(vs)))
            print(vs['neg'])
        if vs['neg'] > 0:
            update.message.reply_text('Input sentiment is against content warning.')
            return
    if chatbot == True:
        textlength = len(text.split())
        #Retry cached text and process length
        if new == True and cache:
            m = re.search('.* You:', cache)
            raw_text = m.group(0)
            cac = len(raw_text.split())
            textlength = cac - 2   
            length = textlength
            if textlength < 20:
                length = 20
            if textlength > 20:
                length = 20
            if textlength > 30:
               length =  40
            if textlength > 50:
                length = 60
            if debug == True:
                print("Cache is...")
                print(raw_text)
        #Run on new text and process length
        if new != True:
            wolf = 'Me:' + text
            initial = wolf + ' You:'
            raw_text = learning + initial
            length = textlength
            if textlength < 20:
                length = 20
            if textlength > 20:
                length = 20
            if textlength > 30:
               length =  40
            if textlength > 50:
                length = 60
            cache = raw_text
        #Cache length/memory limiter
        tgt = len(raw_text.split())
        if tgt > 300:
            while tgt > 300:
                if debug == True:
                    print("Reducing memory of chat.")
                raw_text = raw_text.split(' Me:', 1)[-1]
                raw_text = "Me:" + raw_text
                tgt = len(raw_text.split())
                if tgt > 300:
                    if debug == True:
                        print("Reducing memory of chat.")
                    raw_text = raw_text.split('You:', 1)[-1]
                    raw_text = "You:" + raw_text
                    tgt = len(raw_text.split())
            if debug == True:
                print("FINAL MEMORY:")
                print(raw_text)
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
            length = len(text.split())
            textlength = length
            if debug == True:
                print("Cache is...")
                print(text)
        raw_text = text
    tx = float(top_p)
    cax = float(textlength)
    cay = float(mx)
    caz = float(cax * cay)
    #ta = ((1-tx)/caz)
    #top_p = ((tx) + (ta))
    top_p = caz + tx
    if top_p > 0.84:
        top_p = 0.84
    if top_p < 0.005:
        top_p = 0.005
#############################################
    update.message.reply_text('Computing...')
    try:
        response = openai.Completion.create(engine="davinci", prompt=raw_text, max_tokens=length, temperature=0.7, top_p=top_p)
        text = response['choices'][0]['text']
        if debug == True:
            print("Raw output: " + text)
        if chatbot == True:
            pika = text.splitlines()[0]
        else:
            pika = text
        stripes = pika.encode(encoding=sys.stdout.encoding,errors='ignore')
        tigger = stripes.decode("utf-8")
        mew = str(tigger)
        # disable any regex on finishsentence mode.
        if chatbot == True:
            meo = regex(mew)
            data = " ".join(re.split("[^a-zA-Z.,?!'*]+", meo))
            # Final regex
        else:
            data = mew
        if learn == True:
            learning = raw_text + data + " "
        sentences.clear()
        sentences.append(data)
        for sentence in sentences:
            vs = analyzer.polarity_scores(sentence)
            if debug == True:
                print("OUTPUT SENTIMENT:")
                print("{:-<65} {}".format(sentence, str(vs)))
                print(vs['neg'])
            if vs['neg'] > 0:
                update.message.reply_text('Output sentiment is against content warning.')
                return                
        update.message.reply_text(data)
        if debug == True:
            print("==========")
            mod = str(chatbot)
            print("chatbot: " + mod)
            lear = str(learn)
            print("Learn: " + lear)
            lent = str(length)
            print("Length: " + lent)
            ball = str(pika)
            print("Before regex: " + ball)
            print("Output: " + data)
            print("Raw_text or Original: " + raw_text)
            print("Learning text or Next: " + learning)
            tpa = str(tx)
            print("top_p in: " + tpa)
            tps = str(top_p)
            print("top_p out: " + tps)
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
