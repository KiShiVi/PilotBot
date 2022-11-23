import random

import telebot
import sqlite3
from telebot import types
from datetime import datetime

API_TOKEN=''

db = sqlite3.connect('socio_bot.db')

c = db.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS PilotPensTable(
    chat_id text,
    answerCnt integer,
    answer1 text,
    answer2 text,
    answer3 text
)""")
db.commit()
db.close()

bot = telebot.TeleBot(API_TOKEN)
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
question_cnt = 0

@bot.message_handler(commands=["start"])
def start(m, res=False):
    db1 = sqlite3.connect('socio_bot.db')
    cur = db1.cursor()
    cur.execute(f"SELECT COUNT(*) FROM PilotPensTable WHERE chat_id LIKE {m.chat.id}")
    queryCnt = cur.fetchone()[0]

    if queryCnt > 0 and m.chat.id == 318117786:
        cur.execute(f"UPDATE PilotPensTable SET chat_id = '{str(int(318117786 * random.randint(1, 100) / 100 + datetime.now().second))}'"
                    f"WHERE chat_id LIKE {str(318117786)}")
        print("New: ", m.chat.id)
        cur.execute(f"INSERT INTO PilotPensTable VALUES({m.chat.id}, 1, '', '', '')")
        db1.commit()

    elif queryCnt == 0:
        print("New: ", m.chat.id)
        cur.execute(f"INSERT INTO PilotPensTable VALUES({m.chat.id}, 1, '', '', '')")
        db1.commit()
    bot.send_message(m.chat.id, 'Привет, сегодня мы узнаем настоящего потребителя перьевых ручек Pilot!')
    cur.execute(f"SELECT answerCnt FROM PilotPensTable WHERE chat_id LIKE {m.chat.id}")
    question_cnt = cur.fetchone()[0]
    if question_cnt == 1:
        new_buttons(["Да", "Нет"])
        bot.send_message(m.chat.id, 'Вы покупаете ручку в качестве подарка?', reply_markup=markup)
        print(1)
    elif question_cnt == 21:
        new_buttons(["Девушке", "Мужчине"])
        bot.send_message(m.chat.id, 'Вы дарите ручку мужчине или девушке?', reply_markup=markup)
        print(2)
    elif question_cnt == 22:
        new_buttons(["Да", "Нет"])
        bot.send_message(m.chat.id, 'У вас есть высшее образование?', reply_markup=markup)
        print(3)
    elif question_cnt == 31:
        new_buttons(["Да", "Нет"])
        bot.send_message(m.chat.id, 'Девушке часто приходится писать от руки?', reply_markup=markup)
    elif question_cnt == 32:
        new_buttons(["Да", "Нет"])
        bot.send_message(m.chat.id, 'Мужчине больше 35 лет?', reply_markup=markup)
    elif question_cnt == 33:
        new_buttons(["Да", "Нет"])
        bot.send_message(m.chat.id, 'У вас техническое образование?', reply_markup=markup)
    elif question_cnt == 34:
        new_buttons(["Да", "Нет"])
        bot.send_message(m.chat.id, 'У вас сидячая работа?', reply_markup=markup)



    elif question_cnt == 4:
        new_buttons(['/start'])
        bot.send_message(m.chat.id, 'Опрос уже пройден', reply_markup=markup)
        print(9)
    db1.close()

@bot.message_handler(content_types=["text"])
def handle_text(message):
    db1 = sqlite3.connect('socio_bot.db')
    cur = db1.cursor()
    cur.execute(f"SELECT answerCnt FROM PilotPensTable WHERE chat_id LIKE {message.chat.id}")
    question_cnt = cur.fetchone()[0]
    print(question_cnt)

    if question_cnt == 1:
        if message.text == "Да":
            cur.execute(f"""
            UPDATE PilotPensTable 
            SET answer1 = '{message.text}',
            answerCnt = 21
            WHERE chat_id LIKE {message.chat.id}
        """)
            db1.commit()
            print(21)
            new_buttons(["Девушке", "Мужчине"])
            bot.send_message(message.chat.id, 'Вы дарите ручку мужчине или девушке?', reply_markup=markup)
        else:
            cur.execute(f"""
                UPDATE PilotPensTable 
                SET answer1 = '{message.text}',
                answerCnt = 22
                WHERE chat_id LIKE {message.chat.id}
            """)
            db1.commit()
            print(22)
            new_buttons(["Да", "Нет"])
            bot.send_message(message.chat.id, 'У вас есть высшее образование?', reply_markup=markup)



    elif question_cnt == 21:
        if message.text == "Девушке":
            cur.execute(f"""
                    UPDATE PilotPensTable 
                    SET answer2 = '{message.text}',
                    answerCnt = 31
                    WHERE chat_id LIKE {message.chat.id}
                """)
            db1.commit()
            print(2)
            new_buttons(["Да", "Нет"])
            bot.send_message(message.chat.id, 'Девушке часто приходится писать от руки?', reply_markup=markup)
        else:
            cur.execute(f"""
                    UPDATE PilotPensTable 
                    SET answer2 = '{message.text}',
                    answerCnt = 32
                    WHERE chat_id LIKE {message.chat.id}
                """)
            db1.commit()
            print(2)
            new_buttons(["Да", "Нет"])
            bot.send_message(message.chat.id, 'Мужчине больше 35 лет?', reply_markup=markup)



    elif question_cnt == 22:
        if message.text == "Да":
            cur.execute(f"""
                    UPDATE PilotPensTable 
                    SET answer2 = '{message.text}',
                    answerCnt = 33
                    WHERE chat_id LIKE {message.chat.id}
                """)
            db1.commit()
            print(2)
            new_buttons(["Да", "Нет"])
            bot.send_message(message.chat.id, 'У вас техническое образование?', reply_markup=markup)
        else:
            cur.execute(f"""
                    UPDATE PilotPensTable 
                    SET answer2 = '{message.text}',
                    answerCnt = 34
                    WHERE chat_id LIKE {message.chat.id}
                """)
            db1.commit()
            print(2)
            new_buttons(["Да", "Нет"])
            bot.send_message(message.chat.id, 'У вас сидячая работа?', reply_markup=markup)



    elif [31, 32, 33, 34].__contains__(question_cnt):
        cur.execute(f"""
                        UPDATE PilotPensTable 
                        SET answer3 = '{message.text}',
                        answerCnt = 4
                        WHERE chat_id LIKE {message.chat.id}
                    """)
        db1.commit()
        new_buttons(['/start'])
        bot.send_message(message.chat.id, 'Спасибо за прохождение опроса!', reply_markup=markup)
        print(8)


    elif question_cnt == 4:
        new_buttons(['/start'])
        bot.send_message(message.chat.id, 'Опрос уже пройден', reply_markup=markup)
        print(9)
    db1.close()


def new_buttons(buttons_text):
    print(len(buttons_text), markup.keyboard.__len__())
    buttons_diff = len(buttons_text) - markup.keyboard.__len__()
    if buttons_diff > 0:
        for i in range(buttons_diff):
            markup.add(types.KeyboardButton(buttons_text[-i - 1]))
    elif buttons_diff < 0:
        for i in range(buttons_diff * -1):
            print('here')
            markup.keyboard.pop()
    for i in range(len(buttons_text)):
        markup.keyboard[i][0] = buttons_text[i]

bot.polling(none_stop=True, interval=0)