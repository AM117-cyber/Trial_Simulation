from agent_methods import AgentInterface
from environment import SimulationContext
from utils import StrategiesOwnWitnesses, StrategiesOpposingWitnesses

class Lawyer(AgentInterface):
    def __init__(self, perceive_world_func, execute_action_func):
        self.beliefs = LawyerBeliefs()
        self.desires = LawyerDesires()
        self.intentions = LawyerIntentions()
        self.context = SimulationContext()
        self.perceive_world_func = perceive_world_func
        self.execute_action_func = execute_action_func
        self.strategies = [StrategiesOwnWitnesses, StrategiesOpposingWitnesses]

    def perceive_world(self):
        return super().perceive_world()

    def execute_action(self):
        return super().execute_action()

    def apply_strategy(self, witness, strategy):
        if strategy == 'empathy generation':
            witness.emotions['empathy'] += 2
            witness.emotions['sympathy'] += 2
            witness.emotions['confidence'] += 2
            witness.emotions['sadness'] += 1

        elif strategy == 'empathy generation & altruistic motive':
            witness.emotions['empathy'] += 2
            witness.emotions['character'] += 2
            witness.emotions['confidence'] += 2
            witness.emotions['responsibility'] += 2
            witness.emotions['hope'] += 2
            witness.emotions['compassion'] += 2

        elif strategy == 'chronological clarity':
            witness.emotions['credibility'] += 2
            witness.emotions['coherence'] += 2
            witness.emotions['calm'] += 2
            if witness.ineptitude == 'high' or witness.education == 'low':
                witness.emotions['confusion'] += 2

        elif strategy == 'chronological clarity & detailed observation':
            witness.emotions['credibility'] += 2
            witness.emotions['coherence'] += 2
            witness.emotions['calm'] += 2
            if witness.ineptitude == 'high' or witness.education == 'low':
                witness.emotions['confusion'] += 2
                witness.emotions['frustration'] += 2
                witness.emotions['anxiety'] += 2

        elif strategy == 'reluctant participation':
            witness.emotions['responsibility'] += 2
            witness.emotions['doubt'] += 2
        
        elif strategy == 'memory lapses':
            witness.emotions['doubt'] += 2
            witness.emotions['frustration'] += 2
            witness.emotions['anxiety'] += 2
            witness.emotions['shame'] += 2
            witness.emotions['credibility'] -= 2
            witness.emotions['confidence'] -= 2

        elif strategy == 'biased perspective':
            witness.emotions['doubt'] += 2
            if witness.ineptitude == 'high' or witness.education == 'low':
                witness.emotions['frustration'] += 2
                witness.emotions['anger'] += 2
                witness.emotions['shame'] += 2
            witness.emotions['credibility'] -= 2

        elif strategy == 'motivational doubts':
            witness.emotions['doubt'] += 2
            witness.emotions['shame'] += 2
            witness.emotions['credibility'] -= 2
            witness.emotions['confidence'] -= 2

        elif strategy == 'contradiction trap':
            witness.emotions['confunsion'] += 2
            witness.emotions['frustration'] += 2
            witness.emotions['anxiety'] += 2
            witness.emotions['shame'] += 2
            witness.emotions['anger'] += 2
            witness.emotions['credibility'] -= 2
            witness.emotions['confidence'] -= 2

        elif strategy == 'emotion unreliability':
            witness.emotions['sadness'] += 2
            witness.emotions['frustration'] += 2
            witness.emotions['anxiety'] += 2
            witness.emotions['shame'] += 2
            witness.emotions['anger'] += 2
            witness.emotions['credibility'] -= 2
            witness.emotions['confidence'] -= 2

        else:
            print('Invalid strategy') 

class LawyerBeliefs():
    def __init__(self):
        pass

class LawyerDesires():
    def __init__(self):
        pass

class LawyerIntentions():
    def __init__(self):
        pass