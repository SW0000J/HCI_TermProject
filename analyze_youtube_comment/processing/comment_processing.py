import pandas as pd
import csv

def getBadWords() -> list:
    badWordFile = open("analyze_youtube_comment/badwords/badwords.txt", 'r', encoding = "utf-8")
    badWords = []

    lines = badWordFile.readlines()
    for line in lines:
        line = line.strip()

        if not line: 
            break

        badWords.append(line)
    badWordFile.close()

    return badWords

def getPretreatmentComment(crawledComments : list) -> list:
    pretreatmentComment = []
    return pretreatmentComment