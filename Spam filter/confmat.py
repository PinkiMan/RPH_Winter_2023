



class BinaryConfusionMatrix:
    def __init__(self, pos_tag,neg_tag):
        self.pos_atg=pos_tag
        self.neg_tag = neg_tag

        self.TP = 0
        self.TN = 0
        self.FP = 0
        self.FN = 0

    def as_dict(self):
        return {'tp':self.TP,'tn':self.TN,'fp':self.FP,'fn':self.FN}

    def update(self, truth, prediction):
        if truth not in [self.pos_atg,self.neg_tag] or prediction not in [self.pos_atg,self.neg_tag]:
            return ValueError
        else:
            if truth==self.pos_atg and prediction==self.pos_atg:
                self.TP+=1
            elif truth==self.pos_atg and prediction==self.neg_tag:
                self.FN+=1
            elif truth==self.neg_tag and prediction==self.pos_atg:
                self.FP+=1
            elif truth==self.neg_tag and prediction==self.neg_tag:
                self.TN+=1

    def compute_from_dicts(self, truth_dict, pred_dict):
        for item in truth_dict:
            self.update(truth_dict[item],pred_dict[item])


