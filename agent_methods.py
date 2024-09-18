from abc import ABC, abstractmethod
from collections import Counter
import random
from typing import List

from desires import Desires
from environment import SimulationContext
from utils import Gender, Message, Phase, Roles, S_Status, Trait_Level, Veracity, Vote, map_features, Fact_Types
from expert_system_role import ExpertSystem
class AgentInterface(ABC):
    """Abstract base class for agent interfaces."""
    @abstractmethod
    def perceive_world(self):
        """Function that agents use to perceive the world around them and adjust their beliefs and desires."""
        pass

    @abstractmethod
    def execute_actions(self):
        """Function to execute the intentions of the agent"""
        pass


class JurorBeliefs():
    def __init__(self, facts):

        self.facts = get_facts_in_format(facts)
        self.facts_with_value = facts
        self.other_jurors_beliefs = {}
        self.majority_opinion = None
        self.esteem_for_others = {}

class Juror(AgentInterface):
    def __init__(self,perceive_world_func,execute_action_func, vote_function, id, openness, conscientiousness, extraversion, agreeableness, neuroticism, locus_of_control, social_norms, value_emotional_exp, takes_risks, takes_decisions_by_fear, bias, age, gender, race, socioeconomic_status, beliefs: JurorBeliefs):
        self.context = SimulationContext()
        self.id = id
        self.beliefs = beliefs
        self.desires = Desires()
        self.openness = openness
        self.conscientiousness = conscientiousness
        self.extraversion = extraversion
        self.agreeableness = agreeableness
        self.neuroticism = neuroticism
        self.locus_of_control = locus_of_control
        self.social_norms = social_norms
        self.value_emotional_exp = value_emotional_exp
        self.takes_risks = takes_risks
        self.takes_decisions_by_fear = takes_decisions_by_fear
        self.bias = bias
        self.gender = gender
        self.age = age
        self.race = race
        self.socioeconomic_status = socioeconomic_status
        self.perceive_world_func = perceive_world_func
        self.execute_action_func = execute_action_func
        self.is_foreperson = False
        self.role = None
        self.most_relevant_fact = None
        self.juror_to_interact_with = None
        self.vote_function = vote_function

    def confidence_level(self, facts):
        return sum(abs(level.veracity) for level in facts.values())

    def update_facts_level(self, value, fact):
        if value < -15:
            self.beliefs.facts[fact] = Veracity.LOW
        elif value > 15:
            self.beliefs.facts[fact] = Veracity.HIGH
        else:
            self.beliefs.facts[fact] = Veracity.UNCERTAIN

    def perceive_world(self):
        return self.perceive_world_func(self)
        
    def execute_actions(self,strength):
        return self.execute_action_func(self,strength)
    
    def vote(self):
        return self.vote_function(self)

def perceive_world_general(juror: Juror):
    """Basic way of perceiving the world for a juror"""
    if juror.context.phase is Phase.info_pooling:
        if juror.context.juror_to_speak != juror.id:
            adjust_others_beliefs_general(juror,juror.context.message)
        else:
            share_beliefs_general(juror)
    elif juror.context.phase is Phase.belief_confrontation:
        # perceive_world is called in belief_confrontation only if juror.context.message.sender.id != juror.id:
        answer = process_debate_message_general(juror,juror.context.message)
        return answer
    
def adjust_others_beliefs_general(juror : Juror, messages : Message):
    for message in messages:
        juror.beliefs.other_jurors_beliefs[message.sender_juror] = message.beliefs_debated
        juror.beliefs.esteem_for_others[message.sender_juror] = get_esteem_for_someone(juror, message.sender_juror)

def share_beliefs_general(juror: Juror):
    juror.context.append_message(Message(juror,juror.beliefs.facts)) 
    juror.context.pooling_speakers_count +=1

