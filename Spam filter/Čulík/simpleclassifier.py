from collections import Counter
from statistics import mean
import numpy as np
import time

from corpus import Corpus
from trainingcorpus import TrainingCorpus
import quality

from utils import *
import utils

class SimpleClassifier:
    ''' Very simple, very effective '''
    def __init__(self):
        self.spam = Counter()
        self.ham = Counter()
        self.filter = Counter()

    def train(self, directory = ""):
        if directory:
            trcorp = TrainingCorpus(directory)
            self.fit(trcorp, np.ones(len(trcorp.files)))

    def test(self, directory = ""):
        if directory:
            corp = Corpus(directory)
            res = self.classify(corp)
            output = {}
            for i in range(len(res)):
                cls = HAM_TAG
                if res[i] == 1:
                    cls = SPAM_TAG
                output[corp.files[i]] = cls
            utils.write_classification_to_file(directory + '/!prediction.txt', output)

    def fit(self, input, weight):
        # process each file
        emails = input.training_emails()
        for i in range(input.length):
            _, stat, truth = next(emails)
            for key in stat:
                if truth == 1:
                    self.spam.update({key : stat[key] * weight[i]})
                else:
                    self.ham.update({key : stat[key] * weight[i]})

        for word in self.spam:
            if word not in self.ham:
                self.filter[word] += self.spam[word]

        self.thresh = max(self.filter.values()) / 2

    def classify(self, input):
        output = np.ones(input.length) * -1
        emails = input.testing_emails()
        for i in range(input.length):
            _, stat = next(emails)
            score = 0
            for word in stat:
                score += self.filter[word]
            if score > self.thresh:
                output[i] = 1
        return output

if __name__ == '__main__':
    scl = SimpleClassifier()
    scl.train('../spam-data-12-s75-h25/1/')
    testdir = '../spam-data-12-s75-h25/2/'
    scl.test(testdir)
    print('Quality: ', quality.compute_quality_for_corpus(testdir))
    print('Threshold: ', scl.thresh)
