# -*- coding: utf-8 -*-
"""nb-with-explainability.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1zxag5cAFbU2s7EC-0ivzLhqf1_TOZmbZ
"""

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.naive_bayes import BernoulliNB, GaussianNB, MultinomialNB
import contractions
import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import lime
from lime import lime_text
from lime.lime_text import LimeTextExplainer

from google.colab import drive
drive.mount('/content/drive')

def get_detaset():
    train_df = pd.read_csv('/content/drive/MyDrive/IFT6390/kaggle2/train_data.csv')
    test_df = pd.read_csv('/content/drive/MyDrive/IFT6390/kaggle2/test_data.csv')
    train_result_df = pd.read_csv('/content/drive/MyDrive/IFT6390/kaggle2/train_results.csv')
    return train_df, test_df, train_result_df

def treat_detaset(train_df, test_df, train_result_df):
    train_df= train_df.drop(columns=['id'])
    test_df = test_df.drop(columns=['id'])
    train_result_df = train_result_df.drop(columns=['id'])

    train_result_df.loc[train_result_df['target'] == 'negative'] = 0
    train_result_df.loc[train_result_df['target'] == 'neutral'] = 1
    train_result_df.loc[train_result_df['target'] == 'positive'] = 2
    train_result_df = train_result_df.astype('int')
    return train_df, test_df, train_result_df

train_df, test_df, train_result_df = get_detaset()
X, X_test, y = treat_detaset(train_df, test_df, train_result_df)

X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.3, random_state=6390)

text_clf_NB = Pipeline([('vect', CountVectorizer(ngram_range=(1, 2))),
                         ('tfidf', TfidfTransformer(use_idf=False)),
                         ('clf-NB', MultinomialNB())
                        ])
_ = text_clf_NB.fit(X_train.text, y_train.target)
predicted_NB = text_clf_NB.predict(X_val.text)
np.mean(predicted_NB == y_val.target)

def explain(idx):
    class_names=[0,1,2]
    explainer = LimeTextExplainer(class_names=class_names, feature_selection = 'highest_weights', random_state = 6390)
    exp = explainer.explain_instance(X_val.text[idx], text_clf_NB.predict_proba, num_features=20, labels=[0,1,2])
    print ('Prediction probability of data point index %d' % idx)
    print (text_clf_NB.predict_proba((X_val.text[idx],)))
    print ('Explanation for class %d' % text_clf_NB.predict((X_val.text[idx],))[0])
    print ('\n'.join(map(str, exp.as_list(label=text_clf_NB.predict((X_val.text[idx],))[0]))))
    fig0 = exp.as_pyplot_figure(label=0)
    fig1 = exp.as_pyplot_figure(label=1)
    fig2 = exp.as_pyplot_figure(label=2)
    exp.show_in_notebook()
    return

explain(0)

explain(840641)