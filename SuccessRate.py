import pandas as pd
import numpy as np
from sklearn import pipeline,preprocessing,metrics,model_selection,ensemble
from sklearn_pandas import DataFrameMapper

def Success(m,f):
    data=pd.read_csv('data.csv')
    data["m_age"] = data["m_age"].fillna(data["m_age"].mode()[0])
    data["f_age"] = data["f_age"].fillna(data["f_age"].mode()[0])
    data["m_height"] = data["m_height"].fillna(data["m_height"].mean())
    data["f_height"] = data["f_height"].fillna(data["f_height"].mean())
    data["m_weight"] = data["m_weight"].fillna(data["m_weight"].mode()[0])
    data["f_weight"] = data["f_weight"].fillna(data["f_weight"].mode()[0])
    data["m_income"] = data["m_income"].fillna(data["m_income"].mean())
    data["f_income"] = data["f_income"].fillna(data["f_income"].mean())
    data = data.dropna(axis=0)
    mapper = DataFrameMapper([
        (['m_city', 'm_city', 'm_education', 'f_education', 'm_smoking', 'f_smoking', 'm_drinking', 'f_drinking'],
         preprocessing.OneHotEncoder()),
    ])
    X = ['m_age', 'f_age', 'm_city', 'f_city', 'm_height', 'f_height',
         'm_weight', 'f_weight', 'm_education', 'f_education', 'm_income',
         'f_income', 'm_smoking', 'f_smoking', 'm_drinking', 'f_drinking', ]

    Y = ['success_rate']

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
        ("model", KNeighborsClassifier(n_neighbors=1, metric='minkowski', p=5))
    ])

    ngb = pipeline_Kn.fit(data[X], data[Y].values.ravel())
    ngba = pipeline_Kn.score(data[X], data[Y].values.ravel())
    print("KNeighborsClassifier Accuracy =", ngba)

    from sklearn.tree import DecisionTreeClassifier

    pipeline_rfcla = pipeline.Pipeline([
        ('mapper', mapper),
        ("model", DecisionTreeClassifier(max_depth=10, random_state=70))
    ])
    rtcla = pipeline_rfcla.fit(data[X], data[Y].values.ravel())
    rtclaa = pipeline_rfcla.score(data[X], data[Y].values.ravel())
    print("DecisionTreeClassifier Accuracy =", rtclaa)

    from sklearn import naive_bayes

    pipeline_nv = pipeline.Pipeline([
        ('mapper', mapper),
        ("model", naive_bayes.BernoulliNB())
    ])

    nvfit = pipeline_nv.fit(data[X], data[Y].values.ravel())
    nvacc = pipeline_nv.score(data[X], data[Y].values.ravel())
    print("Naive Bayes Accuracy =", nvacc)

    from sklearn.cluster import KMeans

    pipeline_kmeans = pipeline.Pipeline([
        ('mapper', mapper),
        ("model", KMeans(n_clusters=40))
    ])
    kmeansf = pipeline_kmeans.fit(data[X], data[Y].values.ravel())
    kmeansc = pipeline_kmeans.score(data[X], data[Y].values.ravel())
    print("KMeans Accuracy =", nvacc)

    pipeline_rfc = pipeline.Pipeline([
        ('mapper', mapper),
        ("model", ensemble.RandomForestClassifier(n_estimators=70))
    ])

    rfcf = pipeline_rfc.fit(data[X], data[Y].values.ravel())
    rfcfa = pipeline_rfc.score(data[X], data[Y].values.ravel())
    print("RandomForestClassifierr Accuracy =", rfcfa)

    temp = {}
    temp['m_age'] = m.age
    temp['f_age'] = f.age
    temp['m_height'] = m.height
    temp['f_height'] = f.height
    temp['m_weight'] = m.weight
    temp['f_weight'] = f.weight
    temp['m_city'] = m.city
    temp['f_city'] = f.city
    temp['m_education'] = m.education
    temp['f_education'] = f.education
    temp['m_income'] = m.annual_income
    temp['f_income'] = f.annual_income
    temp['m_drinking'] = m.drinking_habit
    temp['f_drinking'] = f.drinking_habit
    temp['m_smoking'] = m.smoking_habit
    temp['f_smoking'] = f.smoking_habit

    testData = pd.DataFrame({'i': temp}).transpose()
    print(testData)
    result=[]
    rnd = ob.predict(testData)[0]
    result.append(rnd)
    print("Using Random Forest Regressor =", round(rnd, 2), "%")
    knn = ngb.predict(testData)[0]
    result.append(knn)
    print("Using KNeighborsClassifier =", round(knn, 2), "%")
    nv = nvfit.predict(testData)[0]
    result.append(nv)
    print("Using Naive Bayes =", round(nv, 2), "%")
    km = kmeansf.predict(testData)[0]
    result.append(km)
    print("Using Kmeans Bayes =", round(km, 2), "%")
    rmcs = rfcf.predict(testData)[0]
    result.append(rmcs)
    print("Using RandomforestClassifier Bayes =", round(rmcs, 2), "%")
    return max(result)



