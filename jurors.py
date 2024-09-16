# # juror profile
# # (High or Low)
# # Openness
# # Conscientiousness
# # Extraversion
# # Agreeableness
# # Neuroticism
# # locus_of_control
# # social_norms
# # value_emotional_exp
# # takes_risks
# # takes_decisions_by_fear
# # bias
# # Demographic factors such as:  Age, gender, race, socioeconomic status (if you are similar to a person might be more relatable)
# # Beliefs:
# # facts{} fact, (relevance, veracity)
# # testimony impressions [] as testimonies have an id starting from 0 then the list in position i contains the ith testimony
# # verdict (guilty or not guilty)
# import random
# from utils import Gender, Phase, Roles, S_Status, Trait_Level,Veracity, Vote
# from collections import Counter


# class JurorBeliefs():
#     def __init__(self, openness, conscientiousness, extraversion, agreeableness, neuroticism, locus_of_control, social_norms, value_emotional_exp, takes_risks, takes_decisions_by_fear, bias, age, gender, race, socioeconomic_status, facts):
#         self.openness = openness
#         self.conscientiousness = conscientiousness
#         self.extraversion = extraversion
#         self.agreeableness = agreeableness
#         self.neuroticism = neuroticism
#         self.locus_of_control = locus_of_control
#         self.social_norms = social_norms
#         self.value_emotional_exp = value_emotional_exp
#         self.takes_risks = takes_risks
#         self.takes_decisions_by_fear = takes_decisions_by_fear
#         self.bias = bias
#         self.age = age
#         self.gender = gender
#         self.race = race
#         self.facts_with_discrepancy_value = {}
#         self.socioeconomic_status = socioeconomic_status
#         self.facts = facts
#         self.jurors_that_have_talked = 0
#         self.majority_beliefs = {}


# class Desires():
#     def __init__(self):
#         self.listen_testimonies = True
#         self.participate_in_info_pooling = False
#         self.lie = False
#         self.debate = False


# class Juror:
#     def __init__(self, id, beliefs: JurorBeliefs,total_jurors_amount):
#         self.id = id
#         self.verdict = None
#         self.role = None
#         self.beliefs = beliefs
#         self.desires = Desires()
#         self.other_jurors_beliefs = {}
#         self.total_jurors_amount = total_jurors_amount

#     def confidence_level(self):
#         return sum(abs(value[1]) for value in self.beliefs.facts.values())

#     def share_veracity_beliefs(self, jury):
#          """Sends a message containing this juror's beliefs about fact veracity and testimony impressions to the jurors on the list jury."""


#     def calculate_influence(self, sender_juror, perssuassion_strategy):
#         influence = 0
#         if sender_juror.role is Roles.leader:
#             if self.role is Roles.holdout:
#                 influence +=1
#             elif self.role is Roles.leader:
#                 influence +=5
#             elif self.role is Roles.negotiator:
#                 influence += 7
#             else:
#                 influence += 12
#         if sender_juror.role is Roles.negotiator:
#             influence +=8
#         if self.agreeableness is Trait_Level.high:
#             influence+=5
#         return influence
    
#     def execute_action(self):
#         if self.desires.participate_in_info_pooling:
#             if self.desires.lie:
#                 return self.beliefs.majority_beliefs
#             else:
#                 beliefs = get_facts_in_format(self.beliefs.facts)
#                 return beliefs
#         # how do I know what's the opinion I'll lie about?

#     def perceive_world(self, info):
#         """método con el que los agentes perciben el mundo"""
#         result = None
#         # En dependencia de en qué fase estés la información que te interesa es diferente, por lo tanto percibes cosas diferentes
#         if self.desires.participate_in_info_pooling:
#             if not self.turn_to_speak:
#                 self.beliefs.jurors_that_have_talked = info.jurors_that_have_talked
#                 # aquí definimos cómo se percibe el mensaje que en este caso son los veracity beliefs del juror remitente
#                 self.other_jurors_beliefs[info.sender_juror] = info.message.case_beliefs #falta evaluate discern level
#             else:
#                 self.beliefs.jurors_that_have_talked = info.jurors_that_have_talked
#                 discrepancy_by_fact = self.get_discrepancy_by_fact()
#                 self.beliefs.facts_with_discrepancy_value = discrepancy_by_fact
#                 for fact in discrepancy_by_fact.keys():
#                     value = discrepancy_by_fact[fact][1] / self.total_jurors_amount
#                     if value >= 0.83: # if 83% similar opinion and different from mine. Opinions are high, uncertain or low
#                         self.beliefs.majority_beliefs[fact] = discrepancy_by_fact[fact]
#                         self.desires.lie = True
#                     else:
#                         if self.beliefs.facts[fact][1] < -15:
#                             self.beliefs.majority_beliefs[fact] = [Veracity.LOW,0]
#                         elif self.beliefs.facts[fact][1] > -15:
#                             self.beliefs.majority_beliefs[fact] = [Veracity.HIGH,0]
#                         else:
#                             self.beliefs.majority_beliefs[fact] = [Veracity.UNCERTAIN,0]
                  
