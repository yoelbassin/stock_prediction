from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.ensemble import AdaBoostClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import confusion_matrix
import utils
import numpy as np
import pandas as pd
import pickle
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import svm
from sklearn.model_selection import GridSearchCV
from utils import simplify, features





def model_train(n, dfn, model_type, duplicated_words):
    """
    Training the model using specific classifier

    :param n: number of train samples
    :param dfn: book data frame
    :param model_type: classifier type
    :return:
    """
    from sklearn.metrics import accuracy_score
    from joblib import dump
    x_unprocessed, y = dfn['X'][:n], dfn['y'][:n]

    x_test_unprocessed, y_test = dfn['X'][n:], dfn['y'][n:]

    x = [features(simplify(i), duplicated_words) for i in x_unprocessed]

    x_test = [features(simplify(i), duplicated_words) for i in x_test_unprocessed]

    model = model_type
    model.fit(x, y)
    y_pred = model.predict(x)
    print(model)
    print("Training acc: ", accuracy_score(y, y_pred))

    CM = confusion_matrix(y, y_pred)

    print("TN:", CM[0][0], " (", 100 * CM[0][0] / (CM[0][0] + CM[1][0]), "%) FN: ", CM[1][0], " TP: ", CM[1][1], " (",
          100 * CM[1][1] / (CM[1][1] + CM[0][1]), "%) FP: ", CM[0][1])

    y_expect = y_test
    y_pred = model.predict(x_test)
    print("Test acc: ", accuracy_score(y_expect, y_pred))

    CM = confusion_matrix(y_expect, y_pred)

    print("TN:", CM[0][0], " (", 100 * CM[0][0] / (CM[0][0] + CM[1][0]), "%) FN: ", CM[1][0], " TP: ", CM[1][1], " (",
          100 * CM[1][1] / (CM[1][1] + CM[0][1]), "%) FP: ", CM[0][1])

    dump(model, 'model.joblib')


def different_models_train():
    """
    Training the model using Naive bayes from the Sklearn library
    :return:
    """
    from sklearn.naive_bayes import BernoulliNB
    from sklearn.naive_bayes import GaussianNB
    from sklearn.naive_bayes import MultinomialNB
    from sklearn.gaussian_process.kernels import RBF
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.gaussian_process import GaussianProcessClassifier
    from sklearn.neural_network import MLPClassifier
    from sklearn.tree import DecisionTreeClassifier

    xls = pd.ExcelFile('data6.xls')
    df1 = pd.read_excel(xls, "Sheet 1 Today's Close")
    df2 = pd.read_excel(xls, "Sheet 2 Tomorrow's Start")
    df3 = pd.read_excel(xls, "Sheet 3 24 hours later")

    for i in range(1, 2):
        # Bernoulli
        # model_train(7500, df1, BernoulliNB(), i)
        # model_train(6000, df2, BernoulliNB(), i)
        # model_train(6000, df3, BernoulliNB(), i)

        # Gaussian
        # model_train(7500, df1, GaussianNB(), i)
        # model_train(6000, df2, GaussianNB(), i)
        # model_train(6000, df3, GaussianNB(), i)

        # Multinomial
        # model_train(7500, df1, MultinomialNB(), i)
        # model_train(6000, df2, MultinomialNB(), i)
        # model_train(6000, df3, MultinomialNB(), i)

        # SVM
        # model_train(7500, df1, svm.SVC(), i)
        # model_train(6000, df2, svm.SVC(), i)
        # model_train(6000, df3, svm.SVC(), i)

        # Random Forest
        # model_train(7500, df1, RandomForestClassifier(n_estimators=10, max_features='sqrt'), i)
        model_train(6000, df2, RandomForestClassifier(n_estimators=10, max_features='sqrt'), i)
        # model_train(6000, df3, RandomForestClassifier(n_estimators=10, max_features='sqrt'), i)

        # Neural Net
        # model_train(7500, df1, MLPClassifier(alpha=0.001, max_iter=1000), i)  # 0.49836601307189543 | 0.5196078431372549
        # model_train(6000, df2, MLPClassifier(alpha=0.001, max_iter=1000), i)  # 0.5184243964421855 | 0.5400254129606099
        # model_train(6000, df3, MLPClassifier(alpha=0.001, max_iter=1000), i)  # 0.5412960609911055 | 0.49174078780177893

        # Decision Trees
        # model_train(7500, df1, DecisionTreeClassifier(max_depth=7), i)
        # model_train(6000, df2, DecisionTreeClassifier(max_depth=7), i)
        # model_train(6000, df3, DecisionTreeClassifier(max_depth=7), i)

        # Ada boos
        # model_train(7500, df1, AdaBoostClassifier(), i)
        # model_train(6000, df2, AdaBoostClassifier(), i)
        # model_train(6000, df3, AdaBoostClassifier(), i)


if __name__ == "__main__":
    different_models_train()
