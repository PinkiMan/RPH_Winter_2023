import numpy as np
import time
from math import isclose

from corpus import Corpus
from trainingcorpus import TrainingCorpus
from simpleclassifier import SimpleClassifier
import quality

from utils import *
import utils

class MyFilter:
    ''' AdaBoost based filer '''
    def __init__(self):
        self.trained = False
        self.reset_classifiers()
        self.clear_variables()

    def reset_classifiers(self, iterations = 0):
        self.classifiers = []
        self.classifier_weights = []
        self.classifier_length = iterations

    def clear_variables(self):
        self.input_weights = []
        self.input = None

    def train(self, directory = ""):
        if directory:
            self.fit(TrainingCorpus(directory))

    def test(self, directory = ""):
        if directory:
            corp = Corpus(directory)
            res = self.classify(corp)
            output = {}
            for i in range(res.size):
                cls = HAM_TAG
                if res[i] == 1:
                    cls = SPAM_TAG
                output[corp.files[i]] = cls
            utils.write_classification_to_file(directory + '/!prediction.txt', output)
        
    def get_prediction_error(self, prediction):
        error = (np.not_equal(self.input.truth, prediction)).astype(int)
        error_weights = self.input_weights * error
        error_weight_sum = sum(error_weights)
        return error_weight_sum / sum(self.input_weights)

    def update_input_weights(self, alpha, prediction):
        error = (np.not_equal(self.input.truth, prediction)).astype(int)
        self.input_weights *= np.exp(alpha * error)
        
    def fit(self, input, count = 16):
        self.trained = True
        self.reset_classifiers(count)
        # set fitting variables
        self.input_weights = np.ones(input.length) / input.length
        self.input = input
        # iterate and make weak classifiers
        start_time = time.time()
        for i in range(self.classifier_length):
            if i: self.update_input_weights(alpha, prediction)
            # print(self.input_weights)
            # fit weak classifier
            weak = SimpleClassifier()
            weak.fit(input, self.input_weights)
            self.classifiers.append(weak)
            # evaluate classifier
            prediction = weak.classify(input)
            # compute weak classifier weight
            error = self.get_prediction_error(prediction)
            if not isclose(error, 0):
                alpha = np.log((1 - error) / error)
                #print(error, ' ', alpha)
                self.classifier_weights.append(alpha)
            else:
                self.classifier_weights.append(1)
                self.classifier_length = i + 1
                break;

        # clean up
        self.clear_variables()
        print('Training Elapsed: ', time.time() - start_time)
            
    def classify(self, input):
        if self.trained:
            start_time = time.time()
            prediction = []
            # weighted weak predictions
            for i in range(self.classifier_length):
                classification = self.classifiers[i].classify(input)
                weak = classification * self.classifier_weights[i]
                prediction.append(weak)
            # final prediction
            prediction = np.array(prediction)
            if input.length:
                prediction = np.sum(prediction, axis = 0)
            print('Classification Elapsed: ', time.time() - start_time)
        else:
            prediction = np.ones(input.length) * -1
        result = np.sign(prediction)
        if np.isscalar(result):
            result = np.array([result])
        return result

if __name__ == '__main__':
    ada = MyFilter()
    ada.train('../spam-data-12-s75-h25/2/')
    testdir = '../spam-data-12-s75-h25/1/'
    ada.test(testdir)
    print('Quality: ', quality.compute_quality_for_corpus(testdir))
    for c in ada.classifiers:
        print(c.thresh)
