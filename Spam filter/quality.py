import os.path

import utils,confmat



def quality_score(tp, tn, fp, fn):
    return (tp+tn)/(tp+tn+10*fp+fn)

def compute_quality_for_corpus(corpus_dir):
    truth=utils.read_classification_from_file(os.path.join(corpus_dir,'!truth.txt'))
    prediction = utils.read_classification_from_file(os.path.join(corpus_dir, '!prediction.txt'))

    Binary=confmat.BinaryConfusionMatrix(pos_tag='SPAM',neg_tag='OK')

    Binary.compute_from_dicts(truth,prediction)

    Dict=Binary.as_dict()

    return quality_score(Dict['tp'],Dict['tn'],Dict['fp'],Dict['fn'])

#print(compute_quality_for_corpus('1'))