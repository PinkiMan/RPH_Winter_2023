from email.parser import Parser as EmailParser
from email.policy import default
from collections import Counter
from statistics import median, mean
import re

import time

SPAM_TAG = 'SPAM'
HAM_TAG = 'OK'


def dict_compare(filter, ref):
    score = 0
    #t0 = time.time_ns()
    for k, v in ref.items():
        if k in filter:
            f = filter[k]
            if (f < 0 and v < -f) or (f >= 0 and v > f):
                score += 1
    #print('2: ', time.time_ns() - t0)
    return score


def dict_threshold(spam, ham, ratio = 10):
    output = Counter()
    for k in spam:
        if k in ham:
            spam_list = spam[k].copy()
            ham_list = ham[k].copy()
            spam_list.sort()
            ham_list.sort()
            # print(spam_list)
            down = mean(spam_list) > mean(ham_list)
            if down:
                output[k] = minimize_error_rate_down(spam_list, ham_list, ratio)
            else:
                output[k] = minimize_error_rate_up(spam_list, ham_list, ratio)
        else:
            output[k] = 0
    return output

def roll_list(list, total_len, thresh, down):
    res = 0
    while list and roll_cond(list, thresh, down):
        if down:
            list.pop(-1)
        else:
            list.pop(0)
        res += 1
    return res

def roll_cond(list, thresh, down):
    if down:
        res = list[-1] >= thresh
    else:
        res = list[0] <= thresh
    return res

def minimize_error_rate_up(spam, ham, ratio = 10):
    spam_len = len(spam)
    ham_len = len(ham)
    fn = 0
    fp = ham_len
    threshold = 0
    total_len = spam_len + ham_len
    while spam and ham and fp > 0 and fp/ham_len * ratio > fn/spam_len:
        # set lowest necessary threshold
        if spam[0] > ham[0]:
            threshold = ham[0]
        else:
            threshold = spam[0]
        fn += roll_list(spam, total_len, threshold, False)
        fp -= roll_list(ham, total_len, threshold, False)

    return threshold

def minimize_error_rate_down(spam, ham, ratio = 10):
    spam_len = len(spam)
    ham_len = len(ham)
    fn = spam_len
    fp = 0
    threshold = 1
    total_len = spam_len + ham_len
    while spam and ham and fp == 0 and fp/ham_len * ratio < fn/spam_len:
        # set highest necessary threshold
        if spam[-1] < ham[-1]:
            threshold = ham[-1]
        else:
            threshold = spam[-1]
        fn -= roll_list(spam, total_len, threshold, True)
        fp += roll_list(ham, total_len, threshold, True)

    return -threshold

def dict_normalize(dict, length):
    for k in dict.keys():
        dict[k] /= length

def dict_list_append(dict, other):
    for k in other.keys():
        if k not in dict:
            dict[k] = []
        dict[k].append(other[k])

def read_classification_from_file(filename):
    res = {}
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            k, v = line.strip().split()
            if v != None:
                res[k] = v
    return res

def write_classification_to_file(filename, dictionary):
    with open(filename, 'w', encoding='utf-8') as f:
        for k, v in dictionary.items():
            print(k, v, file=f)


def parse_email(email):
    # parse email
    #parsed = EmailParser(policy=default).parsestr(email)
    #headers = parsed.items()
    #body = str(parsed.get_payload())
    # process body
    #cleaned = re.sub(r'\s', ' ', body)
    #cleaned = re.sub(r'<.*?>', '', cleaned)
    #tokens = list(filter(None, re.split(r'(\d+|\w+|\s)', cleaned)))
    # output
    #return headers, tokens
    return [], email.split()

def compute_statistic(headers, tokens):
    stats = StatCounter()
    stats.length += len(tokens)
    stats.words.update(tokens)
    stats.all_upper.update([p for p in tokens if p.isupper()])
    stats.all_lower.update([p for p in tokens if p.islower()])
    stats.normalize()
    return stats

class StatCounter:
    def __init__(self):
        self.length = 0
        self.words = Counter()
        self.all_upper = Counter()
        self.all_lower = Counter()
        # headers
        self.header_length = 0
        self.headers = HeaderCounter()

    def evaluate(self, other):
        total = 0
        total += dict_compare(self.words, other.words)
        total += dict_compare(self.all_upper, other.all_upper)
        total += dict_compare(self.all_lower, other.all_lower)
        return total

    def append(self, other):
        self.length += other.length
        dict_list_append(self.words, other.words)
        dict_list_append(self.all_upper, other.all_upper)
        dict_list_append(self.all_lower, other.all_upper)
        # headers
        self.headers.append(other.headers)

    def normalize(self):
        dict_normalize(self.words, self.length)
        dict_normalize(self.all_upper, self.length)
        dict_normalize(self.all_lower, self.length)
        # headers

    def prune(self):
        dict_prune(self.words)
        dict_prune(self.all_upper)
        dict_prune(self.all_lower)
        # headers


class HeaderCounter:
    def __init__(self):
        self.headers = {}

    def add(self, header, value):
        if header not in self.headers:
            self.headers[header] = Counter()
        self.headers[header].update(value)

    def append(self, other):
        for k in other.headers:
            if k in self.headers:
                self.headers[k] += other.headers[k]
            else:
                self.headers[k] = other.headers[k]



if __name__ == '__main__':
    a = {'a': [0.01, 0.02]}
    b = {'a': [0.001, 0.005]}

    c = dict_threshold(a, b)
    d = dict_threshold(b, a)
    print(c)
    print(d)