#                 result = self.execute_action() #define qué va a responder ante el llamado del foreperson
                
#             return result
#         # si lie está activado voy a tratar mis beliefs como las mentiras que voy a promulgar, al menos hasta que se deje de cumplir la condición de la opinión de la mayoría

#         if self.desires.debate:
#             # decide how the message influences me
#             influence = self.calculate_influence(info.sender_juror, info.perssuassion_strategy)
#             for fact in info.beliefs_debated.keys():
#                 if  info.beliefs_debated[fact][0].value < self.beliefs.facts[fact][1]:
#                     self.beliefs.facts[fact][1] -= influence
#                 else:
#                     self.beliefs.facts[fact][1] += influence
#                     if self.beliefs.facts[fact][1] >= -15 and self.beliefs.facts[fact][1] <=15:
#                        self.beliefs.facts[fact][1] += 5 # si no estás muy seguro la influencia es mayor 
#             # my beliefs have been updated
#             discrepancy_by_fact = self.get_discrepancy_by_fact()
#             self.beliefs.facts_with_discrepancy_value = discrepancy_by_fact
#             result = 0
#             for fact in discrepancy_by_fact.keys():
#                 result += discrepancy_by_fact[fact][1] * abs(self.beliefs.facts[fact][1])
#             return result
#             # return my discrepancy value 
#             # if I am lying my discrepancy value is with self.beliefs.majority_beliefs[1]
#             # as the sum of discrepancies' values

    
        

#     def get_discrepancy_by_fact(self):


#         facts_with_discrepancy_value = {}
    
#         for fact in set(fact for beliefs in self.other_jurors_beliefs.values() for fact in beliefs):
#             # Count occurrences of each veracity for this fact across all jurors except the given one
#             veracity_counts = Counter(belief[fact] for name, belief in self.other_jurors_beliefs.items())
        
#             # Find the most common veracity
#             most_common_veracity = veracity_counts.most_common(1)[0]

#             if most_common_veracity[0] != self.beliefs.facts[fact]:
#                     self.beliefs.facts_with_discrepancy_value[fact] = most_common_veracity
    
#         return facts_with_discrepancy_value

#     def vote(self):
#         value = 0
#         for fact in self.beliefs.facts.keys():
#             value += self.beliefs.facts[fact][0] * self.beliefs.facts[fact][1]
#         if value <0:
#             return Vote.guilty
#         return Vote.not_guilty

# def get_facts_in_format(fact_dict):
#     """
#     Convert a dictionary of facts with relevance and veracity scores to a dictionary with Veracity enums.

#     Args:
#         fact_dict (dict): Dictionary where keys are fact names and values are lists [relevance, veracity].

#     Returns:
#         dict: Dictionary where keys are fact names and values are Veracity enums.
#     """
#     converted_dict = {}

#     for fact, scores in fact_dict.items():
#         _, veracity_score = scores  # Assuming the second element is the veracity score
        
#         if veracity_score < -15:
#             converted_dict[fact] = Veracity.LOW
#         elif veracity_score > 15:
#             converted_dict[fact] = Veracity.HIGH
#         else:
#             converted_dict[fact] = Veracity.UNCERTAIN

#     return converted_dict



# def set_foreperson(jury):
#     foreperson_value = 0
#     curr_foreperson = None
#     for juror in jury:
#         value = 0
#         if juror.role is Roles.leader:
#             value += 2
#         if juror.extraversion is Trait_Level.high:
#             value += 1
#         if juror.gender is Gender.male:
#             gender_bias = random.randint(0, 2)
#             if gender_bias:
#                 value += 0.5
#         if (juror.socioeconomic_status is S_Status.high) or (juror.socioeconomic_status is S_Status.medium):
#             value +=1
#         if juror.age >= average_age(jury):
#             value += 1.5
#         if value >= foreperson_value:
#             foreperson_value = value
#             curr_foreperson = juror
#     return curr_foreperson

# def average_age(jury):
#     age_sum = 0
#     for juror in jury:
#         age_sum += juror.age
#     return age_sum/len(jury)


# def order_for_info_pooling(jurors):
#     return sorted(jurors, key=lambda juror: (juror.confidence_level(), juror.beliefs.extraversion, juror.beliefs.openness), reverse=True)
            
            
        
        
            