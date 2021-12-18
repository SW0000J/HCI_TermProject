import pandas as pd
import numpy as np
import scipy.sparse as sp
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score
import joblib
import pickle
from konlpy.tag import Okt
import re
import warnings
import operator

class MTfidfVectorizer(TfidfVectorizer):
    def setIdfs(self, idfs):
        TfidfVectorizer.idf_ = idfs

def train(train_df : pd.DataFrame, okt : Okt, crawledComments : list, badwords : list, newTrainflag : bool):
    text = train_df['comment']
    score = train_df['label']

    train_x, test_x, train_y, test_y = train_test_split(text, score , test_size=0.2, random_state=0)
    #print(len(train_x), len(train_y), len(test_x), len(test_y))
    tfv = MTfidfVectorizer(tokenizer=okt.morphs, ngram_range=(1,2), min_df=3, max_df=0.9)

    if newTrainflag == True:
        tfv.fit(train_x)
        tfv_train_x = tfv.transform(train_x)

        print("fitted done")

        clf = LogisticRegression(random_state=0)
        params = {'C': [1, 3, 5, 5, 4, 5, 6, 7]}
        grid_cv = GridSearchCV(clf, param_grid=params, cv=3, scoring='accuracy', verbose=1)
        grid_cv.fit(tfv_train_x, train_y)

        print(grid_cv.best_params_, grid_cv.best_score_)

        tfv_test_x = tfv.transform(test_x)
        # test_predict = grid_cv.best_estimator_.score(tfv_test_x,test_y)
        test_predict = grid_cv.best_estimator_.predict(tfv_test_x)
        print('혐오 표현 분석 모델의 정확도 : ',round(accuracy_score(test_y, test_predict), 3))

        with open('./analyze_youtube_comment/train_src/vocabulary.dat', 'wb') as fin:
            pickle.dump(tfv.vocabulary_, fin)
        with open('./analyze_youtube_comment/train_src/vector_idfs.dat', 'wb') as fin:
            pickle.dump(tfv.idf_, fin)
        with open('./analyze_youtube_comment/train_src/trained_set.dat', 'wb') as fin:
            pickle.dump(grid_cv, fin)
        
    else:
        grid_cv = pickle.load(open('./analyze_youtube_comment/train_src/trained_set.dat', 'rb'))
        idfs = pickle.load(open('./analyze_youtube_comment/train_src/vector_idfs.dat', 'rb'))
        vocabulary = pickle.load(open('./analyze_youtube_comment/train_src/vocabulary.dat', 'rb'))
        print(idfs)
        print(type(idfs))
        tfv.setIdfs(idfs)
        tfv._tfidf._idf_diag = sp.spdiags(idfs, diags=0, m=len(idfs), n=len(idfs))
        tfv.vocabulary_ = vocabulary

    #print(tfv)
    print(grid_cv)

#def predict(crawledComments : list, badwords : list, tfv : TfidfVectorizer, clf : LogisticRegression, grid_cv : GridSearchCV) -> list:
    bad_count = 0
    good_count = 0
    exc_count = 0
    bad_dataL = []
    good_dataL = []
    exc_dataL = []

    for comment_data in crawledComments:
        commentDataKey = ['Comment', 'Author', 'Date', 'CommentLikes', 'Label']
        commentInfo = dict(zip(commentDataKey, comment_data))

        try:
            comment = str(comment_data[0])
        
            comment = re.compile(r'[ㄱ-ㅣ가-힣]+').findall(comment)
            comment = [" ".join(comment)]

            st_tfidf = tfv.transform(comment)

            st_predict = grid_cv.best_estimator_.predict(st_tfidf)
            #print(st_predict)
            if(st_predict == 0 or badwords in comment):
                bad_dataL.append(commentInfo)
                bad_count += 1
            else:
                good_dataL.append(commentInfo)
                good_count += 1
        except:
            exc_dataL.append(commentInfo)
            exc_count += 1
            pass
    
    bad_dataL.sort(key=operator.itemgetter('CommentLikes', 'Comment'), reverse=True)
    good_dataL.sort(key=operator.itemgetter('CommentLikes', 'Comment'), reverse=True)
    exc_dataL.sort(key=operator.itemgetter('CommentLikes', 'Comment'), reverse=True)

    bad_key = [ str(i) for i in range(1, bad_count+1)]
    good_key = [ str(i) for i in range(1, good_count+1)]
    exc_key = [ str(i) for i in range(1, exc_count+1)]

    bad_data = dict(zip(bad_key, bad_dataL))
    good_data = dict(zip(good_key, good_dataL))
    exc_data = dict(zip(exc_key, exc_dataL))

    #print("bad count :", bad_count)
    #print("good count :", good_count)
    #print("exc count :", exc_count)
    #print("\nbad data :\n", bad_data)
    #print("\ngood data :\n", good_data)
    #print("\nexc data :\n", exc_data)

    return [str(bad_count), str(good_count), str(exc_count), bad_data, good_data, exc_data]