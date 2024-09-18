from enum import Enum
import numpy as np

class Vote(Enum):
    guilty = 0
    not_guilty = 1

class Trait_Level(Enum):
    high = 1
    undefined = 0
    low = -1

class Roles(Enum):
    leader = 1
    follower = 0
    negotiator = 2
    holdout = 2
    filler = 3


class S_Status(Enum):
    high= 1
    medium = 0

class Gender(Enum):
    male = 1
    female = 0

class Testimony_Impressions(Enum):
    nervous_witness = 0
    incoherent = 1
    not_backed_by_evidence = 2
    caught_lying = 3
    relatable = 4
    backed_by_evidence = 5

class Fact_Types(Enum):
    motive = 1
    oportunity = 2
    character = 3
    causality = 4
    intention = 5

class Fact():
    def __init__(self,type, text):
        self.text = text
        self.type = type

class Fact_Info():
    def __init__(self,relevance, veracity):
        self.relevance = relevance
        self.veracity = veracity

class Phase(Enum):
    aplication_strategies = 1
    witness_testimony = 2
    juror_feedback = 3
    info_pooling = 4
    belief_confrontation = 5


class Case_beliefs():
    def __init__(self,facts_info):
        self.facts_info = facts_info

        
class Info_pooling_data():
    def __init__(self,jurors_that_have_talked, message: Case_beliefs, sender_juror,):
        self.jurors_that_have_talked = jurors_that_have_talked
        self.message = message
        self.sender_juror = sender_juror

class Debating_points():
    def __init__(self,sender_juror, beliefs_debated, perssuassion_strategy):
        self.sender_juror = sender_juror
        self.beliefs_debated = beliefs_debated 
        self.perssuassion_strategy = perssuassion_strategy

class Message():
    def __init__(self,sender_juror, content):
        self.sender_juror = sender_juror
        self.beliefs_debated = content # beliefs the juror wants to discuss

class Veracity(Enum):
    HIGH = 3
    UNCERTAIN = 2
    LOW = 1

class StrategiesOwnWitnesses(Enum):
    Empathy_generation = 1
    Empathy_generation_altruistic_motive = 2
    Chronological_clarity = 3
    Chronological_clarity_detailed_observation = 4
    Reluctant_participation = 5

class StrategiesOpposingWitnesses(Enum):
    Memory_lapses = 1
    Biased_perspective = 2
    Motivational_doubts = 3
    Contradiction_trap = 4
    Emotion_unreliability = 5

class LawyerDesires_Enum(Enum):
    # With own witnesses
    Desire_to_maximize_witness_credibility = 0 # clarity chronical y clarity + detailed
    Desire_to_generate_positive_emotions_in_witnesses = 1 # empathy reluctante
    Desire_to_positively_influence_jurors = 2 # motive altruistic
    # With opposing witnesses
    Desire_to_destabilize_the_testimony_of_the_opposing_witness = 3 # emotion_unreliability, 
    Desire_to_reduce_the_credibility_of_the_opposing_witness = 4 # memory_lapses, trap
    Desire_to_make_the_jury_question_the_neutrality_of_the_opposing_witness = 5 # motivational_doubts, 
    Desire_to_discredit_the_testimony_of_the_opposing_witness_by_demonstrating_bias = 6 # bias 
class LawyerIntentions_Enum(Enum):
    Intention_to_execute_strategies_to_generate_empathy = 0 # empathy, empathy+motive,
    Intention_to_present_clear_and_logical_evidence = 1 # clarity, detailed
    Intention_to_underline_the_moral_duty_of_the_witness_when_testifying = 2 # reluctant

    Intention_to_weaken_contrary_testimony = 3 # mem laps, bias, trap
    Intention_to_ask_about_possible_benefits_the_witness_could_obtain = 4 # motivational_doubts, 
    Intention_to_ask_emotionally_provocative_questions = 5 # emotion_unreliablity

class WitnessIntentions_Enum(Enum):
    # Both
    Generate_sympathy = 0
    Convince_jury = 1
    Provide_detailed_information = 2
    Show_vulnerability = 3
    # Own 
    Strengthen_lawyer_narrative = 4
    # Opposing 
    Self_protection = 5
    Defend_aggressively = 6
    Keep_calm_under_pressure = 7    
    Avoid_difficult_questions = 8
    

def map_features(feat):
    cases = {
        Trait_Level.low : np.random.choice([2,3]),
        Trait_Level.undefined : np.random.choice([4,5,6]),
        Trait_Level.high : np.random.choice([7,8,9]),
        "Low" : np.random.choice([2,3]),
        "Middle" : np.random.choice([4,5,6]),
        "High" : np.random.choice([7,8,9]),
        'Internal' : np.random.choice([6,7,8,9]),
        'External' : np.random.choice([2,3,4]),
        0 : 'Leader',
        1 : 'Follower',
        2 : 'Filler',
        3 : 'Negotiator',
        4 : 'Holdout'
    }

    return cases[feat]

def map_intentions(index, is_own):
    if is_own:
        cases = {
            0 : WitnessIntentions_Enum.Generate_sympathy,
            1 : WitnessIntentions_Enum.Convince_jury,
            2 : WitnessIntentions_Enum.Provide_detailed_information,
            3 : WitnessIntentions_Enum.Show_vulnerability,
            4 : WitnessIntentions_Enum.Strengthen_lawyer_narrative
        }
    else:
        cases = {
            0 : WitnessIntentions_Enum.Generate_sympathy,
            1 : WitnessIntentions_Enum.Convince_jury,
            2 : WitnessIntentions_Enum.Provide_detailed_information,
            3 : WitnessIntentions_Enum.Show_vulnerability,
            4 : WitnessIntentions_Enum.Self_protection,
            5 : WitnessIntentions_Enum.Defend_aggressively,
            6 : WitnessIntentions_Enum.Keep_calm_under_pressure,
            7 : WitnessIntentions_Enum.Avoid_difficult_questions
        }

    return cases[index]

def map_trait_level(trait):
    cases = {
        "High" : Trait_Level.high,
        "Middle" : Trait_Level.undefined,
        "Low" : Trait_Level.low
    }

    return cases[trait]