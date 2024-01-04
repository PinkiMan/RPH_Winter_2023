
import utils

import os,random

import corpus

class NaiveFilter:
    def __init__(self):
        pass

    def train(self, path):
        dictionary = utils.read_classification_from_file(path)

    def test(self, path):
        obj = corpus.Corpus(path)
        List = list(obj.emails())

        dictionary = {}
        for item in List:
            dictionary[item[0]]='OK'



        utils.write_classification_to_file(os.path.join(path,'!prediction.txt'),dictionary)



class ParanoidFilter:
    def __init__(self):
        pass

    def train(self, path):
        dictionary = utils.read_classification_from_file(path)

    def test(self, path):
        obj = corpus.Corpus(path)
        List = list(obj.emails())

        dictionary = {}
        for item in List:
            dictionary[item[0]]='SPAM'



        utils.write_classification_to_file(os.path.join(path,'!prediction.txt'),dictionary)


class RandomFilter:
    def __init__(self):
        pass

    def train(self, path):
        dictionary = utils.read_classification_from_file(path)

    def test(self, path):
        obj = corpus.Corpus(path)
        List = list(obj.emails())

        dictionary = {}
        for item in List:
            value = random.choice(['OK','SPAM'])
            dictionary[item[0]]=value

        utils.write_classification_to_file(os.path.join(path,'!prediction.txt'),dictionary)



