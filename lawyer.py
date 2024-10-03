from agent_methods import AgentInterface
from environment import SimulationContext, Phase
from utils import StrategiesOwnWitnesses, StrategiesOpposingWitnesses, LawyerDesires_Enum, LawyerIntentions_Enum, Rule
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
        self.rules = [SetWitnessRule(self.beliefs, self.context)]

    def perceive_world(self):
        return self.perceive_world_func(self)

    def execute_actions(self):
        return super().execute_actions()

# BDI Architecture
class LawyerBeliefs():
    def __init__(self, witnesses):
        self.witnesses_dict = {}
        for wit in witnesses:
            self.witnesses_dict[wit] = False

class LawyerDesires():
    def __init__(self):
        self.dict = {item : True for item in LawyerDesires_Enum}
class LawyerIntentions():
    def __init__(self):
        self.dict = {item : True for item in LawyerIntentions_Enum}

# RULES OF LAWYER
class SetWitnessRule(Rule):
    """ Rule to update the belief of the witness who is testifying"""
    def __init__(self, beliefs, context):
        super().__init__(beliefs, context)
    def match(self):
        return self.context.phase is Phase.aplication_strategies
    def do(self):
        for wit in self.beliefs.witnesses_dict:
            if self.beliefs.witnesses_dict[wit]: # If I find the witness who testified earlier, I put False in 'witnesses_dict'
                self.beliefs.witnesses_dict[wit] = False
            if wit == self.context.witness_speaking: # If I find the witness who is testifying, I put True in 'witnesses_dict'
                self.beliefs.witnesses_dict[wit] = True
                break

# Function to perceive the world and update the beliefs 
def perceive_world_lawyer(lawyer : Lawyer):
    for rule in lawyer.rules:
        if rule.match():
            rule.do()
        
    # Save data of case
    lawyer.context.sequence_of_events += 'The lawyer felt the ' + LawyerDesires_Enum.Desire_to_win_the_case.name + ' and had the ' + LawyerIntentions_Enum.Intention_to_apply_strategy.name + '.\n'

    