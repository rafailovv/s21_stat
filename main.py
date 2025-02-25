""" Secure and optimized Telegram bot """

import os
import io
import time
import re
from collections import defaultdict
import telebot
import pandas as pd
import dotenv
import functions.graph as graph

dotenv.load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")

bot = telebot.TeleBot(API_TOKEN, parse_mode="HTML")
user_requests = defaultdict(lambda: 0)  # Ограничение на частоту запросов
MAX_NICKNAMES = 50  # Максимальное количество ников в запросе

def sanitize_nickname(nick: str) -> str:
    """Удаляет нежелательные символы из ника и делает его безопасным"""
    return re.sub(r'[^a-zA-Z0-9_а-яА-Я]', '', nick.strip())

@bot.message_handler(commands=['start'])
def send_welcome(message: telebot.types.Message) -> None:
    """Отправляет приветственное сообщение"""
    bot.reply_to(message, "<b>Бот запущен! Введите ники через запятую.</b>")

@bot.message_handler(commands=['help'])
def send_help(message: telebot.types.Message) -> None:
    """Отправляет инструкцию по использованию"""
    bot.reply_to(message,
                 "Для получения статистики введите ники через запятую (не более 50).\n"
                 "Если ников больше 45, в легенде будут указаны только первые 45.\n"
                 "<i>*Чтобы получить средние значения, используйте ник 'Средние'</i>")

@bot.message_handler(func=lambda message: True, content_types=['text'])
def send_stats(message: telebot.types.Message) -> None:
    """Обрабатывает текстовые сообщения и отправляет графики"""
    user_id = message.from_user.id
    current_time = time.time()

    # Ограничение на частоту запросов (1 запрос в 5 секунд)
    if current_time - user_requests[user_id] < 5:
        bot.reply_to(message, "Подождите перед следующим запросом!")
        return
    user_requests[user_id] = current_time

    # Читаем данные из CSV
    try:
        df = pd.read_csv(os.path.join(graph.PATH, "data/users_means.csv"), dtype=str)
    except Exception:
        bot.reply_to(message, "Ошибка загрузки данных! Попробуйте позже.")
        return

    # Обработка введенных ников
    nicknames = sorted(set(map(sanitize_nickname, message.text.split(','))))
    if not nicknames:
        bot.reply_to(message, "<b>Вы не ввели ни одного корректного ника!</b>")
        return

    if len(nicknames) > MAX_NICKNAMES:
        bot.reply_to(message, f"Слишком много ников! Введите не более {MAX_NICKNAMES}.")
        return

    # Фильтрация существующих ников
    found_nicknames = [nick for nick in nicknames if nick in df.nickname.to_list()]
    if not found_nicknames:
        bot.reply_to(message, "<b>Ни одного ника не найдено!</b>")
        return

    # Генерация графиков
    try:
        exams = ["E01D05", "E02D12", "E03D19", "E04D26"]
        dates = graph.format_dates(graph.create_datetimes(), "%d.%m")

        exam_img_buffer = io.BytesIO(graph.get_exam_dynamic(df, found_nicknames, exams))
        time_img_buffer = io.BytesIO(graph.get_time_dynamic(df, found_nicknames, dates))

        exam_img = telebot.types.InputMediaPhoto(telebot.types.InputFile(exam_img_buffer),
                                                 caption="Экзамен и время в кампусе",
                                                 show_caption_above_media=True)
        time_img = telebot.types.InputMediaPhoto(telebot.types.InputFile(time_img_buffer),
                                                 show_caption_above_media=True)

        bot.send_media_group(message.chat.id, [exam_img, time_img], reply_to_message_id=message.id)
    except Exception:
        bot.reply_to(message, "Ошибка генерации графиков! Попробуйте позже.")

@bot.message_handler(func=lambda message: True)
def handle_invalid_messages(message: telebot.types.Message) -> None:
    """Обрабатывает все неподдерживаемые сообщения"""
    bot.reply_to(message, "<b>Пожалуйста, отправьте текстовое сообщение с никами.</b>")

if __name__ == "__main__":
    bot.infinity_polling()
