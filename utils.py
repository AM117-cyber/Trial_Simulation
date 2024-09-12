from enum import Enum


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

class Fact():
    def __init__(self,type, text):
        self.text = text
        self.type = type

class Phase(Enum):
    witness_interrogation= 1
    info_pooling = 2
    belief_confrontation = 3


class Case_beliefs():
    def __init__(self,facts_info):
        self.facts_info = facts_info

        
class Info_pooling_data():
    def __init__(self,jurors_that_have_talked, total_jurors_amount, message: Case_beliefs, sender_juror,):
        self.jurors_that_have_talked = jurors_that_have_talked
        self.total_jurors_amount = total_jurors_amount 
        self.message = message
        self.sender_juror = sender_juror

class Debating_points():
    def __init__(self,sender_juror, beliefs_debated, perssuassion_strategy):
        self.sender_juror = sender_juror
        self.beliefs_debated = beliefs_debated 
        self.perssuassion_strategy = perssuassion_strategy

class Veracity(Enum):
    HIGH = 2
    UNCERTAIN = 1
    LOW = -15