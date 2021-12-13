import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score
from konlpy.tag import Okt
import re
import warnings

def train(train_df : pd.DataFrame, okt : Okt, crawledComments : list, badwords : list):
    text = train_df['comment']
    score = train_df['label']

    train_x, test_x, train_y, test_y = train_test_split(text, score , test_size=0.2, random_state=0)
    #print(len(train_x), len(train_y), len(test_x), len(test_y))

    tfv = TfidfVectorizer(tokenizer=okt.morphs, ngram_range=(1,2), min_df=3, max_df=0.9)
    tfv.fit(train_x)
    tfv_train_x = tfv.transform(train_x)
    #print(tfv_train_x)

    clf = LogisticRegression(random_state=0)
    params = {'C': [15, 18, 19, 20, 22]}
    grid_cv = GridSearchCV(clf, param_grid=params, cv=3, scoring='accuracy', verbose=1)
    grid_cv.fit(tfv_train_x, train_y)

    # 최적의 평가 파라미터는 grid_cv.best_estimator_에 저장됨
    print(grid_cv.best_params_, grid_cv.best_score_)# 가장 적합한 파라메터, 최고 정확도 확인

    tfv_test_x = tfv.transform(test_x)
    # test_predict = grid_cv.best_estimator_.score(tfv_test_x,test_y)
    test_predict = grid_cv.best_estimator_.predict(tfv_test_x)
    print('혐오 표현 분석 모델의 정확도 : ',round(accuracy_score(test_y, test_predict), 3))

#def predict(crawledComments : list, badwords : list, tfv : TfidfVectorizer, clf : LogisticRegression, grid_cv : GridSearchCV) -> list:
    bad = 0
    good = 0
    exc = 0
    bad_data = []
    good_data = []

    for comment_data in crawledComments:
        try:
            comment = str(comment_data[0])
        
            comment = re.compile(r'[ㄱ-ㅣ가-힣]+').findall(comment)
            comment = [" ".join(comment)]

            st_tfidf = tfv.transform(comment)

            st_predict = grid_cv.best_estimator_.predict(st_tfidf)
            
            if(st_predict == 1 or badwords in comment):
                bad_data.append(comment_data)
                bad += 1
            else:
                good_data.append(comment_data)
                good += 1
        except:
            exc += 1
            pass
    
    print("bad count :", bad)
    print("good count :", good)
    print("exc count :", exc)
    print("\nbad data :\n", bad_data)
    print("\ngood data :\n", good_data)
    
    return [bad_data, good_data, bad, good, exc]