import json
import os
from quiz import send_quiz
from utils import (
    STARTER_MESSAGE,
    code_to_img,
    escape_reserved,
    get_chat_id,
    restricted,
    add_text_message,
)


def help_command_handler(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text(
        "Type /list to list all quizzes\nType /quiz x to send a quiz\nType /submit to submit a question\nType /sample to see a sample quiz"
    )


@restricted
def intro_command_handler(update, context):
    update.message.reply_text(STARTER_MESSAGE)


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
                file_qn += escape_reserved(
                    "\nQuestion " + str(idx + 1) + ": " + data[idx].get("question")
                )
            add_text_message(update, context, file_qn)
        # update.message.reply_text(f)


def yolo_command_handler(update, context):
    update.message.reply_text("You found it!YOLO!")


def submit_question_command_handler(update, context):
    update.message.reply_text(
        "Thank you! At the moment, you may submit a question through this link: \nhttps://forms.gle/aLssGK6QMekTR75n9"
    )
    # add_text_message(update, context, escape_dot("Enter a Question (required):"))
    # reply_value(update, context)
    # if not check_confimation(update, context):
    #     return
    # add_text_message(update, context, "Number of options? (required):")
    # reply_value(update, context)
    # add_text_message(update, context, "Option 1:")
    # add_text_message(update, context, "Add an explnation (default:none):")


def about_command_handler(update, context):
    update.message.reply_text("The Tea-A-Bot is created by Jun Xiong and Yongliang.")


def code_command_handler(update, context):
    if not context.args:
        update.message.reply_text("Please provide a code snippet")
        return
    try:
        context.bot.send_photo(
            chat_id=get_chat_id(update, context), photo=code_to_img(context.args[0])
        )
    except Exception as e:
        print(e)
