""" Module providing graph for statistics """

import os
from io import BytesIO
from datetime import datetime, timedelta
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('Agg')  # Используем Agg для работы без GUI
PATH = os.path.dirname(os.path.abspath(os.path.join(__file__, "..")))

def get_hours_by_nickname(df: pd.DataFrame, nick: str) -> pd.Series:
    """ Return list of hours in campus by days by nickname """
    user_data = df[df.nickname == nick]
    if user_data.empty:
        return pd.Series([0] * (len(df.columns) - 30))  # Возвращаем пустой график
    return user_data.iloc[0, 30:].astype(float) / 60

def get_exams_by_nickname(df: pd.DataFrame, nick: str) -> pd.Series:
    """ Return list of exams XP by nickname """
    user_data = df[df.nickname == nick]
    if user_data.empty:
        return pd.Series([0, 0, 0, 0])  # Возвращаем пустой график
    return user_data.iloc[0, [12, 18, 24, 29]].astype(float)

def format_dates(dates: list[datetime], date_format: str) -> list[str]:
    """ Return list of formatted date strings """
    return [date.strftime(date_format) for date in dates]

def create_datetimes() -> list[datetime]:
    """ Creating list of datetime objects from 23.01.2025 to 14.02.2025 """
    start_date = datetime(2025, 1, 23)
    end_date = datetime(2025, 2, 14)
    return [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]

def plot_graph(title: str, xlabel: str, ylabel: str, x_values: list, y_values_dict: dict, y_ticks: list, max_line=None) -> bytes:
    """ General function to plot graphs """
    plt.figure(figsize=(12, 6))
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.yticks(y_ticks)
    plt.grid(alpha=0.5, linestyle="--", linewidth=0.5)

    if max_line:
        plt.plot(x_values, [max_line] * len(x_values), label="Максимум", linestyle="--", color="red")

    for nick, y_values in y_values_dict.items():
        plt.plot(x_values, y_values, label=nick)

    plt.legend(bbox_to_anchor=(1.01, 1), borderaxespad=0)
    plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format="png", dpi=100)  # Улучшенное качество
    plt.close()  # Закрываем график для освобождения памяти
    return buffer.getvalue()

def get_exam_dynamic(df: pd.DataFrame, nicknames: list[str], exams: list[str]) -> bytes:
    """ Returns bytes object with exams graphs for nicknames """
    y_values_dict = {nick: get_exams_by_nickname(df, nick) for nick in nicknames}
    return plot_graph("Результаты экзаменов", "Экзамен", "XP за экзамен", exams, y_values_dict, list(range(0, 46)), max_line=45)

def get_time_dynamic(df: pd.DataFrame, nicknames: list[str], dates: list[datetime]) -> bytes:
    """ Returns bytes object with time in campus by days graphs for nicknames """
    y_values_dict = {nick: get_hours_by_nickname(df, nick) for nick in nicknames}
    return plot_graph("Время в кампусе", "Дата", "Время, часы", dates, y_values_dict, list(range(0, 25)))
