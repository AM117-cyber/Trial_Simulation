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
        self.rules = [GenerateEmpathyRule(self.beliefs, self.context), EmpathyGenerationAltruisticMotiveRule(self.beliefs, self.context), 
                      ChronologicalClarityRule(self.beliefs, self.context), ChronologicalClarityDetailedObservationRule1(self.beliefs, self.context), 
                      ChronologicalClarityDetailedObservationRule2(self.beliefs, self.context), ReluctantParticipationRule(self.beliefs, self.context), 
                      MemoryLapsesRule(self.beliefs, self.context), BiasedPerspectiveRule1(self.beliefs, self.context), BiasedPerspectiveRule2(self.beliefs, self.context), 
                      MotivationalDoubtsRule(self.beliefs, self.context), ContradictionTrapRule(self.beliefs, self.context), EmotionUnreliabilityRule(self.beliefs, self.context)]
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
        return self.execute_action_func(self)

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
        strategy = self.context.witness_speaking.side
        strategy = StrategiesOwnWitnesses(strategy) if strategy else StrategiesOpposingWitnesses(strategy)
        return self.context.phase is Phase.witness_testimony and strategy == StrategiesOwnWitnesses.Empathy_generation
    def do(self):
        self.context.witness_speaking.beliefs.emotions['empathy'] += 2
        self.context.witness_speaking.beliefs.emotions['sympathy'] += 2
        self.context.witness_speaking.beliefs.emotions['confidence'] += 2
        self.context.witness_speaking.beliefs.emotions['sadness'] += 1
        # Save data of case
        self.context.sequence_of_events += f'''The witness being questioned is witness number {self.context.witness_speaking.id}, 
                                            on behalf of the lawyer, who due to the strategy applied by the lawyer increased his 
                                            emotions, such as: empathy, sympathy, confidence and sadness.\n'''

class EmpathyGenerationAltruisticMotiveRule(Rule):
    """ Rule to update the emotions of witness with the strategies Empathy generation and Altruistic motive"""
    def __init__(self, beliefs, context):
        super().__init__(beliefs, context)
    def match(self):
        strategy = self.context.witness_speaking.side
        strategy = StrategiesOwnWitnesses(strategy) if strategy else StrategiesOpposingWitnesses(strategy)
        return self.context.phase is Phase.witness_testimony and strategy == StrategiesOwnWitnesses.Empathy_generation_altruistic_motive
    def do(self):
        self.context.witness_speaking.beliefs.emotions['empathy'] += 2
        self.context.witness_speaking.beliefs.emotions['credibility'] += 2
        self.context.witness_speaking.beliefs.emotions['confidence'] += 2
        self.context.witness_speaking.beliefs.emotions['responsibility'] += 2
        self.context.witness_speaking.beliefs.emotions['hope'] += 2
        # Save data of case
        self.context.sequence_of_events += f'''The witness being questioned is witness number {self.context.witness_speaking.id}, 
                                            on behalf of the lawyer, who due to the strategy applied by the lawyer increased his 
                                            emotions, such as: empathy, credibility, confidence, responsibility and hope.\n'''

class ChronologicalClarityRule(Rule):
    """ Rule to update the emotions of witness with the strategy Chronological clarity"""
    def __init__(self, beliefs, context):
        super().__init__(beliefs, context)
    def match(self):
        strategy = self.context.witness_speaking.side
        strategy = StrategiesOwnWitnesses(strategy) if strategy else StrategiesOpposingWitnesses(strategy)
        return self.context.phase is Phase.witness_testimony and strategy == StrategiesOwnWitnesses.Chronological_clarity
    def do(self):
        self.context.witness_speaking.beliefs.emotions['credibility'] += 2
        self.context.witness_speaking.beliefs.emotions['calm'] += 2
        # Save data of case
        self.context.sequence_of_events += f'''The witness being questioned is witness number {self.context.witness_speaking.id}, 
                                            on behalf of the lawyer, who due to the strategy applied by the lawyer increased his 
                                            emotions, such as: credibility and calm.\n'''

class ChronologicalClarityDetailedObservationRule1(Rule):
    """ Rule to update the emotions of witness with the strategies Chronological clarity and Detailed observation"""
    def __init__(self, beliefs, context):
        super().__init__(beliefs, context)
    def match(self):
        strategy = self.context.witness_speaking.side
        strategy = StrategiesOwnWitnesses(strategy) if strategy else StrategiesOpposingWitnesses(strategy)
        return self.context.phase is Phase.witness_testimony and strategy == StrategiesOwnWitnesses.Chronological_clarity_detailed_observation
    def do(self):
        self.context.witness_speaking.beliefs.emotions['credibility'] += 2
        self.context.witness_speaking.beliefs.emotions['calm'] += 2
        # Save data of case
        self.context.sequence_of_events += f'''The witness being questioned is witness number {self.context.witness_speaking.id}, 
                                            on behalf of the lawyer, who due to the strategy applied by the lawyer increased his 
                                            emotions, such as: credibility and calm.\n'''

