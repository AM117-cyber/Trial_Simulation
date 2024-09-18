import random
from agent_methods import Juror
from utils import Message, Trait_Level, Veracity


class Intentions():
    def __init__(self):
        self.Share_only_most_relevant_fact_with_my_veracity = False # Strengthen_veracity_of_most_relevant_fact
        self.Share_only_that_fact_with_smaller_veracity = False # Diminish_veracity_of_poorly_explained_fact
        self.Share_only_most_relevant_fact_with_popular_opinion = False # Reach_consensus_on_most_relevant_fact
        self.Share_discrepancies_from_other_juror = False # Support_a_jurors_beliefs
        self.Share_opposite_discrepancies_from_other_juror = False # Contradict_a_jurors_beliefs
        self.Share_most_discrepant_facts = False # Convince_others_of_my_beliefs
        self.Share_most_discrepant_facts_middle = False # Convince_others_of_my_beliefs
        self.Share_less_discrepant_facts = False # Convince_others_of_my_beliefs
        self.Share_all_discrepant_facts = False # Convince_others_of_my_beliefs
        self.Share_all_facts_beliefs = False # Convince_others_of_my_beliefs



def execute_actions_general(juror:Juror, strength):
    answer = {}
    if juror.desires.Contradict_a_jurors_beliefs:
        juror.desires.Contradict_a_jurors_beliefs = False
        for fact in juror.context.message.beliefs_debated:
            if juror.context.message.beliefs_debated[fact] is Veracity.HIGH or juror.context.message.beliefs_debated[fact] is Veracity.UNCERTAIN:
                answer[fact] = Veracity.LOW
            else:
                answer[fact] = Veracity.HIGH
    elif juror.desires.Strengthen_veracity_of_most_relevant_fact:
        juror.desires.Strengthen_veracity_of_most_relevant_fact = False
        answer[juror.most_relevant_fact] = juror.beliefs.facts[juror.most_relevant_fact]
    elif juror.desires.Support_a_jurors_beliefs:
        juror.desires.Support_a_jurors_beliefs = False
        answer = juror.beliefs.other_jurors_beliefs[juror.juror_to_interact_with]
    elif juror.desires.Support_big_majority:
        juror.desires.Support_big_majority = False
        answer = juror.beliefs.majority_opinion
    elif juror.desires.Reach_consensus_on_most_relevant_fact:
        juror.desires.Reach_consensus_on_most_relevant_fact = False
        avg = juror.beliefs.facts[juror.most_relevant_fact].value
        for other_juror in juror.beliefs.other_jurors_beliefs:
            avg += juror.beliefs.other_jurors_beliefs[other_juror][juror.most_relevant_fact].value
        result = round(avg/(len(juror.beliefs.other_jurors_beliefs.keys()) + 1))
        answer[juror.most_relevant_fact] = result
    elif juror.desires.Convince_others_of_my_beliefs:
        juror.desires.Convince_others_of_my_beliefs = False
        answer = get_my_debate_message_with_value_high_openness(juror)
    elif juror.desires.Start_debate:
        juror.desires.Start_debate = False
        answer = juror.beliefs.facts
        juror.context.set_message(Message(juror,answer))
    return [answer,strength]

def get_my_debate_message_with_value_high_openness(juror: Juror):
    r = random.randint(1, 10)
    message = None
    if juror.agreeableness is Trait_Level.low:
        if r >= 4:
        # all
            message = get_all_beliefs_to_debate(juror, Trait_Level.high)
        else:
            #some
            message = get_some_beliefs_to_debate(juror, Trait_Level.high)
    elif juror.extraversion is Trait_Level.low and r >= 4:
        # some
        message = get_some_beliefs_to_debate(juror, Trait_Level.low)
    else:
        # all
        message = get_all_beliefs_to_debate(juror, Trait_Level.low)
    if juror.extraversion is Trait_Level.high:
        message[1] += 5
    return message

def get_some_beliefs_to_debate(juror: Juror, discrepance_level):
    """without considering majority or middle ground"""
    valid_facts_scores = 0
    valid_facts = {}
    for fact in juror.beliefs.facts.keys():
        for juror in juror.beliefs.other_jurors_beliefs.keys():
            difference = abs(juror.beliefs.other_jurors_beliefs[fact].value - juror.beliefs.facts[fact].value)
            if difference != discrepance_level.value:
                continue
            valid_facts_scores += 1
            if fact not in valid_facts:
                valid_facts[fact] = juror.beliefs.facts[fact]
    return [valid_facts,valid_facts_scores/len(valid_facts)]

def get_all_beliefs_to_debate(juror, discrepance_level):
    """without considering majority or middle ground"""
    discrepant_facts_scores = 0
    discrepant_facts = {}
    for fact in juror.beliefs.facts.keys():
        for other_juror in juror.beliefs.other_jurors_beliefs.keys():
            difference = abs(juror.beliefs.other_jurors_beliefs[other_juror][fact].value - juror.beliefs.facts[fact].value)
            if not difference:
                continue
            discrepant_facts_scores += 1
            if fact not in discrepant_facts:
                discrepant_facts[fact] = juror.beliefs.facts[fact]
    
    return [discrepant_facts,discrepant_facts_scores/len(discrepant_facts)]
    

def Share_only_most_relevant_fact_with_my_veracity(juror: Juror):
    """Strengthen_veracity_of_most_relevant_fact"""
def Share_only_that_fact_with_smaller_veracity(juror: Juror):
    """Diminish_veracity_of_poorly_explained_fact"""
def Share_only_most_relevant_fact_with_popular_opinion(juror: Juror):
    """Reach_consensus_on_most_relevant_fact"""
def Share_discrepancies_from_other_juror(juror: Juror):
    """Support_a_jurors_beliefs"""
def Share_opposite_discrepancies_from_other_juror(juror: Juror):
    """Contradict_a_jurors_beliefs"""
def Share_most_discrepant_facts(juror: Juror):
    """Convince_others_of_my_beliefs"""
def Share_most_discrepant_facts_middle(juror: Juror):
    """Convince_others_of_my_beliefs"""
def Share_less_discrepant_facts(juror: Juror):
    """Convince_others_of_my_beliefs"""
def Share_all_discrepant_facts(juror: Juror):
    """Convince_others_of_my_beliefs"""
def Share_all_facts_beliefs(juror: Juror):
    """Convince_others_of_my_beliefs"""