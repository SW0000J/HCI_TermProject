import pandas as pd
from konlpy.tag import Okt
import warnings
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
import joblib
import pickle

import analyze_youtube_comment.crawling.crawling_youtube as craw
import analyze_youtube_comment.processing.comment_processing as proc
import analyze_youtube_comment.processing.train as tr

warnings.filterwarnings(action="ignore")
okt = Okt()

def Train(youtubeId : str):
    badwords = proc.getBadWords()
    #train_data = pd.read_excel('./analyze_youtube_comment/train_src/train_data.xlsx').values.tolist()
    #train_df = proc.getProcessedDf(train_data)
    train_data = pd.read_csv('./analyze_youtube_comment/train_src/train_data.txt', sep='\t').values.tolist()
    train_df = proc.getTrainDf(train_data)

    crawledComments, videoInfoList = craw.getYoutubeComments(youtubeId)
    crawl_df = proc.getProcessedDf(crawledComments)
    preprocessedData = crawl_df.values.tolist()

    commentInfoList = tr.train(train_df, okt, preprocessedData, badwords, False)

    # Video - Title, VeiwCount, LikeCount, CommentCount
    #for i in videoInfoList:
    #    print(i)
    
    # Comment - BadCount, GoodCount, ExecCount, BadComment, GoodComment, ExecComment
    #for i in commentInfoList:
    #    print(i)

    video_key = ['Title', 'VeiwCount', 'LikeCount', 'CommentCount']
    comment_key = ['BadCount', 'GoodCount', 'ExecCount', 'BadComment', 'GoodComment', 'ExecComment']
    
    videoInfo = dict(zip(video_key, videoInfoList))
    commentInfo = dict(zip(comment_key, commentInfoList))

    passKey = ['VideoInfo', 'CommentInfo']
    passInfo = dict(zip(passKey, [videoInfo, commentInfo]))
    
    print(passInfo)

    return videoInfo, commentInfo

if __name__ == "__main__":
    Train("cCO22gPW6-4")
    # have to sort & countVector
    # have to fix web page