class ChronologicalClarityDetailedObservationRule2(Rule):
    """ Rule to update the emotions of witness with the strategies Chronological clarity and Detailed observation"""
    def __init__(self, beliefs, context):
        super().__init__(beliefs, context)
    def match(self):
        strategy = self.context.witness_speaking.side
        strategy = StrategiesOwnWitnesses(strategy) if strategy else StrategiesOpposingWitnesses(strategy)
        return self.context.phase is Phase.witness_testimony and strategy == StrategiesOwnWitnesses.Chronological_clarity_detailed_observation \
               and  (self.context.witness_speaking.ineptitude == 'High' or self.context.witness_speaking.education == 'Low')
    def do(self):
        self.context.witness_speaking.beliefs.emotions['frustration'] += 2
        # Save data of case
        self.context.sequence_of_events += f'''The witness being questioned is witness number {self.context.witness_speaking.id}, 
                                            on behalf of the lawyer, who due to the strategy applied by the lawyer increased his 
                                            emotions, such as: frustration.\n'''

class ReluctantParticipationRule(Rule):
    """ Rule to update the emotions of witness with the strategy Reluctant participation"""
    def __init__(self, beliefs, context):
        super().__init__(beliefs, context)
    def match(self):
        strategy = self.context.witness_speaking.side
        strategy = StrategiesOwnWitnesses(strategy) if strategy else StrategiesOpposingWitnesses(strategy)
        return self.context.phase is Phase.witness_testimony and strategy == StrategiesOwnWitnesses.Reluctant_participation 
    def do(self):
        self.context.witness_speaking.beliefs.emotions['responsibility'] += 2
        self.context.witness_speaking.beliefs.emotions['confidence'] -= 1
        # Save data of case
        self.context.sequence_of_events += f'''The witness being questioned is witness number {self.context.witness_speaking.id}, 
                                            on behalf of the lawyer, who due to the strategy applied by the lawyer increased his 
                                            emotions, such as: responsibility; and decreased his emotions, such as: confidence.\n'''

class MemoryLapsesRule(Rule):
    """ Rule to update the emotions of witness with the strategy Memory lapses"""
    def __init__(self, beliefs, context):
        super().__init__(beliefs, context)
    def match(self):
        strategy = self.context.witness_speaking.side
        strategy = StrategiesOwnWitnesses(strategy) if strategy else StrategiesOpposingWitnesses(strategy)
        return self.context.phase is Phase.witness_testimony and strategy == StrategiesOpposingWitnesses.Memory_lapses 
    def do(self):
        self.context.witness_speaking.beliefs.emotions['confusion'] += 2
        self.context.witness_speaking.beliefs.emotions['frustration'] += 2
        self.context.witness_speaking.beliefs.emotions['shame'] += 2
        self.context.witness_speaking.beliefs.emotions['credibility'] -= 2
        self.context.witness_speaking.beliefs.emotions['confidence'] -= 2
        # Save data of case
        self.context.sequence_of_events += f'''The witness being questioned is witness number {self.context.witness_speaking.id}, 
                                            against the lawyer, who due to the strategy applied by the lawyer increased his 
                                            emotions, such as: confusion, frustration and shame; and decreased his emotions, such as: 
                                            credibility and confidence.\n'''

class BiasedPerspectiveRule1(Rule):
    """ Rule to update the emotions of witness with the strategy Biased perspective"""
    def __init__(self, beliefs, context):
        super().__init__(beliefs, context)
    def match(self):
        strategy = self.context.witness_speaking.side
        strategy = StrategiesOwnWitnesses(strategy) if strategy else StrategiesOpposingWitnesses(strategy)
        return self.context.phase is Phase.witness_testimony and strategy == StrategiesOpposingWitnesses.Biased_perspective 
    def do(self):
        self.context.witness_speaking.beliefs.emotions['credibility'] -= 2
        # Save data of case
        self.context.sequence_of_events += f'''The witness being questioned is witness number {self.context.witness_speaking.id}, 
                                            against the lawyer, who due to the strategy applied by the lawyer decreased his emotions, 
                                            such as: credibility.\n'''

