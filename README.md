# GPT3-Telegram-Chatbot
OpenAI chatbot for Telegram using GPT-3 with sentiment analysis safety using VaderSentiment.

[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)
[![Python 3.9.7](https://img.shields.io/badge/python-3.9.7-blue.svg)](https://www.python.org/downloads/release/python-397/)

Command reference:

```
start - Basic start command.
help - Show quick help command.
reset - Reset the conversation.
retry - Retry the current input.
username - Set your character. See /help
botname - Set the bot character. See /help 
```

To set your character see this example:
```/username Bill Gates```

To set the bot character name see this example:
```/botname Elon Musk Bot```


Set these options in the python file:
```
#OpenAI API key
openai.api_key = "YOUR OPENAI API KEY GOES HERE"
#Telegram bot key
tgkey = "YOUR TELEGRAM BOT KEY GOES HERE"
```

Runs on latest python and latest python-telegram-bot pip plugins.


### Screenshots
This is the chat and what the backend console looks like in debug mode:
![Alt text](https://i.imgur.com/TAIozL3.jpg "Normal Operating Mode and Backend")

For user privacy you can turn off debug in the python file.

### Notes
- The chat memory is configurable and might be safely set up to 3500 characters. Once it reaches 3000 characters the memory of the chat is reduced for api requirements. Each token is about 4-5 characters, and the api limit is 2000 tokens. When the limit is reached, the chat is cut off at a newline for continual operation. This can get expensive though, and if you can use less characters and reduce the memory by tweaking the ask function that would be helpful so the chat is not repetitive.

- The bot has a 5 minute configurable timer, each user has 5 minutes to make a response and then it will be available to the next user.
- The sentiment analysis should be set to around > 0.6 or > 0.7, when the negativity of the sentiment analysis is above this it will prompt for different input or a retry option.
- If you want to change the bot to roleplay mode, change lines 223 and 238 to:

```chat_log = 'The following is a roleplay between two users:\n\n'```
