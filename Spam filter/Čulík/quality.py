from utils import *
import utils
import confmat

def quality_score_mat(mat):
    return quality_score(mat[1][1], mat[0][0], mat[0][1], mat[1][0])

def quality_score(tp, tn, fp, fn):
    up = (tn + tp)
    bottom = (up + fn + 10*fp)
    return up / bottom
    
def compute_quality_for_corpus(corpus_dir):
    truth = utils.read_classification_from_file(corpus_dir + '/!truth.txt')
    predict = utils.read_classification_from_file(corpus_dir + '/!prediction.txt')
    cm = confmat.BinaryConfusionMatrix(SPAM_TAG, HAM_TAG)
    cm.compute_from_dicts(truth, predict)
    return quality_score_mat(cm.stats)
