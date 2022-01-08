from telegram import Poll
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import telegram
import time
import os
from dotenv import load_dotenv, find_dotenv
import os
import json
import random
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import ImageFormatter
from functools import wraps

load_dotenv(find_dotenv())


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


def help_command_handler(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text(
        "Type /list to list all quizzes\nType /quiz x to send a quiz\nType /submit to submit a question\nType /sample to see a sample quiz"
    )


def sample_command_handler(update, context):
    update.message.reply_text("Sample Quiz Incoming!")
    send_quiz(update, context, 5)


@restricted
def deploy_quiz_command_handler(update, context):
    """Send a message when the command /help is issued."""
    if not context.args:
        update.message.reply_text("Please provide a quiz index\nE.g. /quiz 1")
        return
    update.message.reply_text("Quiz Incoming!")
    try:
        send_quiz(update, context, context.args[0])
    except Exception as e:
        print(e)


def list_quiz_command_handler(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text("Quiz List Incoming!")
    # get all file names from data
    files = os.listdir("data")
    files = [f.split(".")[0] for f in files]
    files = [f for f in files if f.isdigit()]
    files.sort()
    files = [f + ".json" for f in files]
    # send list of files
    for f in files:
        # read file
        with open(f"data/{f}") as fp:
            data = json.load(fp)
            # send file name
            file_qn = (
                "Quiz name:  "
                + f.split(".")[0]
                + "   \(Command to send: \\\quiz "
                + f.split(".")[0]
                + "\)\n"
            )
            # send file content
            for idx in range(len(data)):
                file_qn += escape_dot(
                    "\nQuestion " + str(idx + 1) + ": " + data[idx].get("question")
                )
            add_text_message(update, context, file_qn)
        # update.message.reply_text(f)


def check_confimation(update, context):
    add_text_message(update, context, escape_dot("y/n?"))
    confirmation = update.message.text
    if confirmation == "y":
        add_text_message(update, context, "Confirmed...")
        return True
    else:
        add_text_message(update, context, "Exitting...")
        return False


def reply_value(update, context):
    value = update.message.text
    add_typing(update, context)
    add_text_message(update, context, escape_dot("You inputed: " + value))


def submit_question_command_handler(update, context):
    update.message.reply_text(
        "Submit question through this link: \nhttps://forms.gle/aLssGK6QMekTR75n9"
    )
    # add_text_message(update, context, escape_dot("Enter a Question (required):"))
    # reply_value(update, context)
    # if not check_confimation(update, context):
    #     return
    # add_text_message(update, context, "Number of options? (required):")
    # reply_value(update, context)

    # add_text_message(update, context, "Option 1:")

    # add_text_message(update, context, "Add an explnation (default:none):")


def escape_dot(dotted_string):
    dotted_string = dotted_string.replace(".", "\.")
    dotted_string = dotted_string.replace("(", "\(")
    dotted_string = dotted_string.replace(")", "\)")
    dotted_string = dotted_string.replace("*", "\*")
    dotted_string = dotted_string.replace("_", "\_")
    dotted_string = dotted_string.replace("`", "\`")
    dotted_string = dotted_string.replace("~", "\~")
    return dotted_string


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
    context.bot.send_message(
        chat_id=get_chat_id(update, context),
        text=message,
        parse_mode=telegram.ParseMode.MARKDOWN_V2,
    )


def code_to_img(code):
    return highlight(code, PythonLexer(), ImageFormatter())


def send_code(context, chat_id, qn):
    if qn.get("code"):
        context.bot.send_photo(
            chat_id=chat_id,
            photo=code_to_img(qn.get("code")),
        )


def mcq(update, context, chat_id, qn):
    options = qn["correct_answers"] + qn["incorrect_answers"]
    random.shuffle(options)
    ans = 0
    for idx in range(len(options)):
        if options[idx] in qn["correct_answers"]:
            ans = idx
    context.bot.send_poll(
        chat_id=chat_id,
        question=qn["question"],
        options=options,
        type=Poll.QUIZ,
        correct_option_id=ans,
        explanation=qn.get("explanation"),
    )


def mrq(update, context, chat_id, qn):
    options = qn["correct_answers"] + qn["incorrect_answers"]
    random.shuffle(options)
    ans = []
    for idx in range(len(options)):
        if options[idx] in qn["correct_answers"]:
            ans.append(str(idx + 1))
    context.bot.send_poll(
        chat_id=chat_id,
        question=qn["question"],
        options=options,
        type=Poll.REGULAR,
        allows_multiple_answers=True,
    )
    ans_text = "The correct answers are:\n||"
    ans_text += ", ".join(ans)
    ans_text += "||"
    add_text_message(update, context, ans_text)
    if qn.get("explanation"):
        explanation_text = "The explanation:\n||" + qn["explanation"] + "||"
        add_text_message(update, context, escape_dot(explanation_text))


def send_quiz(update, context, qn_number):
    c_id = get_chat_id(update, context)
    with open(f"data/{qn_number}.json") as f:
        data = json.load(f)
        for qn in data:
            send_code(context, c_id, qn)
            if qn["type"] == "MCQ":
                mcq(update, context, c_id, qn)
            elif qn["type"] == "MRQ":
                mrq(update, context, c_id, qn)
            else:
                raise Exception("Unknown question type")


def echo(update, context):
    if update.message is not None:
        user_input = update.message.text
        # reply
        add_typing(update, context)
        add_text_message(update, context, f"You said: {user_input} ||spoiler||")
        add_text_message(update, context, "test\!")


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
        # start polling
        updater.start_polling()
        updater.idle()


if __name__ == "__main__":
    load_dotenv(find_dotenv())
    main()
