import numpy as np
from experta import *
from sklearn.metrics.pairwise import cosine_similarity
from utils import map_features

# Definición de Hechos
class JurorExpSys(Fact):
    """Información sobre el jurado."""
    openness = Field(str, default="")
    extraversion = Field(str, default="")
    agreeableness = Field(str, default="")
    conscientiousness = Field(str, default="")
    neuroticism = Field(str, default="")
    locus_of_control = Field(str, default="")
    value_emotional_exp = Field(str, default="")
    takes_risks = Field(str, default="")
    takes_decisions_by_fear = Field(str, default="")
    socioeconomic_status = Field(str, default="")

# Motor de Inferencia (Reglas)
class JurorIdentificator(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.role = None

    @Rule(JurorExpSys(openness="Middle", extraversion="High", agreeableness="Middle", conscientiousness="High", neuroticism="Middle", 
                      locus_of_control="Internal", value_emotional_exp="Low", takes_risks="High", takes_decisions_by_fear="Low", 
                      socioeconomic_status="High")) # rule1
    def is_leader(self):
        self.role = "Leader"

    @Rule(JurorExpSys(openness="Middle", extraversion="Low", agreeableness="High", conscientiousness="Middle", neuroticism="Middle", 
                      locus_of_control="External", value_emotional_exp="Middle", takes_risks="Low", takes_decisions_by_fear="High", 
                      socioeconomic_status="Middle")) # rule2
    def is_follower(self):
        self.role = "Follower"
    
    @Rule(JurorExpSys(openness="High", extraversion="Middle", agreeableness="Middle", conscientiousness="Middle", neuroticism="Middle", 
                      locus_of_control="External", value_emotional_exp="Middle", takes_risks="Middle", takes_decisions_by_fear="Middle", 
                      socioeconomic_status="Middle")) # rule3
    def is_filler(self):
        self.role = "Filler"

    @Rule(JurorExpSys(openness="High", extraversion="High", agreeableness="High", conscientiousness="High", neuroticism="Middle", 
                      locus_of_control="Internal", value_emotional_exp="Low", takes_risks="Middle", takes_decisions_by_fear="Middle", 
                      socioeconomic_status="High")) # rule4
    def is_negotiator(self):
        self.role = "Negotiator"

    @Rule(JurorExpSys(openness="Low", extraversion="Middle", agreeableness="Middle", conscientiousness="Middle", neuroticism="High", 
                      locus_of_control="Internal", value_emotional_exp="Middle", takes_risks="High", takes_decisions_by_fear="Low", 
                      socioeconomic_status="High")) # rule5
    def is_holdout(self):
        self.role = "Holdout"

    @Rule(AS.fact << JurorExpSys())
    def unknown_role(self, fact):
        if(self.role == None):
            # Predefined features for each role of jury
            leader_features = np.array([4,9,6,8,4,9,2,8,3,8])
            follower_features = np.array([5,3,8,4,5,2,5,2,8,4])
            filler_features = np.array([7,4,5,4,5,5,5,4,5,5])
            negotiator_features = np.array([7,7,8,8,4,7,3,6,4,7])
            holdout_features = np.array([3,6,4,6,8,5,5,8,2,8])

            current_features = [fact[f] for f in fact][:10]
            current_features = np.array([map_features(elem) for elem in current_features])
            similarity = cosine_similarity([current_features], np.array([leader_features, follower_features, filler_features, negotiator_features,
                                                                    holdout_features]))
            
            index = np.argmax(similarity)
            self.role = map_features(index)
        
class ExpertSystem:
    def __init__(self, juror):
        self.role = None

        # Ejecución del Motor
        identificator = JurorIdentificator()
        identificator.reset()  # Restablecer el motor de inferencia
        identificator.declare(JurorExpSys(openness=juror.openness, extraversion=juror.extraversion, agreeableness=juror.agreeableness, 
                                          conscientiousness=juror.conscientiousness, neuroticism=juror.neuroticism, 
                                          locus_of_control=juror.locus_of_control, value_emotional_exp=juror.value_emotional_exp, 
                                          takes_risks=juror.takes_risks, takes_decisions_by_fear=juror.takes_decisions_by_fear, 
                                          socioeconomic_status=juror.socioeconomic_status))
        identificator.run()  # Ejecutar el motor
        self.role = identificator.role

