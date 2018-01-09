import os
import sys
import time
import networkx as nx
import json
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from operator import itemgetter
from matplotlib import colors
from matplotlib.patches import Ellipse, Circle
from matplotlib.backends.backend_pdf import PdfPages
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import scale


from env import *
from data_handler import DataHandler as dh
from lib_ml import MachineLearningLib as mll

class Metric(object):
    @staticmethod
    def cal_metric(TP, FP, TN, FN):
        res = {}
        res["acc"] = float(TP + TN) / float(TP + FP + FN + TN)
        res["precision"] = float(TP) / float(TP + FP) if TP + FP > 0 else 1.0
        res["recall"] = float(TP) / float(TP + FN) if TP + FN > 0 else 1.0
        try:
            res["F1"] = 1.0 / (1.0 / res["recall"] + 1.0 / res["precision"])
        except ZeroDivisionError:
            res["F1"] = 0.0
        return res

    @staticmethod
    def draw_pr(precision, recall, file_name = "pr.png"):
        index = np.array(range(len(precision)))
        width = 0.3
        tmplist1 = [(x, precision[x]) for x in precision]
        tmplist2 = [(x, recall[x]) for x in recall]
        tmplist1.sort()
        tmplist2.sort()
        X = [x[0] for x in tmplist1]
        y1 = [x[1] for x in Gtmplist1]
        y2 = [x[1] for x in tmplist2]
        plt.bar(index - width / 2, y2, width, color = "blue", label="recall")
        plt.bar(index + width / 2, y1, width, color = "red", label="precision")
        plt.grid(True, which='major')
        plt.grid(True, which='minor')
        plt.xticks(index, X, rotation = 45, size = 'small')
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.1), fancybox=True, ncol=5)

        plt.savefig(file_name)
        plt.close()

    @staticmethod
    def draw_circle_2D(embeddings, drawer, draw_path, draw_cnt):
        x = embeddings[:,0]
        y = embeddings[:,1]
        T = np.arctan2(x, y)

        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)

        ax.scatter(embeddings[:, 0], embeddings[:, 1], c = T, alpha = 0.8, marker='o')
        delta_x = -0.1
        delta_y = 0.1
        line_id = 0
        for emb in embeddings:
            ax.text(emb[0]+delta_x, emb[1]+delta_y, line_id, ha='center', va='bottom')
            line_id += 1
        plt.axis('scaled')
        plt.show()
        #file_path = draw_path+'/'+drawer['func']+'_'+str(draw_cnt)
        #pp = PdfPages(file_path)
        #pp.savefig(fig)
        #pp.close()


    @staticmethod
    def multiclass_classification(X, params):
        from sklearn.metrics import f1_score
        from sklearn.multioutput import MultiOutputClassifier
        from sklearn.linear_model import SGDClassifier
        X_scaled = scale(X)
        y = dh.load_ground_truth(os.path.join(DATA_PATH, params["ground_truth"]))
        y = y[:len(X)]
        for _ in xrange(params['times']):
            X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=params['test_size'], stratify=y)
            log = MultiOutputClassifier(SGDClassifier(loss='log'),n_jobs=2)
            log.fit(X_train, y_train)

            f1 = 0
            print(y_test.shape)
            for i in range(y_test.shape[1]):
                print(y_test[:, i])
                print(y_test[:, i])
                f1 = f1_score(y_test[:, i], log.predict(X_test)[:, i], average='micro')
        
    @staticmethod
    def classification(X, params):
        X_scaled = scale(X)
        y = dh.load_ground_truth(os.path.join(DATA_PATH, params["ground_truth"]))
        y = y[:len(X)]
        acc = 0.0
        for _ in xrange(params["times"]):
             X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size = params["test_size"], stratify = y)
             clf = getattr(mll, params["classification_func"])(X_train, y_train)
             acc += mll.infer(clf, X_test, y_test)[1]
        acc /= float(params["times"])
        return acc

<<<<<<< HEAD
if __name__ == '__main__':
    X = np.random.uniform(1, 10, 16).reshape(8, 2)
    drawer = {}
    drawer['func'] = 'abc'
    draw_cnt = 1
    Metric.draw_circle_2D(X, drawer, '', 1)
=======
>>>>>>> 2bd17514d67c70e8d4cb3f4bc2236da4eb4b9999
