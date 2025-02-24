""" Module providing graph for statistics """

import os
from io import BytesIO
from datetime import datetime
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('SVG')
PATH = os.path.dirname(os.path.abspath(os.path.join(__file__, "..")))

def get_hours_by_nickname(df: pd.DataFrame, nick: str) -> pd.Series:
    """ Return list of hours in campus by days by nickname """
    return df[df.nickname == nick].iloc[0, 30:] / 60


def get_exams_by_nickname(df: pd.DataFrame, nick: str) -> pd.Series:
    """ Return list of exams xp by nickname """
    return df[df.nickname == nick].iloc[0, [12, 18, 24, 29]]


def format_dates(dates: list[datetime], date_format: str) -> list[str]:
    """ Return list of dates formatting them in date_format """
    return list(map(lambda x: x.strftime(format=date_format), dates))


def create_datetimes() -> list[datetime]:
    """ Creating list of datetime objects from 23.01.2025 to 14.02.2025 """
    dates = []
    for month in range(1, 3):
        if month == 1:
            for day in range(23, 32):
                dates.append(datetime(2025, month, day))
        else:
            for day in range(1, 15):
                dates.append(datetime(2025, month, day))
    return dates


def get_exam_dynamic(df: pd.DataFrame, nicknames: list[str], exams: list[str]) -> bytes:
    """ Returns bytes object with exams graphs for nicknames picture (png) """
    plt.figure(figsize=(10, 10))
    plt.title("Результаты экзаменов")
    plt.xlabel("Экзамен")
    plt.ylabel("XP за экзамен")
    plt.yticks(list(range(0, 46)))
    plt.grid(alpha=0.5, linestyle = "--", linewidth = 0.5)

    plt.plot(exams, [45] * 4, label = "Максимум", linestyle="--", color="red")

    for nick in nicknames:
        if nick in df.nickname.to_list():
            plt.plot(exams, get_exams_by_nickname(df, nick), label=nick)

    plt.legend(bbox_to_anchor=(1.01, 1), borderaxespad=0)
    plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    plt.clf()
    return buffer.getvalue()


def get_time_dynamic(df: pd.DataFrame, nicknames: list[str], dates: list[datetime]) -> bytes:
    """ Returns bytes object with time in campus by days graphs for nicknames picture (png) """
    plt.figure(figsize=(20, 10))
    plt.title("Время в кампусе")
    plt.xlabel("Дата")
    plt.ylabel("Время, часы")
    plt.yticks(list(range(0, 25)))
    plt.grid(alpha=0.5, linestyle = "--", linewidth = 0.5)

    for nick in nicknames:
        if nick in df.nickname.to_list():
            plt.plot(dates, get_hours_by_nickname(df, nick), label=nick)

    plt.legend(bbox_to_anchor=(1.07, 1), borderaxespad=0)
    plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    plt.clf()
    return buffer.getvalue()
