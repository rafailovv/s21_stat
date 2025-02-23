import os
import pandas as pd
import matplotlib
from matplotlib import pyplot as plt
from datetime import datetime

matplotlib.use('SVG')
PATH = os.path.dirname(os.path.abspath(os.path.join(__file__, "..")))

def createDatetimes() -> list[datetime]:
    dates = []
    for month in range(1, 3):
        if month == 1:
            for day in range(23, 32):
                dates.append(datetime(2025, month, day))
        else:
            for day in range(1, 15):
                dates.append(datetime(2025, month, day))
    return dates


def getHoursByNickname(df: pd.DataFrame, nick: str) -> pd.Series:
    return df[df.nickname == nick].iloc[0, 30:] / 60

def getExamsByNickname(df: pd.DataFrame, nick: str) -> pd.Series:
    return df[df.nickname == nick].iloc[0, [12, 18, 24, 29]]


def formatDates(dates: list[datetime], format: str) -> list[str]:
    return list(map(lambda x: x.strftime(format), dates))


def getExamDynamic(df: pd.DataFrame, nicknames: list[str], exams: list[str]) -> None:
    plt.figure(figsize=(15, 10))
    plt.title("Результаты экзаменов")
    plt.xlabel("Экзамен")
    plt.ylabel("XP за экзамен")
    plt.yticks(list(range(0, 46)))
    plt.grid(alpha=0.5, linestyle = "--", linewidth = 0.5)
        
    plt.plot(exams, [45] * 4, label = "Максимум", linestyle="--", color="red")

    for nick in nicknames:
        if nick in df.nickname.to_list():
            plt.plot(exams, getExamsByNickname(df, nick), label=nick)

    plt.legend()
    plt.savefig(os.path.join(PATH, "images\\exam.png"), bbox_inches="tight")
    plt.clf()
    
    
def getTimeDynamic(df: pd.DataFrame, nicknames: list[str], dates: list[datetime]) -> None:
    plt.figure(figsize=(20, 10))
    plt.title("Время в кампусе")
    plt.xlabel("Дата")
    plt.ylabel("Время, часы")
    plt.yticks(list(range(0, 25)))
    plt.grid(alpha=0.5, linestyle = "--", linewidth = 0.5)

    for nick in nicknames:
        if nick in df.nickname.to_list():
            plt.plot(dates, getHoursByNickname(df, nick), label=nick)

    plt.legend()
    plt.savefig(os.path.join(PATH, "images\\time.png"), bbox_inches="tight")
    plt.clf()