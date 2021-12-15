import pandas as pd
from konlpy.tag import Okt
import warnings
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
import crawling.crawling_youtube as craw
import processing.comment_processing as proc
import processing.train as tr
import joblib
import pickle

warnings.filterwarnings(action="ignore")
okt = Okt()

def Train():
    badwords = proc.getBadWords()
    #train_data = pd.read_excel('./analyze_youtube_comment/train_src/train_data.xlsx').values.tolist()
    #train_df = proc.getProcessedDf(train_data)
    train_data = pd.read_csv('./analyze_youtube_comment/train_src/train_data.txt', sep='\t').values.tolist()
    train_df = proc.getTrainDf(train_data)

    crawledComments = craw.getYoutubeComments("cCO22gPW6-4")
    crawl_df = proc.getProcessedDf(crawledComments)
    preprocessedData = crawl_df.values.tolist()

    tr.train(train_df, okt, preprocessedData, badwords, False)

if __name__ == "__main__":
    Train()
    # have to fix save model
    # have to fix web page