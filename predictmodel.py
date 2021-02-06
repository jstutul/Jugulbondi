import pandas as pd
import numpy as np
from sklearn import pipeline,preprocessing,metrics,model_selection,ensemble
from sklearn_pandas import DataFrameMapper


def tutul(temp):
    data = pd.read_csv('dataset.csv')
    data["age"] = data["age"].fillna(data["age"].mode()[0])
    data["height"] = data["height"].fillna(data["height"].mean())
    data["weight"] = data["weight"].fillna(data["weight"].mode()[0])
    data["income"] = data["income"].fillna(data["income"].mean())
    data = data.dropna(axis=0)
    mapper = DataFrameMapper([
        (['age', 'height', 'weight', 'income'], preprocessing.StandardScaler()),
        (['city', 'education', 'gender', 'body_type', 'complexin', 'drinking', 'smoking', 'religion', 'family_status', 'marital_status', 'physical_status'], preprocessing.OneHotEncoder()),
    ])
    X = ['age', 'height', 'weight', 'city', 'education', 'income', 'gender',
         'body_type', 'complexin', 'drinking', 'smoking', 'religion',
         'family_status', 'marital_status', 'physical_status']
    Y = ['id']

    pipeline_obj = pipeline.Pipeline([
        ('mapper', mapper),
        ("model", ensemble.RandomForestRegressor(n_estimators=70))
    ])
    ob = pipeline_obj.fit(data[X], data[Y].values.ravel())
    kn = pipeline_obj.score(data[X], data[Y].values.ravel())
    print("Random Forest Regressor Accuracy =", kn)
    from sklearn.neighbors import KNeighborsClassifier
    pipeline_Kn = pipeline.Pipeline([
        ('mapper', mapper),
        ("model", KNeighborsClassifier(n_neighbors=1, metric='minkowski', p=2))
    ])
    ngb = pipeline_Kn.fit(data[X], data[Y].values.ravel())
    ngba = pipeline_Kn.score(data[X], data[Y].values.ravel())
    print("KNeighborsClassifier Accuracy =", ngba)
    pipeline_rfcla = pipeline.Pipeline([
        ('mapper', mapper),
        ("model", ensemble.RandomForestClassifier(n_estimators=70))
    ])
    rtcla = pipeline_rfcla.fit(data[X], data[Y].values.ravel())
    rtclaa = pipeline_rfcla.score(data[X], data[Y].values.ravel())
    print("RandomForestClassifierr Accuracy =", rtclaa)
    from sklearn import naive_bayes
    pipeline_nv = pipeline.Pipeline([
        ('mapper', mapper),
        ("model", naive_bayes.BernoulliNB())
    ])
    nvfit = pipeline_nv.fit(data[X], data[Y].values.ravel())
    nvacc = pipeline_nv.score(data[X], data[Y].values.ravel())
    print("Naive Bayes Accuracy =", nvacc)


    testData = pd.DataFrame({'i': temp}).transpose()
    result=[]

    res=ob.predict(testData)[0]
    a=round(res)
    result.append(a)
    print("Using Random Forest Regressor =", res, "==", round(res))
    res = ngb.predict(testData)[0]
    b = round(res)
    result.append(b)
    print("Using KNeighborsClassifier =", res, "==", round(res))
    res = rtcla.predict(testData)[0]
    c=round(res)
    result.append(c)
    print("Using RandomForestClassifierr =", res, "==", round(res))
    res = nvfit.predict(testData)[0]
    d=round(res)
    result.append(d)
    print("Using Naive Bayes =", res, "==", round(res))
    result=list(dict.fromkeys(result))
    return result



