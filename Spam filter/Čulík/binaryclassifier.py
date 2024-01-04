from collections import Counter
import numpy as np
import time

from corpus import Corpus
from trainingcorpus import TrainingCorpus
import quality

from utils import *
import utils

class BinaryClassifier:
    ''' 
        Complex and not very good, 
        doesn't work since parsing was changed
        to better suit SimpleClassifier 
    '''
    def __init__(self):
        self.spam = utils.StatCounter()
        self.ham = utils.StatCounter()
        self.filter = utils.StatCounter()

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

    def fit(self, input, weight, order = 1):
        # process each file
        for _, stat, truth in input.training_emails():
            if truth == 1:
                self.spam.append(stat)
            else:
                self.ham.append(stat)
        # select out filter parameters
        # header filter

        # body filter
        self.filter.words = utils.dict_threshold(self.spam.words, self.ham.words)
        self.filter.all_upper = utils.dict_threshold(self.spam.all_upper, self.ham.all_upper)
        self.filter.all_lower = utils.dict_threshold(self.spam.all_lower, self.ham.all_lower)

        weighted_sum = 0
        emails = input.testing_emails()
        for i in range(input.length):
            _, stat = next(emails)
            weighted_sum += self.filter.evaluate(stat) * weight[i] * order
        self.thresh = weighted_sum / np.sum(weight)

    def classify(self, input):
        output = np.ones(input.length) * -1
        emails = input.testing_emails()
        for i in range(input.length):
            _, stat = next(emails)
            score = self.filter.evaluate(stat)
            if score > self.thresh:
                output[i] = 1
            # print(score)

        return output

    def __str__(self):
        return str(self.filter.words) + '\n' + str(self.filter.all_upper) + '\n' + str(self.filter.all_lower)

if __name__ == '__main__':
    bincl = BinaryClassifier()
    bincl.train('../spam-data-12-s75-h25/1/')
    testdir = '../spam-data-12-s75-h25/2/'
    bincl.test(testdir)
    print('Quality: ', quality.compute_quality_for_corpus(testdir))

    #print(utils.parse_email('<abc>name___1 11_52 xx </def>:) yes!?\naaa'))

    #print(weak.filter.words)
    #print(weak.filter.all_upper)
    #print(weak.filter.all_lower)
