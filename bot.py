from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
from dotenv import load_dotenv, find_dotenv
from command_handlers import (
    code_command_handler,
    deploy_quiz_command_handler,
    help_command_handler,
    intro_command_handler,
    list_quiz_command_handler,
    sample_command_handler,
    submit_question_command_handler,
    yolo_command_handler,
    about_command_handler,
)
from utils import add_text_message, add_typing, escape_reserved, get_chat_id


load_dotenv(find_dotenv())


def reply_value(update, context):
    value = update.message.text
    add_typing(update, context)
    add_text_message(update, context, escape_reserved("You inputed: " + value))


def get_text_from_callback(update):
    return update.callback_query.data


def echo(update, context):
    if update.message is not None:
        user_input = update.message.text
        add_typing(update, context)
        add_text_message(update, context, f"You said: {user_input}")


def main_handler(update, context):
    if update.message is not None:
        user_input = update.message.text
        if user_input == "yolo":
            add_typing(update, context)
            add_text_message(update, context, "YOLO")


def main():
    updater = Updater(os.environ.get("TELEGRAM_TOKEN", ""), use_context=True)
    dp = updater.dispatcher
    # command handlers
    dp.add_handler(CommandHandler("help", help_command_handler))
    dp.add_handler(CommandHandler("list", list_quiz_command_handler))
    dp.add_handler(CommandHandler("quiz", deploy_quiz_command_handler))
    dp.add_handler(CommandHandler("submit", submit_question_command_handler))
    dp.add_handler(CommandHandler("sample", sample_command_handler))
    dp.add_handler(CommandHandler("intro", intro_command_handler))
    dp.add_handler(CommandHandler("about", about_command_handler))
    dp.add_handler(CommandHandler("code", code_command_handler))
    dp.add_handler(CommandHandler("yolo", yolo_command_handler))
    # message handler
    dp.add_handler(MessageHandler(Filters.text, main_handler))

    ENV = os.environ.get("ENV", "")
    if ENV == "production":
        # Start the webhook
        TOKEN = os.environ.get("TELEGRAM_TOKEN", "")
        NAME = os.environ.get("NAME", "")
        PORT = int(os.environ.get("PORT", 5000))
        updater.start_webhook(
            listen="0.0.0.0",
            port=int(PORT),
            url_path=TOKEN,
            webhook_url=f"https://{NAME}.herokuapp.com/{TOKEN}",
        )
        updater.idle()
    elif ENV == "development":
        print("Bot is running locally...Press Ctrl-C to quit.")
        # start polling
        updater.start_polling()
        updater.idle()


if __name__ == "__main__":
    load_dotenv(find_dotenv())
    main()
