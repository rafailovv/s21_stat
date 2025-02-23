import os
import io
import telebot
import pandas as pd
import functions.graph as graph
import dotenv

dotenv.load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")

bot = telebot.TeleBot(API_TOKEN, parse_mode="HTML")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "<b>Бот запущен!</b>")
    
    
@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message,
                 ("Для получения статистики - введи ники через запятую\n"
                 "При попытке отобразить <b>более 45 ников</b>, в легенде будут указаны <b>только</b> первые 45 ников\n"
                 "<i>*для получения средних значений, введите в качестве ника Средние</i>"))


@bot.message_handler(func=lambda message: True, content_types=["text"])
def echo_message(message):
    df = pd.read_csv(os.path.join(graph.PATH, "data\\users_means.csv"))

    dates = graph.formatDates(graph.createDatetimes(), "%d.%m")
    exams = ["E01D05", "E02D12", "E03D19", "E04D26"]

    nicknames = list(map(lambda x: x.strip(), message.text.split(',')))
    founded_nicknames_count = sum(df.nickname.isin(nicknames))
    
    if founded_nicknames_count > 0:
        exam_img_buffer = io.BytesIO(graph.getExamDynamic(df, nicknames, exams))
        time_img_buffer = io.BytesIO(graph.getTimeDynamic(df, nicknames, dates))
        
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

bot.infinity_polling()