class BiasedPerspectiveRule2(Rule):
    """ Rule to update the emotions of witness with the strategy Biased perspective"""
    def __init__(self, beliefs, context):
        super().__init__(beliefs, context)
    def match(self):
        strategy = self.context.witness_speaking.side
        strategy = StrategiesOwnWitnesses(strategy) if strategy else StrategiesOpposingWitnesses(strategy)
        return self.context.phase is Phase.witness_testimony and strategy == StrategiesOpposingWitnesses.Biased_perspective \
               and  (self.context.witness_speaking.ineptitude == 'High' or self.context.witness_speaking.education == 'Low')
    def do(self):
        self.context.witness_speaking.beliefs.emotions['frustration'] += 2
        self.context.witness_speaking.beliefs.emotions['calm'] -= 2
        self.context.witness_speaking.beliefs.emotions['shame'] += 2
        # Save data of case
        self.context.sequence_of_events += f'''The witness being questioned is witness number {self.context.witness_speaking.id}, 
                                            against the lawyer, who due to the strategy applied by the lawyer increased his 
                                            emotions, such as: frustration and shame; and decreased his emotions, such as: calm.\n'''

class MotivationalDoubtsRule(Rule):
    """ Rule to update the emotions of witness with the strategy Motivational doubts"""
    def __init__(self, beliefs, context):
        super().__init__(beliefs, context)
    def match(self):
        strategy = self.context.witness_speaking.side
        strategy = StrategiesOwnWitnesses(strategy) if strategy else StrategiesOpposingWitnesses(strategy)
        return self.context.phase is Phase.witness_testimony and strategy == StrategiesOpposingWitnesses.Motivational_doubts 
    def do(self):
        self.context.witness_speaking.beliefs.emotions['shame'] += 2
        self.context.witness_speaking.beliefs.emotions['credibility'] -= 2
        self.context.witness_speaking.beliefs.emotions['confidence'] -= 2
        # Save data of case
        self.context.sequence_of_events += f'''The witness being questioned is witness number {self.context.witness_speaking.id}, 
                                            against the lawyer, who due to the strategy applied by the lawyer increased his 
                                            emotions, such as: shame; and decreased his emotions, such as: credibility and confidence.\n'''

class ContradictionTrapRule(Rule):
    """ Rule to update the emotions of witness with the strategy Contradiction trap"""
    def __init__(self, beliefs, context):
        super().__init__(beliefs, context)
    def match(self):
        strategy = self.context.witness_speaking.side
        strategy = StrategiesOwnWitnesses(strategy) if strategy else StrategiesOpposingWitnesses(strategy)
        return self.context.phase is Phase.witness_testimony and strategy == StrategiesOpposingWitnesses.Contradiction_trap 
    def do(self):
        self.context.witness_speaking.beliefs.emotions['frustration'] += 2
        self.context.witness_speaking.beliefs.emotions['shame'] += 2
        self.context.witness_speaking.beliefs.emotions['anger'] += 2
        self.context.witness_speaking.beliefs.emotions['credibility'] -= 2
        self.context.witness_speaking.beliefs.emotions['confidence'] -= 2
        # Save data of case
        self.context.sequence_of_events += f'''The witness being questioned is witness number {self.context.witness_speaking.id}, 
                                            against the lawyer, who due to the strategy applied by the lawyer increased his 
                                            emotions, such as: anger, frustration and shame; and decreased his emotions, such as: 
                                            credibility and confidence.\n'''

class EmotionUnreliabilityRule(Rule):
    """ Rule to update the emotions of witness with the strategy Emotion unreliability"""
    def __init__(self, beliefs, context):
        super().__init__(beliefs, context)
    def match(self):
        strategy = self.context.witness_speaking.side
        strategy = StrategiesOwnWitnesses(strategy) if strategy else StrategiesOpposingWitnesses(strategy)
        return self.context.phase is Phase.witness_testimony and strategy == StrategiesOpposingWitnesses.Emotion_unreliability 
    def do(self):
        self.context.witness_speaking.beliefs.emotions['sadness'] += 2
        self.context.witness_speaking.beliefs.emotions['frustration'] += 2
        self.context.witness_speaking.beliefs.emotions['shame'] += 2
        self.context.witness_speaking.beliefs.emotions['calm'] -= 2
        self.context.witness_speaking.beliefs.emotions['credibility'] -= 2
        self.context.witness_speaking.beliefs.emotions['confidence'] -= 2
        # Save data of case
        self.context.sequence_of_events += f'''The witness being questioned is witness number {self.context.witness_speaking.id}, 
                                            against the lawyer, who due to the strategy applied by the lawyer increased his 
                                            emotions, such as: sadness, frustration and shame; and decreased his emotions, such as: 
                                            credibility, confidence and calm.\n'''

# Function to perceive the world and update the beliefs and intentions
def perceive_world_witness(witness : Witness):
    for rule in witness.rules:
        if rule.match():
            rule.do()

def execute_actions_witness(witness : Witness):
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