def process_debate_message_general(juror : Juror, message : Message):
    if juror.is_foreperson and not juror.context.message:
        # return my beliefs
        juror.desires.Start_debate = True
        return juror.execute_actions(0)
        # answer = get_my_debate_message_with_value_high_openness(juror)
        # if not answer:
        #     juror.context.set_message(Message(juror,[juror.beliefs.facts]))
        # else:
        #     juror.context.set_message(Message(juror,answer[0]))
    else:
        # process_message(get influence and update that jurors beliefs) and return my debate message with its value
        esteem = get_esteem_for_someone(juror, message.sender_juror)
        juror.beliefs.esteem_for_others[message.sender_juror] = esteem
        debated_beliefs_similarity = 2 * len(message.beliefs_debated.keys()) 
        # contradecir o apoyar como deseo, normal
        # si está en contra con todo lo compartido y la persona me cae mal y neurotic, si holdout prob mayor y si está en contra del foreperson y tu filler o follower
        # si eres leader o foreperson y yo filler o follower =>apoyar sería si compartimos lo debatido y me cae bien y high agreeablenness

        # update beliefs on sender_juror
        for fact in message.beliefs_debated:
            juror.beliefs.other_jurors_beliefs[message.sender_juror][fact] = message.beliefs_debated[fact]
            
            difference = abs(message.beliefs_debated[fact].value - juror.beliefs.facts[fact].value)
            debated_beliefs_similarity -= difference  # if belief is the same it adds 2 to the value, if it's close adds one, else adds 0
        
        all_beliefs_similarity = calculate_belief_similarity(juror, message.sender_juror, juror.beliefs.facts) # similarity between my beliefs and the ones in message
        if debated_beliefs_similarity >= len(message.beliefs_debated.keys()):
            all_beliefs_similarity += debated_beliefs_similarity

        influence = esteem + all_beliefs_similarity

        for fact in message.beliefs_debated:
            if message.beliefs_debated[fact].value < juror.beliefs.facts[fact].value:
                juror.beliefs.facts_with_value[fact].veracity-= influence
            else:
                juror.beliefs.facts_with_value[fact].veracity += influence
            juror.update_facts_level(juror.beliefs.facts_with_value[fact].veracity, fact)

        # generate desires and get an answer (intention) according to them
        prob = random.randint(1,10)
        motivation = juror.extraversion.value
        motivation += debated_beliefs_similarity
        if juror.role is Roles.leader and prob > 3:
            juror.desires.Convince_others_of_my_beliefs = True
            motivation +=1
        else:
            if esteem >= 10:
                if juror.role is Roles.filler:
                    if prob <=3:
                        juror.desires.Support_a_jurors_beliefs = True
                elif debated_beliefs_similarity >= 5 and juror.role is Roles.follower:
                    juror.desires.Support_a_jurors_beliefs = True

                motivation +=1
                return juror.execute_actions(motivation)
            most_esteemed = None
            tmp = 15
            for key in juror.beliefs.esteem_for_others.keys():
                if juror.beliefs.esteem_for_others[key] >= tmp:
                    tmp = juror.beliefs.esteem_for_others[key]
                    most_esteemed = key
            if most_esteemed and juror.extraversion is Trait_Level.high:
                juror.desires.Support_a_jurors_beliefs = True
                motivation += 1
                return juror.execute_actions(motivation)
            elif esteem < 1 and juror.extraversion is Trait_Level.high and all_beliefs_similarity < 3:
                juror.desires.Contradict_a_jurors_beliefs = True
                motivation += 4
                if juror.neuroticism is Trait_Level.high:
                    motivation +=2
                return juror.execute_actions(motivation)
            elif juror.role is Roles.holdout or juror.role is Roles.negotiator or juror.role is Roles.leader:
                most_relevant_fact = get_most_relevant_fact(juror.beliefs.facts_with_value)
                confidence = abs(most_relevant_fact.veracity)
                disagreeing_jurors = get_fact_disagreement(juror,most_relevant_fact)
                if confidence >= 30 and disagreeing_jurors >= 0.4: # bigger than 40 %
                    juror.desires.Strengthen_veracity_of_most_relevant_fact = True
                    if juror.conscientiousness is Trait_Level.high:
                        motivation += 2
                elif disagreeing_jurors >= 0.3 and juror.role is Roles.negotiator:
                    juror.desires.Reach_consensus_on_most_relevant_fact = True
                    motivation += 3
                return juror.execute_actions(motivation)
            common_belief = get_common_belief_different_from_yours(juror,8.3)
            if common_belief and juror.role is Roles.follower and prob >=4:
                juror.desires.Support_big_majority = True
                motivation += 2
                return juror.execute_actions(motivation)
        if not(juror.role is Roles.filler) and prob <=5:
            juror.desires.Convince_others_of_my_beliefs = True
        else:
            return None
        

