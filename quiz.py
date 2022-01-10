import random
import json

from telegram import Poll

from utils import add_text_message, escape_reserved, get_chat_id, code_to_img


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
        explanation_text = (
            "The explanation:\n||" + escape_reserved(qn["explanation"]) + "||"
        )
        add_text_message(update, context, explanation_text)


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
