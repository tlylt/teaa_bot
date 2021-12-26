from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Poll
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackQueryHandler,
    PollHandler,
)
import telegram
import time
import os
from dotenv import load_dotenv, find_dotenv
import os
load_dotenv(find_dotenv())

def get_chat_id(update, context):
    chat_id = -1

    if update.message is not None:
        chat_id = update.message.chat.id
    elif update.callback_query is not None:
        chat_id = update.callback_query.message.chat.id
    elif update.poll is not None:
        chat_id = context.bot_data[update.poll.id]
    return chat_id


def help_command_handler(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text("Type /start")


def get_text_from_callback(update):
    return update.callback_query.data


def add_typing(update, context):
    context.bot.send_chat_action(
        chat_id=get_chat_id(update, context),
        action=telegram.ChatAction.TYPING,
        timeout=1,
    )
    time.sleep(1)


def add_text_message(update, context, message):
    context.bot.send_message(chat_id=get_chat_id(update, context), text=message)

def main_handler(update, context):
    if update.message is not None:
        user_input = update.message.text
        # reply
        add_typing(update, context)
        add_text_message(update, context, f"You said: {user_input}")
    # c_id = get_chat_id(update, context)
    # q = 'Question'
    # answers = ['Rome', 'London', 'Amsterdam']
    # context.bot.send_poll(chat_id=c_id, question=q, options=answers, type=Poll.QUIZ, correct_option_id=0)



# def poll_handler(update, context):
#     logging.info(f"question : {update.poll.question}")
#     logging.info(f"correct option : {update.poll.correct_option_id}")
#     logging.info(f"option #1 : {update.poll.options[0]}")
#     logging.info(f"option #2 : {update.poll.options[1]}")
#     logging.info(f"option #3 : {update.poll.options[2]}")

#     user_answer = get_answer(update)
#     logging.info(f"correct option {is_answer_correct(update)}")

#     add_typing(update, context)
#     add_text_message(update, context, f"Correct answer is {user_answer}")



def main():
    updater = Updater(
        os.environ.get("TELEGRAM_TOKEN", ""), use_context=True
    )
    dp = updater.dispatcher
    # command handlers
    dp.add_handler(CommandHandler("help", help_command_handler))
    # message handler
    dp.add_handler(MessageHandler(Filters.text, main_handler))
    # quiz handler
    #   dp.add_handler(PollHandler(poll_handler, pass_chat_data=True, pass_user_data=True))
    # start polling
    # updater.start_polling()
    # updater.idle()

    # Start the webhook
    TOKEN = os.environ.get("TELEGRAM_TOKEN", "")
    NAME = os.environ.get("NAME", "")
    PORT = int(os.environ.get('PORT', 5000))
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN,
                          webhook_url=f"https://{NAME}.herokuapp.com/{TOKEN}")
    updater.idle()

if __name__ == "__main__":
    load_dotenv(find_dotenv())
    main()
