## Tea A Bot
Team
- Jun Xiong
- Yongliang

## Flow
1. The bot is deployed in the cloud and will be available after a command is issued to it.
2. Users either chat with the bot or add the bot into a telegram group.
3. Admin send a specific command to the bot.
4. The bot will respond to the command and send a series of quiz questions to the chat or telegram group.
5. The user will answer the quiz questions.

## User Stories
- As an admin, I want a command to trigger the bot to send out quiz questions into the group.
- As an admin, I want a way to store the quiz questions in the backend.
- As an admin, I want a way to organize the quiz questions into weeks.
- As an user, I want to be able to view the code in the quiz with syntax highlighting.
- Bonus: the users can submit a question to the bot for consideration.

## Development
1. git clone the repository (either via GitHub desktop or CLI)
2. change to project directory
 - `cd teaa_bot` 
3. create virtual environment
 - `python3 -m venv venv # If not created, creating virtualenv`
4. activate virtual environment
 - Windows: `venv\Scripts\activate.bat`
 - Mac: `source ./venv/bin/activate # Activating virtualenv`
 - (Better) using VSCode, select the python interpreter within the `venv` folder and the above is done automatically
5. install dependencies
 - `pip3 install -r ./requirements.txt # Installing dependencies`
6. to update dependencies requirements
 - `pip freeze > requirements.txt`
## Commands
- To re-deploy: `git push heroku main` (For the one with the hosting account)
- To start the bot locally: `python bot.py`
## Reference
- [Creating a Telegram Chatbot Quiz with Python](https://towardsdatascience.com/creating-a-telegram-chatbot-quiz-with-python-711a43c0c424)
- [Bring your Telegram Chatbot to the next level](https://towardsdatascience.com/bring-your-telegram-chatbot-to-the-next-level-c771ec7d31e4)
- [Deployment](https://towardsdatascience.com/how-to-deploy-a-telegram-bot-using-heroku-for-free-9436f89575d2)
- [python-telegram-bot on Heroku](https://github.com/Bibo-Joshi/ptb-heroku-skeleton)


## Inspiration
As TA's (teach assistants) we feel that it is very important to keep students engaged in the learning process. One of these methods to engage students is to ask them questions, and what better way to achieve this than by automating it using a telegram bot!

## What it does
Our bot houses a large library of questions from which the TA's can pick from. All they have to do is to add the bot to their teaching telegram group and voilà. It just works. With 2 simple commands, the user can browse through the list of quiz sets we have in our library as well as the questions in them.

## Functions
`/help` - brings up a help list
`/quiz [quiz_name]` - sends the quiz with quiz name specified (restricted to people with access only)
`/list` - lists all the quizzes
`/sample` - sample question to see how the bot sends
`/submit` - submit a sample question

## How we built it
We built this app with a python backend and hosted it on Heroku

## Challenges we ran into
Reading the bad documentation that plagues most python libraries 

## Accomplishments that we're proud of
A robot friend to help busy TAs manage and send short quizzes to their students.

## What we learned
Telegram truly is a powerful tool and their API enables many possibilities.

## What's next for Tea A Bot
More features:
- Support for multiple modules
- Support for more question types (possibly open-ended)
- Support for out of telegram quiz library UI

<!-- https://www.freeformatter.com/json-escape.html#ad-output -->