def get_most_relevant_fact(facts):
    max_relevance = 0
    curr_rel_fact = None
    for fact in facts.keys():
        if facts[fact].relevance >= max_relevance:
            max_relevance = facts[fact].relevance
            curr_rel_fact = fact
    return curr_rel_fact

def get_fact_disagreement(juror: Juror,fact):
    disagreeing_jurors = 0
    fact_opinion_level = juror.beliefs.facts[fact].name
    for juror in juror.beliefs.other_jurors_beliefs.keys():
        if juror.beliefs.other_jurors_beliefs[juror][fact].name != fact_opinion_level:
            disagreeing_jurors +=1
    return disagreeing_jurors/len(juror.beliefs.other_jurors_beliefs.keys())


def get_common_belief_different_from_yours(juror: Juror, threshold=0.83):
    """
    Find facts where the most common veracity among other jurors differs from the given juror's belief,
    occurring in at least threshold percent of other jurors.

    Args:
        juror_beliefs (dict): Dictionary of dictionaries, where outer keys are juror names and inner dictionaries contain fact-veracity pairs.
        juror_name (str): Name of the juror whose beliefs we're comparing against.
        threshold (float): Minimum percentage of agreement required (default=0.83).

    Returns:
        dict: Facts that meet the criteria, mapped to their most common veracity.
    """
    # Get the total number of other jurors
    
    discrepant_facts = {}
    
    for fact in set(fact for beliefs in juror.beliefs.other_jurors_beliefs.values() for fact in beliefs):
        # Count occurrences of each veracity for this fact across all jurors except the given one
        veracity_counts = Counter(belief for name, belief in juror.beliefs.facts.items())
        
        # Find the most common veracity
        most_common_veracity = veracity_counts.most_common(1)[0]
        
        # Calculate the percentage of agreement
        agreement_percentage = most_common_veracity[1] / juror.context.jury_size
        
        # Check if the most common veracity meets the threshold and differs from the given juror's belief
        if agreement_percentage >= threshold:
            if most_common_veracity[0] != juror.beliefs.facts[fact]:
                discrepant_facts[fact] = most_common_veracity[0]
    
    return discrepant_facts

# def process_debate_message_general(juror : Juror, message : Message):
#     if juror.is_foreperson and not juror.context.message:
#         # return my beliefs
#         answer = get_my_debate_message_with_value_high_openness(juror)
#         if not answer:
#             juror.context.set_message(Message(juror,[juror.beliefs.facts]))
#         else:
#             juror.context.set_message(Message(juror,answer[0]))
#     else:
#         # process_message(get influence and update that jurors beliefs) and return my debate message with its value
#         esteem = get_esteem_for_someone(juror, message.sender_juror)
#         debated_beliefs_similarity = 2 * len(message.beliefs_debated.keys()) 
#         # contradecir o apoyar como deseo, normal
#         # si está en contra con todo lo compartido y la persona me cae mal y neurotic, si holdout prob mayor y si está en contra del foreperson y tu filler o follower
#         # si eres leader o foreperson y yo filler o follower =>apoyar sería si compartimos lo debatido y me cae bien y high agreeablenness

#         for fact in message.beliefs_debated:
#             juror.beliefs.other_jurors_beliefs[message.sender_juror][fact] = message.beliefs_debated[fact]
#             difference = abs(message.beliefs_debated[fact].value - juror.beliefs.facts[fact].value)
#             debated_beliefs_similarity -= difference  # if belief is the same it adds 2 to the value, if it's close adds one, else adds 0
#         all_beliefs_similarity = calculate_belief_similarity(juror, message.sender_juror, juror.beliefs.facts) # similarity between my beliefs and the ones in message
#         if debated_beliefs_similarity >= len(message.beliefs_debated.keys()):
#             all_beliefs_similarity += debated_beliefs_similarity
#         influence = esteem + all_beliefs_similarity
#         for fact in message.beliefs_debated:
#             if message.beliefs_debated[fact].value < juror.beliefs.facts[fact].value:
#                 juror.beliefs.facts_with_value[fact].veracity-= influence
#             else:
#                 juror.beliefs.facts_with_value[fact].veracity += influence
#             juror.update_facts_level(juror.beliefs.facts_with_value[fact].veracity, fact)
#         answer =  get_my_debate_message_with_value_high_openness(juror)
#     return answer

