import pandas as pd
from konlpy.tag import Okt
import warnings
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
import crawling.crawling_youtube as craw
import processing.comment_processing as proc
import processing.train as tr

warnings.filterwarnings(action="ignore")
okt = Okt()

if __name__ == "__main__":
    badwords = proc.getBadWords()
    train_data = pd.read_excel('./analyze_youtube_comment/train_src/train_data.xlsx').values.tolist()
    train_df = proc.getTrainDf(train_data)

    crawledComments = craw.getYoutubeComments("cCO22gPW6-4")
    crawl_df = proc.getTrainDf(crawledComments)
    preprocessedData = crawl_df.values.tolist()

    tr.train(train_df, okt, preprocessedData, badwords)

    # have to fix model, web page