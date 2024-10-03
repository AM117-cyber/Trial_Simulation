from agent_methods import AgentInterface
from environment import SimulationContext
from utils import Phase, map_intentions, WitnessIntentions_Enum, Rule, StrategiesOwnWitnesses, StrategiesOpposingWitnesses
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class Witness(AgentInterface):
    def __init__(self, id, perceive_world_func, execute_action_func, facts, age, socioeconomic_status, education, ineptitude, side):
        self.beliefs = WitnessBeliefs()
        self.desires = WitnessDesires()
        self.intentions = WitnessIntentions()
        self.context = SimulationContext()
        self.id = id
        self.perceive_world_func = perceive_world_func
        self.execute_action_func = execute_action_func
        self.facts = facts
        self.age = age
        self.socioeconomic_status = socioeconomic_status
        self.education = education
        self.ineptitude = ineptitude
        self.side = side
        # Predefined values ​​of the relation between witness' emotions and characteristics of jurors
        self.matrix_emotions_features = [[0.8, 0.1, 0.6, 0.9, -0.2],
                                         [0.4, 0.2, 0.4, 1.0, 0.0],
                                         [0.2, 0.9, 0.3, 0.4, -0.3],
                                         [0.6, 0.8, 0.9, 0.4, -0.7],
                                         [0.4, 1.0, 0.2, 0.3, -0.1], 
                                         [0.6, 0.4, 0.5, 0.5, -0.3],
                                         [-0.1, -0.6, 0.0, -0.8, 0.7],
                                         [0.3, 0.8, 0.5, 0.4, -0.9],
                                         [-0.5, -0.4, -0.6, -0.5, 0.9],
                                         [-0.1, -0.2, -0.3, -0.4, 0.8],
                                         [-0.3, -0.1, -0.5, 0.0, 0.6]]

    def perceive_world(self):
        return self.perceive_world_func(self)

    def execute_actions(self):
        return super().execute_actions()

# BDI Architecture   
class WitnessBeliefs():
    def __init__(self):
        self.emotions = {
            "empathy": 0, # empatia
            "sympathy": 0, # simpatia
            "credibility": 0, # credibilidad
            "confidence": 0, # confianza
            "responsibility": 0, # responsabilidad 
            "hope" : 0, # esperanza
            "frustration": 0, # frustracion
            "calm": 0, # calma 
            "fear": 0, # miedo
            "sadness": 0, # tristeza
            "shame": 0, # verguenza
            #"confusion": 0
        }
class WitnessDesires():
    def __init__(self):
        pass

class WitnessIntentions():
    def __init__(self):
        self.dict = {item : False for item in WitnessIntentions_Enum}

# RULES OF WITNESS
class GenerateEmpathyRule(Rule):
    """ Rule to update the emotions of witness with the strategy Generate Empathy"""
    def __init__(self, beliefs, context):
        super().__init__(beliefs, context)
    def match(self):
        strategy = self.context.get_ongoing_strategy()
        strategy = StrategiesOwnWitnesses(strategy) if self.context.witness_speaking.side else StrategiesOpposingWitnesses(strategy)
        return self.context.phase is Phase.witness_testimony and strategy == StrategiesOwnWitnesses.Empathy_generation
    def do(self):
        self.context.witness_speaking.beliefs.emotions['empathy'] += 2
        self.context.witness_speaking.beliefs.emotions['sympathy'] += 2
        self.context.witness_speaking.beliefs.emotions['confidence'] += 2
        self.context.witness_speaking.beliefs.emotions['sadness'] += 1

class EmpathyGenerationAltruisticMotiveRule(Rule):
    """ Rule to update the emotions of witness with the strategies Empathy generation and Altruistic motive"""
    def __init__(self, beliefs, context):
        super().__init__(beliefs, context)
    def match(self):
        strategy = self.context.get_ongoing_strategy()
        strategy = StrategiesOwnWitnesses(strategy) if self.context.witness_speaking.side else StrategiesOpposingWitnesses(strategy)
        return self.context.phase is Phase.witness_testimony and strategy == StrategiesOwnWitnesses.Empathy_generation_altruistic_motive
    def do(self):
        self.context.witness_speaking.beliefs.emotions['empathy'] += 2
        self.context.witness_speaking.beliefs.emotions['credibility'] += 2
        self.context.witness_speaking.beliefs.emotions['confidence'] += 2
        self.context.witness_speaking.beliefs.emotions['responsibility'] += 2
        self.context.witness_speaking.beliefs.emotions['hope'] += 2

# Function to perceive the world and update the beliefs and intentions 
def perceive_world_witness(witness : Witness):
    if witness.context.phase == Phase.witness_testimony:
        # List of emotions of own witness
        list_own_intentions = [np.array([2,2,1,-1,1,-1,0,1,1,2,1]), # Generate_sympathy
                               np.array([1,1,2,2,2,1,-1,2,0,0,0]), # Convince_jury
                               np.array([1,1,2,2,2,1,0,2,-1,-1,0]), #Provide_detailed_information
                               np.array([2,2,1,-1,1,1,0,-1,1,2,1]), #Show_vulnerability
                               np.array([2,1,1,1,1,2,0,1,0,-1,0])] #Strengthen_lawyer_narrative
        # List of emotions of opposing witness
        list_opposing_intentions = [np.array([2,2,1,-1,1,-1,0,1,1,2,1]), # Generate_sympathy
                                    np.array([1,1,2,2,2,1,-1,2,0,0,0]), # Convince_jury
                                    np.array([1,1,2,2,2,1,0,2,-1,-1,0]), #Provide_detailed_information
                                    np.array([2,2,1,-1,1,1,0,-1,1,2,1]), #Show_vulnerability
                                    np.array([-1,-2,0,-2,-1,-2,1,-1,2,0,2]), #Self_protection
                                    np.array([-2,-2,0,1,-1,0,2,-2,-1,-2,-2]), # Defend_aggressively
                                    np.array([1,1,1,1,1,1,-1,2,-2,-1,-1]), # Keep_calm_under_pressure
                                    np.array([0,-1,-1,-1,0,0,1,-1,2,1,1])] # Avoid_difficult_questions
        witness_emotions = np.array([witness.beliefs.emotions[emot] for emot in witness.beliefs.emotions])

        if witness.side:
            similarity = cosine_similarity([witness_emotions], np.array(list_own_intentions))
        else:
            similarity = cosine_similarity([witness_emotions], np.array(list_opposing_intentions))
        index = np.argmax(similarity)
        intention = map_intentions(index, witness.side)
        witness.intentions.dict[intention] = True
        witness.context.set_witness_intention(intention)

        # Save data of case
        witness.context.sequence_of_events += f'The witness had the intention of {intention.name}.\n'