def calculate_belief_similarity(juror: Juror, sender_juror: Juror, facts):
    debated_beliefs_similarity = 2 * len(facts.keys()) 
    for fact in facts:
        difference = abs(juror.beliefs.other_jurors_beliefs[sender_juror][fact].value - facts[fact].value)
        debated_beliefs_similarity -= difference  # if belief is the same it adds 2 to the value, if it's close adds one, else adds 0
    return debated_beliefs_similarity
  

    
def get_esteem_for_someone(juror: Juror, sender_juror: Juror):
    esteem = 0
    if sender_juror.is_foreperson:
        esteem +=5
    if juror.role is Roles.holdout:
        return esteem
    if sender_juror.role is Roles.negotiator or Roles.leader:
        esteem +=3
    if juror.role is Roles.filler or juror.role is Roles.follower:
        esteem +=3
    return esteem


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
    discrepant_facts_scores = 0 if len(discrepant_facts) == 0 else discrepant_facts_scores/len(discrepant_facts)
    return [discrepant_facts,discrepant_facts_scores]
    

# def get_some_beliefs_to_debate(juror: Juror, discrepance_level):
#     """without considering majority or middle ground"""
#     valid_facts_scores = {}
#     for fact in juror.beliefs.facts.keys():
#         for juror in juror.beliefs.other_jurors_beliefs.keys():
#             difference = abs(juror.beliefs.other_jurors_beliefs[fact].value - juror.beliefs.facts[fact])
#             if difference != discrepance_level.value:
#                 continue
#             if fact in valid_facts_scores:
#                 valid_facts_scores[fact] += 1
#             else:
#                 valid_facts_scores[fact] = 1
    
def get_facts_in_format(fact_dict):
    """
    Convert a dictionary of facts with relevance and veracity scores to a dictionary with Veracity enums.

    Args:
        fact_dict (dict): Dictionary where keys are fact names and values are lists [relevance, veracity].

    Returns:
        dict: Dictionary where keys are fact names and values are Veracity enums.
    """
    converted_dict = {}

    for fact in fact_dict.keys():
        
        if fact_dict[fact].veracity < -15:
            converted_dict[fact] = Veracity.LOW
        elif fact_dict[fact].veracity> 15:
            converted_dict[fact] = Veracity.HIGH
        else:
            converted_dict[fact] = Veracity.UNCERTAIN

    return converted_dict



def set_foreperson(jury):
    foreperson_value = 0
    curr_foreperson = None
    for juror in jury:
        value = 0
        if juror.role is Roles.leader:
            value += 2
        if juror.extraversion is Trait_Level.high:
            value += 1
        if juror.gender is Gender.male:
            gender_bias = random.randint(0, 2)
            if gender_bias:
                value += 0.5
        if (juror.socioeconomic_status is S_Status.high) or (juror.socioeconomic_status is S_Status.medium):
            value +=1
        if juror.age >= average_age(jury):
            value += 1.5
        if value >= foreperson_value:
            foreperson_value = value
            curr_foreperson = juror
    curr_foreperson.is_foreperson = True
    return curr_foreperson

def average_age(jury):
    age_sum = 0
    for juror in jury:
        age_sum += juror.age
    return age_sum/len(jury)


def order_for_info_pooling(jurors):
    return sorted(jurors, key=lambda juror: (juror.confidence_level(juror.beliefs.facts_with_value), juror.extraversion.value, juror.openness.value), reverse=True)


