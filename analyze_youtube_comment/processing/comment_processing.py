import pandas as pd
import csv
import warnings
import re

warnings.filterwarnings(action="ignore")

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

def getTrainDf(crawledComments : list) -> pd.DataFrame:
    pretreatmentComment = []

    for commentData in crawledComments:
        commentData[0] = str(commentData[0])
        commentData[0] = commentData[0].strip()

        if not commentData[0]:
            break

        pretreatmentComment.append(commentData)

    train_df = pd.DataFrame(pretreatmentComment)
    train_df.columns = ['comment', 'author', 'date', 'numLikes', 'label']

    train_df = train_df[train_df['comment'].notnull()]
    #print(train_df.info())
    #print(train_df['label'].value_counts())

    train_df['comment'] = train_df['comment'].apply(lambda x : re.sub(r'[^ ㄱ-ㅣ가-힣]+', " ", x))
    #print(train_df.head())
    #print(train_df.info())

    return train_df