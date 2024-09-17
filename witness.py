from agent_methods import AgentInterface
from environment import SimulationContext

class Witness(AgentInterface):
    def __init__(self, id, perceive_world_func, execute_action_func, facts, age, socioeconomic_status, education, ineptitude):
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
        self.emotions = {
            "empathy": 0, # empatia
            "sympathy": 0, # simpatia
            "credibility": 0, # credibilidad
            "confidence": 0, # confianza
            "responsability": 0, # responsabilidad 
            "hope" : 0, # esperanza
            "frustration": 0, # frustracion
            "calm": 0, # calma 
            "fear": 0, # miedo
            "sadness": 0, # tristeza
            "shame": 0, # verguenza
        }

    def perceive_world(self):
        return super().perceive_world()

    def execute_action(self):
        return super().execute_action()
    
class WitnessBeliefs():
    def __init__(self):
        pass

class WitnessDesires():
    def __init__(self):
        pass

class WitnessIntentions():
    def __init__(self):
        pass













# ----------------------------------------------------------------------------------------------
# "empathy": 0, # empatia
#             "sympathy": 0, # simpatia
#             "credibility": 0, # credibilidad
#             # "coherence": 0, # coherencia 
#             "confidence": 0, # confianza
#             # "character" : 0, # caracter
#             "responsability": 0, # responsabilidad 
#             "hope" : 0, # esperanza
#             # "confusion": 0, # confusion
#             # "anger": 0, # ira 
#             "frustration": 0, # frustracion
#             # "doubt": 0, # duda
#             "calm": 0, # calma 
#             "fear": 0, # miedo
#             # "anxiety": 0, # ansiedad
#             "sadness": 0, # tristeza
#             "shame": 0, # verguenza
#             # "compassion": 0 # compasion