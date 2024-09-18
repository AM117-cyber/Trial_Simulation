from agent_methods import AgentInterface
from environment import SimulationContext, Phase
from utils import StrategiesOwnWitnesses, StrategiesOpposingWitnesses, LawyerDesires_Enum, LawyerIntentions_Enum
from witness import Witness
import numpy as np

class Lawyer(AgentInterface):
    def __init__(self, perceive_world_func, execute_action_func, witnesses):
        self.beliefs = LawyerBeliefs(witnesses)
        self.desires = LawyerDesires()
        self.intentions = LawyerIntentions()
        self.context = SimulationContext() 
        self.perceive_world_func = perceive_world_func
        self.execute_action_func = execute_action_func
        self.strategies = [StrategiesOwnWitnesses, StrategiesOpposingWitnesses]

    def perceive_world(self):
        return self.perceive_world_func(self)

    def execute_actions(self):
        return super().execute_actions()

    def apply_strategy(self, witness : Witness, strategy):
        strategy = StrategiesOwnWitnesses(strategy) if witness.side else StrategiesOpposingWitnesses(strategy)
        if strategy is StrategiesOwnWitnesses.Empathy_generation:
            witness.beliefs.emotions['empathy'] += 2
            witness.beliefs.emotions['sympathy'] += 2
            witness.beliefs.emotions['confidence'] += 2
            witness.beliefs.emotions['sadness'] += 1

        elif strategy is StrategiesOwnWitnesses.Empathy_generation_altruistic_motive:
            witness.beliefs.emotions['empathy'] += 2
            witness.beliefs.emotions['credibility'] += 2
            witness.beliefs.emotions['confidence'] += 2
            witness.beliefs.emotions['responsibility'] += 2
            witness.beliefs.emotions['hope'] += 2

        elif strategy is StrategiesOwnWitnesses.Chronological_clarity:
            witness.beliefs.emotions['credibility'] += 2
            witness.beliefs.emotions['calm'] += 2

        elif strategy is StrategiesOwnWitnesses.Chronological_clarity_detailed_observation:
            witness.beliefs.emotions['credibility'] += 2
            witness.beliefs.emotions['calm'] += 2
            if witness.ineptitude == 'High' or witness.education == 'Low':
                witness.beliefs.emotions['frustration'] += 2

        elif strategy is StrategiesOwnWitnesses.Reluctant_participation:
            witness.beliefs.emotions['responsibility'] += 2
            witness.beliefs.emotions['confidence'] -= 1
        
        elif strategy is StrategiesOpposingWitnesses.Memory_lapses:
            witness.beliefs.emotions['confusion'] += 2
            witness.beliefs.emotions['frustration'] += 2
            witness.beliefs.emotions['shame'] += 2
            witness.beliefs.emotions['credibility'] -= 2
            witness.beliefs.emotions['confidence'] -= 2

        elif strategy is StrategiesOpposingWitnesses.Biased_perspective:
            if witness.ineptitude == 'High' or witness.education == 'Low':
                witness.beliefs.emotions['frustration'] += 2
                witness.beliefs.emotions['calm'] -= 2
                witness.beliefs.emotions['shame'] += 2
            witness.beliefs.emotions['credibility'] -= 2

        elif strategy is StrategiesOpposingWitnesses.Motivational_doubts:
            witness.beliefs.emotions['shame'] += 2
            witness.beliefs.emotions['credibility'] -= 2
            witness.beliefs.emotions['confidence'] -= 2

        elif strategy is StrategiesOpposingWitnesses.Contradiction_trap:
            witness.beliefs.emotions['frustration'] += 2
            witness.beliefs.emotions['shame'] += 2
            witness.beliefs.emotions['anger'] += 2
            witness.beliefs.emotions['credibility'] -= 2
            witness.beliefs.emotions['confidence'] -= 2

        elif strategy is StrategiesOpposingWitnesses.Emotion_unreliability:
            witness.beliefs.emotions['sadness'] += 2
            witness.beliefs.emotions['frustration'] += 2
            witness.beliefs.emotions['shame'] += 2
            witness.beliefs.emotions['calm'] -= 2
            witness.beliefs.emotions['credibility'] -= 2
            witness.beliefs.emotions['confidence'] -= 2
        else:
            print('Invalid strategy') 

class LawyerBeliefs():
    def __init__(self, witnesses):
        self.witnesses = witnesses

class LawyerDesires():
    def __init__(self):
        self.dict = [[item, False] for item in LawyerDesires_Enum]
class LawyerIntentions():
    def __init__(self):
        self.dict = [[item, False] for item in LawyerIntentions_Enum]

def perceive_world_lawyer(lawyer : Lawyer):
    if lawyer.context.phase is Phase.aplication_strategies:
        strategy = lawyer.context.get_ongoing_strategy()
        is_own = lawyer.context.get_is_own_witness()
        reset_desires_intentions(lawyer)
        # Update desires
        desire = None
        if (strategy == 3 or strategy == 4) and is_own:
            lawyer.desires.dict[0][1] = True
            desire = lawyer.desires.dict[0][0]
        elif (strategy == 1 or strategy == 5) and is_own:
            lawyer.desires.dict[1][1] = True
            desire = lawyer.desires.dict[1][0]
        elif strategy == 2 and is_own:
            lawyer.desires.dict[2][1] = True
            desire = lawyer.desires.dict[2][0]

        elif strategy == 5 and not is_own:
            lawyer.desires.dict[3][1] = True
            desire = lawyer.desires.dict[3][0]
        elif (strategy == 1 or strategy == 4) and not is_own:
            lawyer.desires.dict[4][1] = True
            desire = lawyer.desires.dict[4][0]
        elif strategy == 3 and not is_own:
            lawyer.desires.dict[5][1] = True
            desire = lawyer.desires.dict[5][0]
        elif strategy == 2 and not is_own:
            lawyer.desires.dict[6][1] = True
            desire = lawyer.desires.dict[6][0]

        # Update intentions
        intention = None
        if lawyer.desires.dict[2][1] and is_own:
            lawyer.intentions.dict[0][1] = True
            intention = lawyer.intentions.dict[0][0]
        elif lawyer.desires.dict[0][1] and is_own:
            lawyer.intentions.dict[1][1] = True
            intention = lawyer.intentions.dict[1][0]
        elif lawyer.desires.dict[1][1] and is_own:
            x = np.random.choice([0,2])
            lawyer.intentions.dict[x][1] = True
            intention = lawyer.intentions.dict[x][0]

        elif (lawyer.desires.dict[4][1] or lawyer.desires.dict[6][1]) and not is_own:
            lawyer.intentions.dict[3][1] = True
            intention = lawyer.intentions.dict[3][0]
        elif lawyer.desires.dict[5][1] and not is_own:
            lawyer.intentions.dict[4][1] = True
            intention = lawyer.intentions.dict[4][0]
        elif lawyer.desires.dict[3][1] and not is_own:
            lawyer.intentions.dict[5][1] = True
            intention = lawyer.intentions.dict[5][0]
        
        # Save data of case
        lawyer.context.sequence_of_events += 'The lawyer felt the ' + desire.name + ' and had the ' + intention.name + '.\n'

def reset_desires_intentions(lawyer : Lawyer):
    for desire in lawyer.desires.dict:
        desire[1] = False
    for intention in lawyer.intentions.dict:
        intention[1] = False
    