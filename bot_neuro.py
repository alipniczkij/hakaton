import pickle
import re
from functools import lru_cache

import numpy as np
import pymorphy2
from annoy import AnnoyIndex


def norm(text):
    morph = pymorphy2.MorphAnalyzer()

    @lru_cache(maxsize=100000)
    def get_normal_form(i):
        return morph.normal_forms(i)[0]

    def normalize_text(x):
        x = x[:200]
        return ' '.join([get_normal_form(i) for i in re.findall('\w+', x)])

    return normalize_text(text).split()


def get_similar(text):
    df = pickle.load(open('data.sav', 'rb'))
    w2v = pickle.load(open('w2v.sav', 'rb'))
    u = AnnoyIndex(100, 'angular')
    u.load('file')
    nrm = norm(text)
    nrm_1 = []
    for i in nrm:
        try:
            nrm_1.append(w2v.wv[i])
        except:
            nrm_1.append(np.zeros(100))
    nrm = np.mean(nrm_1, axis=0).tolist()
    pred_list = u.get_nns_by_vector(nrm, 5)
    ret_list = []
    for i in pred_list:
        ret_list.append(df['train'][i])
    return ret_list


def classify(text):
    vectorizer = pickle.load(open('vectorizer.sav', 'rb'))
    model = pickle.load(open('model.sav', 'rb'))
    return model.predict(vectorizer.transform([text]))
