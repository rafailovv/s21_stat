""" Bot entry point """

import os
import io
import telebot
import pandas as pd
import dotenv
import functions.graph as graph

dotenv.load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")

bot = telebot.TeleBot(API_TOKEN, parse_mode="HTML")

@bot.message_handler(commands=['start'])
def send_welcome(message: telebot.types.Message) -> None:
    """ Send welcome message by start command """
    bot.reply_to(message, "<b>Бот запущен!</b>")


@bot.message_handler(commands=['help'])
def send_help(message: telebot.types.Message) -> None:
    """ Send help message for help command """
    bot.reply_to(message,
                 ("Для получения статистики - введи ники через запятую\n"
                 "При попытке отобразить <b>более 45 ников</b>, "
                 "в легенде будут указаны <b>только</b> первые 45 ников\n"
                 "<i>*для получения средних значений, введите в качестве ника Средние</i>"))


@bot.message_handler(func=lambda message: True, content_types=["text"])
def send_stats(message: telebot.types.Message) -> None:
    """ Send graphs by nicknames in message """
    df = pd.read_csv(os.path.join(graph.PATH, "data\\users_means.csv"))

    dates = graph.format_dates(graph.create_datetimes(), "%d.%m")
    exams = ["E01D05", "E02D12", "E03D19", "E04D26"]

    nicknames = sorted(set(map(lambda x: x.strip(), message.text.split(','))))
    founded_nicknames_count = sum(df.nickname.isin(nicknames))

    if founded_nicknames_count > 0:
        exam_img_buffer = io.BytesIO(graph.get_exam_dynamic(df, nicknames, exams))
        time_img_buffer = io.BytesIO(graph.get_time_dynamic(df, nicknames, dates))

        exam_img = telebot.types.InputMediaPhoto(telebot.types.InputFile(exam_img_buffer),
                                                 caption="Экзамен и время в кампусе",
                                                 show_caption_above_media=True)
        time_img = telebot.types.InputMediaPhoto(telebot.types.InputFile(time_img_buffer),
                                                 show_caption_above_media=True)

        bot.send_media_group(message.chat.id,
                            [exam_img, time_img],
                            reply_to_message_id=message.id)
    else:
        bot.reply_to(message,
                     "<b>Ни одного ника в сообщении не найдено!</b>")


if __name__ == "__main__":
    bot.infinity_polling()
