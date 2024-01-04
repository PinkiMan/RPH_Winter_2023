from utils import *
import utils


class TrainingCorpus():
    def __init__(self, directory):
        self.files = []
        self.truth = []
        self.dir = directory
        self.stats = []
        self.refsheet = directory + '/!truth.txt'
        self.get_classifications()
        self.parse()

    def get_classifications(self):
        with open(self.refsheet, 'r', encoding = 'utf-8') as f:
            for line in f:
                items = line.strip().split()
                if len(items) == 2 and items[1] in (SPAM_TAG, HAM_TAG):
                    if items[1] == SPAM_TAG:
                        type = 1
                    else:
                        type = -1
                    self.files.append(items[0])
                    self.truth.append(type)
        self.length = len(self.truth)

    def parse(self):
        for _, e in self.emails():
            headers, tokens = utils.parse_email(e)
            self.stats.append(Counter(tokens))
            #self.stats.append(utils.compute_statistic(headers, tokens))

    def emails(self):
        for i in range(self.length):
            body = ''
            file = self.files[i]
            with open(self.dir + '/' + file, 'r', encoding='utf-8') as f:
                body = f.read()
            yield file, body

    def testing_emails(self):
        for i in range(self.length):
            yield self.files[i], self.stats[i]

    def training_emails(self):
        for i in range(self.length):
            yield self.files[i], self.stats[i], self.truth[i]

