class BinaryConfusionMatrix:
    def __init__(self, pos_tag, neg_tag):
        self.tags = [neg_tag, pos_tag]
        self.stats = [[0, 0], [0, 0]]
    
    def as_dict(self):
        return {'tn': self.stats[0][0], 'tp' : self.stats[1][1], 'fn' : self.stats[1][0], 'fp' : self.stats[0][1]}
        
    def update(self, truth, prediction):
        if truth not in self.tags:
            raise ValueError('Truth not in tags.')
        if prediction not in self.tags:
            raise ValueError('Prediction not in tags.')  
        self.stats[truth == self.tags[1]][prediction == self.tags[1]] += 1
        
    def compute_from_dicts(self, truth_dict, pred_dict):
        for k in pred_dict:
            self.update(truth_dict[k], pred_dict[k])