from functools import wraps
import json
import os
import time
from telegram import ChatAction, ParseMode
from pygments import highlight
from pygments.lexers.jvm import JavaLexer
from pygments.formatters import ImageFormatter

STARTER_MESSAGE = "Hi all, to bolster learning, we will be sharing 3-4 MCQs that we adapted from Past Year Papers/lecture notes etc to test your knowledge of the module content so far. They should take no more than 5 mins to complete and are totally optional. We will post about once a week and attempts are anonymous. Feel free to try them and check your understanding:)"


def escape_reserved(raw):
    reserved = [
        "_",
        "*",
        "[",
        "]",
        "(",
        ")",
        "~",
        "`",
        ">",
        "#",
        "+",
        "-",
        "=",
        "|",
        "{",
        "}",
        ".",
        "!",
    ]
    for r in reserved:
        raw = raw.replace(r, "\\" + r)
    return raw


def restricted(func):
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in json.loads(os.environ.get("ADMINS", "")):
            print("Unauthorized access denied for {}.".format(user_id))
            update.message.reply_text(
                "Only admins can do that!\nContact @Jun_Xiong or @lyongl for help."
            )
            return
        return func(update, context, *args, **kwargs)

    return wrapped


def get_chat_id(update, context):
    chat_id = -1
    if update.message is not None:
        chat_id = update.message.chat.id
    elif update.callback_query is not None:
        chat_id = update.callback_query.message.chat.id
    elif update.poll is not None:
        chat_id = context.bot_data[update.poll.id]
    return chat_id


def add_typing(update, context):
    context.bot.send_chat_action(
        chat_id=get_chat_id(update, context),
        action=ChatAction.TYPING,
        timeout=1,
    )
    time.sleep(1)


def add_text_message(update, context, message):
    context.bot.send_message(
        chat_id=get_chat_id(update, context),
        text=message,
        parse_mode=ParseMode.MARKDOWN_V2,
    )


def check_confimation(update, context):
    add_text_message(update, context, escape_reserved("y/n?"))
    confirmation = update.message.text
    if confirmation == "y":
        add_text_message(update, context, "Confirmed...")
        return True
    else:
        add_text_message(update, context, "Exitting...")
        return False


def code_to_img(code):
    return highlight(code, JavaLexer(), ImageFormatter())
