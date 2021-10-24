# GPT3-Telegram-Chatbot
OpenAI chatbot for Telegram using GPT-3 with sentiment analysis safety using VaderSentiment.

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
