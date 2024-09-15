from abc import ABC, abstractmethod
import random
from typing import List

from environment import SimulationContext
from utils import Gender, Message, Phase, Roles, S_Status, Trait_Level, Veracity
class AgentInterface(ABC):
    """Abstract base class for agent interfaces."""
    @abstractmethod
    def perceive_world(self):
        """Function that agents use to perceive the world around them and adjust their beliefs and desires."""
        pass

    @abstractmethod
    def execute_action(self):
        """Function to execute the intentions of the agent"""
        pass

class JurorBeliefs():
    def __init__(self, facts):

        self.facts = get_facts_in_format(facts)
        self.facts_with_value = facts
        self.other_jurors_beliefs = {}

class Juror(AgentInterface):
    def __init__(self,perceive_world_func,execute_action_func, id, openness, conscientiousness, extraversion, agreeableness, neuroticism, locus_of_control, social_norms, value_emotional_exp, takes_risks, takes_decisions_by_fear, bias, age, gender, race, socioeconomic_status, beliefs: JurorBeliefs):
        self.context = SimulationContext()
        self.id = id
        self.beliefs = beliefs
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

    def confidence_level(self):
        return sum(abs(level.value) for level in self.beliefs.facts.values())

    def update_facts_level(self, value, fact):
        if value < -15:
            self.beliefs.facts[fact] = Veracity.LOW
        elif value > 15:
            self.beliefs.facts[fact] = Veracity.HIGH
        else:
            self.beliefs.facts[fact] = Veracity.UNCERTAIN

    def perceive_world(self):
        return self.perceive_world_func(self)
        
    def execute_action(self):
        return self.execute_action_func(self)

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

def share_beliefs_general(juror: Juror):
    juror.context.append_message(Message(juror,juror.beliefs.facts)) 
    juror.context.pooling_speakers_count +=1

def process_debate_message_general(juror : Juror, message : Message):
    if juror.is_foreperson and not juror.context.message:
        # return my beliefs
        answer = get_my_debate_message_with_value_high_openness(juror)
        if not answer:
            juror.context.set_message(Message(juror,[juror.beliefs.facts]))
        else:
            juror.context.set_message(Message(juror,answer[0]))
    else:
        # process_message(get influence and update that jurors beliefs) and return my debate message with its value
        esteem = get_esteem_for_someone(juror, message.sender_juror)
        debated_beliefs_similarity = 2 * len(message.beliefs_debated.keys()) 
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
        answer =  get_my_debate_message_with_value_high_openness(juror)
    return answer

def calculate_belief_similarity(juror: Juror, sender_juror: Juror, facts):
    debated_beliefs_similarity = 2 * len(facts.keys()) 
    for fact in facts:
        difference = abs(juror.beliefs.other_jurors_beliefs[sender_juror][fact].value - facts[fact].value)
        debated_beliefs_similarity -= difference  # if belief is the same it adds 2 to the value, if it's close adds one, else adds 0
    return debated_beliefs_similarity
  
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
    return [discrepant_facts,discrepant_facts_scores/len(discrepant_facts)]
    

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
    return sorted(jurors, key=lambda juror: (juror.confidence_level(), juror.extraversion, juror.openness), reverse=True)
            