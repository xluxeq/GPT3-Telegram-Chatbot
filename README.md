# GPT3-Telegram-Chatbot
OpenAI chatbot for Telegram using GPT-3 with sentiment analysis safety using VaderSentiment.

Command reference:

```
start - Basic start command.
help - Show quick help command.
reset - Reset the conversation.
retry - Retry the current input.
username - Set your character. See /help
character - Set the bot character. See /help 
```

To set your character see this example:
```/username Bill Gates```

To set the bot character name see this example:
```/character Elon Musk Bot```


Set these options in the python file:
```
#OpenAI API key
openai.api_key = "YOUR OPENAI API KEY GOES HERE"
#Telegram bot key
tgkey = "YOUR TELEGRAM BOT KEY GOES HERE"
```

Runs on latest python and latest python-telegram-bot pip plugins.
