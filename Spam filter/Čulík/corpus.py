from os import listdir

from utils import *
import utils

class Corpus:
    def __init__(self, directory):
        self.dir = directory
        self.files = [f for f in listdir(self.dir) if not f.startswith('!')]
        self.stats = []
        self.length = len(self.files)
        self.parse()

    def parse(self):
        for _, e in self.emails():
            headers, tokens = utils.parse_email(e)
            self.stats.append(Counter(tokens))
            #self.stats.append(utils.compute_statistic(headers, tokens))

    def testing_emails(self):
        for i in range(self.length):
            yield self.files[i], self.stats[i]

    def emails(self):
        for email in self.files:
            body = ''
            with open(self.dir + '/' + email, 'r', encoding='utf-8') as f:
                body = f.read()
            yield email, body