def vote(juror):
    """
    Generate a juror's vote based on the relevance and veracity of facts.
    
    Parameters:
    facts (list of tuples): Each tuple contains (relevance, veracity) of a fact.
    
    Returns:
    str: 'Guilty' or 'Not Guilty'
    """
    total_relevance = sum(juror.beliefs.facts_with_value[fact[0]].relevance for fact in juror.beliefs.facts_with_value.items())
    weighted_veracity = sum(juror.beliefs.facts_with_value[fact[0]].relevance * juror.beliefs.facts_with_value[fact[0]].veracity for fact in juror.beliefs.facts_with_value.items()) / total_relevance
    
    # Decision threshold can be adjusted based on desired sensitivity
    decision_threshold = 0
    
    if weighted_veracity > decision_threshold:
        return Vote.guilty
    else:
        return Vote.not_guilty

def update_pool(jury_pool):
    for juror in jury_pool:
        expert = ExpertSystem(juror)
        juror.role = expert.role
        update_relevance_fact(juror)

def update_relevance_fact(juror):
    relevance_facts = [0]*5
    features = [juror.openness, juror.extraversion, juror.agreeableness, juror.conscientiousness, juror.neuroticism, 
                juror.locus_of_control, juror.value_emotional_exp, juror.takes_risks, juror.takes_decisions_by_fear, 
                juror.socioeconomic_status]
    features = [map_features(elem) for elem in features]
    # Predefined values ​​of the influence that a juror characteristic has on how he or she perceives a fact
    matrix_features_facts = [[0.1, 0.3, 0.2, 0.1, 0.3],
                            [0.2, 0.4, 0.1, 0.1, 0.2],
                            [0.1, 0.2, 0.4, 0.1, 0.3],
                            [0.3, 0.1, 0.1, 0.4, 0.1],
                            [0.2, 0.3, 0.1, 0.1, 0.3], 
                            [0.2, 0.1, 0.2, 0.3, 0.2],
                            [0.1, 0.2, 0.3, 0.1, 0.3],
                            [0.4, 0.1, 0.1, 0.3, 0.1],
                            [0.1, 0.3, 0.1, 0.1, 0.3],
                            [0.2, 0.4, 0.3, 0.1, 0.1]]
    
    for i in range(5):
        for j in range(10):
            relevance_facts[i] += features[j] * matrix_features_facts[j][i]

    relevance_facts = [rf/4 for rf in relevance_facts] # range of relevance of a fact [1-10]
    fact_dict = juror.beliefs.facts_with_value
    for fact in fact_dict.keys():
        if fact.type == Fact_Types.oportunity:
            fact_dict[fact].relevance = relevance_facts[0]
        elif fact.type == Fact_Types.motive:
            fact_dict[fact].relevance = relevance_facts[1]
        elif fact.type == Fact_Types.character:
            fact_dict[fact].relevance = relevance_facts[2]
        elif fact.type == Fact_Types.causality:
            fact_dict[fact].relevance = relevance_facts[3]
        elif fact.type == Fact_Types.intention:
            fact_dict[fact].relevance = relevance_facts[4]

def update_veracity(jurors, witness, fact):
    matrix_intentions_features = [[0.2, 0.2, 0.7, 0.6, 0.1],
                                  [0.5, 0.2, 0.8, 0.5, 0.0],
                                  [0.6, 0.9, 0.0, 0.1, 0.0],
                                  [0.2, 0.1, 0.3, 0.6, 0.0],
                                  [0.1, 0.7, 0.0, 0.1, 0.0],
                                  [0.1, 0.0, 0.0, 0.1, 0.0],
                                  [-0.2, -0.8, -0.3, -0.8, -0.9],
                                  [0.1, 0.2, 0.1, 0.1, 0.4],
                                  [-0.1, -0.5, -0.4, -0.3, -0.8]]
    for juror in jurors:
        features = [juror.openness, juror.conscientiousness, juror.extraversion, juror.agreeableness, juror.neuroticism]
        features = [map_features(elem) for elem in features]
        result = 0

        row = matrix_intentions_features[witness.context.get_witness_intention().value]
        for i in range(5):
            if i == 3 and row[i] == (-0.8):
                result = -8 + 0.8*features[i]
            else:
                result += features[i]*row[i]
        result = result*(-1) if witness.side else result
        juror.beliefs.facts_with_value[fact[0]].veracity += result
    