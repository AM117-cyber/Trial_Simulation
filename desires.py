class Desires():
    def __init__(self):
        self.Strengthen_veracity_of_most_relevant_fact = False
        self.Diminish_veracity_of_poorly_explained_fact = False # if the veracity is very close to 0 (the juror is highly uncertain) and the relevance is very low, under 20%, then for the trial to be just assume that the fact is false
        self.Reach_consensus_on_most_relevant_fact = False # insist in that fact until everyone has the same opinion on it
        self.Support_a_jurors_beliefs = False
        self.Contradict_a_jurors_beliefs = False
        self.Convince_others_of_my_beliefs = False
        self.Support_big_majority = False
        self.Start_debate = False