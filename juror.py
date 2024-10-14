# RULES OF JUROR
import random
from agent_methods import AgentInterface, adjust_others_beliefs_general, get_common_belief_different_from_yours, get_esteem_for_someone, get_fact_disagreement, get_facts_in_format, get_most_relevant_fact, get_other_juror_belief_with_discrepancy, share_beliefs_general, update_veracity
from environment import SimulationContext
from utils import Juror_desires, Message, Phase, Roles, Rule, Rule_mine, Trait_Level, Veracity

class JurorBeliefs():
    def __init__(self, facts):

        self.facts = get_facts_in_format(facts)
        self.facts_with_value = facts
        self.other_jurors_beliefs = {}
        self.majority_opinion = None
        self.esteem_for_others = {}
        self.juror_to_support = None
        self.juror_to_contradict = None
        self.confidence_on_most_relevant_fact = 0

class Juror(AgentInterface):
    def __init__(self,perceive_world_func,execute_action_func, assert_rules, generate_desires_rules, vote_function, id, openness, conscientiousness, extraversion, agreeableness, neuroticism, locus_of_control, social_norms, value_emotional_exp, takes_risks, takes_decisions_by_fear, bias, age, gender, race, socioeconomic_status,beliefs):
        self.context = SimulationContext()
        self.id = id
        self.beliefs = beliefs
        self.desires = {Juror_desires.Support_a_jurors_beliefs: 0} # inicializar restantes
        self.assert_rules = assert_rules
        self.generate_desires_rules = generate_desires_rules
        self.openness = openness
        self.conscientiousness = conscientiousness
        self.extraversion = extraversion
        self.agreeableness = agreeableness
        self.neuroticism = neuroticism
        self.locus_of_control = locus_of_control
        self.social_norms = social_norms
        self.value_emotional_exp = value_emotional_exp
        self.takes_risks = takes_risks
        self.takes_decisions_by_fear = takes_decisions_by_fear
        self.bias = bias
        self.gender = gender
        self.age = age
        self.race = race
        self.socioeconomic_status = socioeconomic_status
        self.perceive_world_func = perceive_world_func
        self.execute_action_func = execute_action_func
        self.is_foreperson = False
        self.role = None
        self.most_relevant_fact = None
        self.juror_to_interact_with = None
        self.vote_function = vote_function

    def confidence_level(self, facts):
        return sum(abs(level.veracity) for level in facts.values())

    def update_facts_level(self, value, fact):
        if value < -15:
            self.beliefs.facts[fact] = Veracity.LOW
        elif value > 15:
            self.beliefs.facts[fact] = Veracity.HIGH
        else:
            self.beliefs.facts[fact] = Veracity.UNCERTAIN

    def perceive_world(self):
        return self.perceive_world_func(self)
        
    def execute_actions(self,strength):
        return self.execute_action_func(self,strength)
    
    def vote(self):
        return self.vote_function(self)
    
    
class Rule1(Rule_mine):
    """ Rule to update beliefs, esteem and discrepancy about other jurors in info pooling"""
    def match(juror):
        return (juror.context.phase is Phase.info_pooling and juror.context.juror_to_speak != juror.id)
    def do(juror):
        adjust_others_beliefs_general(juror,juror.context.message)

class Rule5(Rule_mine):
    """ Rule to update my beliefs according to the influence the message has on me"""

    def match(juror):
        return juror.context.phase is Phase.belief_confrontation and juror.context.message
    def do(juror):

        message = juror.context.message[0]
        
        speaker = message.sender_juror
        juror.beliefs.other_jurors_beliefs[speaker] = get_other_juror_belief_with_discrepancy(juror, message.beliefs_debated)

        speaker_opinions = juror.beliefs.other_jurors_beliefs[speaker]
        debated_beliefs_similarity = Veracity.HIGH.value * len(message.beliefs_debated.keys()) # inicializamos con el mayor valor de similitud que se puede tener
        for juror_belief in message.beliefs_debated.keys():

            debated_beliefs_similarity -= speaker_opinions[juror_belief].discrepancy
        debated_beliefs_similarity += juror.beliefs.esteem_for_others[speaker]
        my_opinions = juror.beliefs.facts_with_value
        for fact in message.beliefs_debated.keys():
            if juror.beliefs.facts[fact].name is Veracity.UNCERTAIN.name and message.beliefs_debated[fact].name is Veracity.UNCERTAIN.name:
                continue
            if juror.beliefs.facts[fact].value > message.beliefs_debated[fact].value:
                my_opinions[fact].veracity -= debated_beliefs_similarity
            else:
                my_opinions[fact].veracity += debated_beliefs_similarity
            juror.update_facts_level(my_opinions[fact].veracity, fact)   

class Rule6(Rule_mine):
    """ Rule to update discrepancies once the opinions of others have made me change mine"""

    def match(juror):
        return juror.context.phase is Phase.belief_confrontation and juror.context.message
    def do(juror):
        for other_juror in juror.beliefs.other_jurors_beliefs.keys():
            for fact in juror.beliefs.other_jurors_beliefs[other_juror].keys():
                discrepancy = abs(juror.beliefs.facts[fact].value - juror.beliefs.other_jurors_beliefs[other_juror][fact].value)
                juror.beliefs.other_jurors_beliefs[other_juror][fact].discrepancy = discrepancy

class Rule4(Rule_mine):
    """ Rule to update the veracity of jurors about the case"""

    def match(juror):
        return juror.context.phase is Phase.juror_feedback
    def do(juror):
        update_veracity(juror, juror.context.witness_speaking, juror.context.current_fact)
        
class Rule2(Rule_mine):
    """ Rule to express beliefs in info pooling"""

    def match(juror):
        return juror.context.phase is Phase.info_pooling and juror.context.juror_to_speak == juror.id
    def do(juror):
        share_beliefs_general(juror)

class Rule3(Rule_mine):
    """ Rule to set desire of start debate in info pooling"""

    def match(juror):
        return juror.context.phase is Phase.belief_confrontation and juror.is_foreperson and not juror.context.message
    def do(juror):
        juror.desires[Juror_desires.Start_debate] = 40


class Rule7(Rule_mine):
    """ Rule to update beliefs and discrepancy about other jurors in belief confrontation"""

    def match(juror):
        if juror.context.phase is Phase.belief_confrontation and juror.context.message:
            return juror.role is Roles.leader
        return False
    def do(juror):
        prob = random.randint(20,39)
        juror.desires[Juror_desires.Convince_others_of_my_beliefs] = prob

class Rule8(Rule_mine):
    """ Rule to update beliefs and discrepancy about other jurors in belief confrontation"""

    def match(juror):
        if juror.context.phase is Phase.belief_confrontation and juror.context.message:
            return juror.role is Roles.filler and juror.beliefs.esteem_for_others[juror.context.message[0].sender_juror] >= 10
        return False
    def do(juror):
        prob = random.randint(1,3)
        juror.desires[Juror_desires.Support_a_jurors_beliefs] += prob + 2*(juror.beliefs.esteem_for_others[juror.context.message[0].sender_juror])

class Rule9(Rule_mine):
    """ Rule to update beliefs and discrepancy about other jurors in belief confrontation"""

    def match(juror):
        if juror.context.phase is Phase.belief_confrontation and juror.context.message:
            juror.debated_beliefs_similarity = 0
        
            for belief, value in juror.context.message[0].beliefs_debated.items():
                juror.debated_beliefs_similarity += Veracity.HIGH.value - juror.beliefs.other_jurors_beliefs[juror.context.message[0].sender_juror][belief].discrepancy
            return juror.role is Roles.follower and juror.beliefs.esteem_for_others[juror.context.message[0].sender_juror] >= 10 and juror.debated_beliefs_similarity >= 5
        return False
    def do(juror):
        juror.desires[Juror_desires.Support_a_jurors_beliefs] += juror.debated_beliefs_similarity + (juror.beliefs.esteem_for_others[juror.context.message[0].sender_juror])/2

class Rule10(Rule_mine):
    """ Rule to update beliefs and discrepancy about other jurors in belief confrontation"""

    def match(juror):
        if juror.context.phase is Phase.belief_confrontation and juror.context.message:
            result = sorted([key for key, value in juror.beliefs.esteem_for_others.items() if value > 7], reverse=True)
            if len(result) > 0:
                tmp = random.randint(0,len(result)-1)
                juror.beliefs.juror_to_support = result[tmp]
            return juror.extraversion is Trait_Level.high and len(result) > 0
        return False
    def do(juror):
        juror.desires[Juror_desires.Support_a_jurors_beliefs] += juror.beliefs.esteem_for_others[juror.beliefs.juror_to_support] + 3

class Rule11(Rule_mine):
    """ Rule to update beliefs and discrepancy about other jurors in belief confrontation"""

    def match(juror):
        if juror.context.phase is Phase.belief_confrontation and juror.context.message:
            highest_discrepancy_value = 5
            most_discrepant_jurors = []
            for other_juror in juror.beliefs.other_jurors_beliefs.keys():
                total = 0
                for fact in juror.beliefs.other_jurors_beliefs[other_juror].keys():
                    total += juror.beliefs.other_jurors_beliefs[other_juror][fact].discrepancy
                if total == highest_discrepancy_value:
                    most_discrepant_jurors.append(other_juror)
                if total > highest_discrepancy_value:
                    highest_discrepancy_value = total
                    most_discrepant_jurors = [other_juror]

            if most_discrepant_jurors:
                tmp = random.randint(0, len(most_discrepant_jurors)-1)
                juror.beliefs.juror_to_contradict = most_discrepant_jurors[tmp]
                juror.beliefs.discrepancy_value = highest_discrepancy_value 
                return juror.extraversion is Trait_Level.high
            return False
        return False
    def do(juror):
        juror.desires[Juror_desires.Contradict_a_jurors_beliefs] = juror.beliefs.discrepancy_value + 3*(juror.beliefs.juror_to_contradict.id == juror.context.message[0].sender_juror)
        juror.desires[Juror_desires.Contradict_a_jurors_beliefs] += 2*(juror.neuroticism is Trait_Level.high)

class Rule12(Rule_mine):
    """ Rule to update beliefs and discrepancy about other jurors in belief confrontation"""

    def match(juror):
        if juror.context.phase is Phase.belief_confrontation and juror.context.message:
            most_relevant_fact = get_most_relevant_fact(juror.beliefs.facts_with_value)
            juror.beliefs.confidence_on_most_relevant_fact = abs(juror.beliefs.facts_with_value[most_relevant_fact].veracity)
            juror.disagreeing_jurors = get_fact_disagreement(juror,most_relevant_fact)
            return (juror.role is Roles.holdout or juror.role is Roles.negotiator or juror.role is Roles.leader) and (juror.beliefs.confidence_on_most_relevant_fact >= 28 and juror.disagreeing_jurors >= 0.4)
        return False
    def do(juror):
        juror.desires[Juror_desires.Strengthen_veracity_of_most_relevant_fact] = juror.beliefs.confidence_on_most_relevant_fact
        juror.desires[Juror_desires.Strengthen_veracity_of_most_relevant_fact] += 2*(juror.conscientiousness is Trait_Level.high)
        juror.desires[Juror_desires.Strengthen_veracity_of_most_relevant_fact] -= 3*(juror.openness is Trait_Level.low)

class Rule13(Rule_mine):
    """ Rule to update beliefs and discrepancy about other jurors in belief confrontation"""

    def match(juror):
        if juror.context.phase is Phase.belief_confrontation and juror.context.message:
            if not juror.most_relevant_fact:
                juror.most_relevant_fact = get_most_relevant_fact(juror.beliefs.facts_with_value)
            
            juror.beliefs.confidence_on_most_relevant_fact = abs(juror.beliefs.facts_with_value[juror.most_relevant_fact].veracity)
            juror.disagreeing_jurors = get_fact_disagreement(juror,juror.most_relevant_fact)
            return juror.role is Roles.negotiator and juror.beliefs.confidence_on_most_relevant_fact >= 28 and juror.disagreeing_jurors >= 0.3
        return False
    def do(juror):
        juror.desires[Juror_desires.Reach_consensus_on_most_relevant_fact] = juror.beliefs.confidence_on_most_relevant_fact + 10
        juror.desires[Juror_desires.Reach_consensus_on_most_relevant_fact] += 2*(juror.conscientiousness is Trait_Level.high)
        juror.desires[Juror_desires.Reach_consensus_on_most_relevant_fact] -= 3*(juror.openness is Trait_Level.low)

class Rule14(Rule_mine):
    """ Rule to update beliefs and discrepancy about other jurors in belief confrontation"""

    def match(juror):
        if juror.context.phase is Phase.belief_confrontation and juror.context.message:
            common_belief = get_common_belief_different_from_yours(juror,8.3)
            juror.beliefs.common_belief = common_belief
            return common_belief and juror.role is Roles.filler
        return False
    def do(juror):
        juror.desires[Juror_desires.Support_big_majority] = 26 + len(juror.beliefs.common_belief.keys())

class Rule15(Rule_mine):
    """ Rule to update beliefs and discrepancy about other jurors in belief confrontation"""

    def match(juror):
        if juror.context.phase is Phase.belief_confrontation and juror.context.message:
            return juror.role is not Roles.follower and juror.role is not Roles.filler
        return False
    def do(juror):
        juror.desires[Juror_desires.Convince_others_of_my_beliefs] = 15 + juror.beliefs.confidence_on_most_relevant_fact

def perceive_world_juror(juror : Juror):
    for rule in juror.assert_rules:
        if rule.match(juror):
            rule.do(juror)
    for rule in juror.generate_desires_rules:
        if rule.match(juror):
            rule.do(juror)
    return juror.execute_action_func(juror, filter_desires(juror.desires))

def filter_desires(desires):
    if len(desires) > 0:
        result = sorted([key for key, value in desires.items() if value > 0], key=lambda k: desires[k], reverse=True)
        if not len(result):
            return None
        if len(result)< 3:
            return result[0]
        tmp = random.randint(0, 2)
        return result[tmp]
    return None

def execute_actions_juror(juror: Juror, desire: Juror_desires):

    answer = {}
    if not desire:
        return [answer, 0]
    strength = juror.desires[desire]
    if desire is Juror_desires.Contradict_a_jurors_beliefs:
        for fact in juror.context.message[0].beliefs_debated:
            if juror.context.message[0].beliefs_debated[fact] is Veracity.HIGH or juror.context.message[0].beliefs_debated[fact] is Veracity.UNCERTAIN:
                answer[fact] = Veracity.LOW
            else:
                answer[fact] = Veracity.HIGH
    elif desire is Juror_desires.Strengthen_veracity_of_most_relevant_fact:
        answer[juror.most_relevant_fact] = juror.beliefs.facts[juror.most_relevant_fact]
    elif desire is Juror_desires.Support_a_jurors_beliefs:
        answer = juror.beliefs.other_jurors_beliefs[juror.beliefs.juror_to_support]
    elif desire is Juror_desires.Support_big_majority:
        answer = juror.beliefs.majority_opinion
    elif desire is Juror_desires.Reach_consensus_on_most_relevant_fact:
        avg = juror.beliefs.facts[juror.most_relevant_fact].value
        for other_juror in juror.beliefs.other_jurors_beliefs:
            avg += juror.beliefs.other_jurors_beliefs[other_juror][juror.most_relevant_fact].value
        result = round(avg/(len(juror.beliefs.other_jurors_beliefs.keys()) + 1))
        if result < -15:
            answer[juror.most_relevant_fact] = Veracity.LOW
        elif result > 15:
            answer[juror.most_relevant_fact] = Veracity.HIGH
        else:
            answer[juror.most_relevant_fact] = Veracity.UNCERTAIN
    elif desire is Juror_desires.Convince_others_of_my_beliefs:
        result = get_my_debate_message_with_value_high_openness(juror)
        answer = result[0]
        strength += result[1]
    elif desire is Juror_desires.Start_debate:
        answer = juror.beliefs.facts
    for des in juror.desires:
        juror.desires[des] = 0
    return[Message(juror,answer), strength]
    
# def execute_actions_general(juror:Juror, strength):
#     answer = {}
#     if juror.desires.Contradict_a_jurors_beliefs:
#         juror.desires.Contradict_a_jurors_beliefs = False
#         for fact in juror.context.message.beliefs_debated:
#             if juror.context.message.beliefs_debated[fact] is Veracity.HIGH or juror.context.message.beliefs_debated[fact] is Veracity.UNCERTAIN:
#                 answer[fact] = Veracity.LOW
#             else:
#                 answer[fact] = Veracity.HIGH
#     elif juror.desires.Strengthen_veracity_of_most_relevant_fact:
#         juror.desires.Strengthen_veracity_of_most_relevant_fact = False
#         answer[juror.most_relevant_fact] = juror.beliefs.facts[juror.most_relevant_fact]
#     elif juror.desires.Support_a_jurors_beliefs:
#         juror.desires.Support_a_jurors_beliefs = False
#         answer = juror.beliefs.other_jurors_beliefs[juror.juror_to_interact_with]
#     elif juror.desires.Support_big_majority:
#         juror.desires.Support_big_majority = False
#         answer = juror.beliefs.majority_opinion
#     elif juror.desires.Reach_consensus_on_most_relevant_fact:
#         juror.desires.Reach_consensus_on_most_relevant_fact = False
#         avg = juror.beliefs.facts[juror.most_relevant_fact].value
#         for other_juror in juror.beliefs.other_jurors_beliefs:
#             avg += juror.beliefs.other_jurors_beliefs[other_juror][juror.most_relevant_fact].value
#         result = round(avg/(len(juror.beliefs.other_jurors_beliefs.keys()) + 1))
#         answer[juror.most_relevant_fact] = result
#     elif juror.desires.Convince_others_of_my_beliefs:
#         juror.desires.Convince_others_of_my_beliefs = False
#         result = get_my_debate_message_with_value_high_openness(juror)
#         answer = result[0]
#         strength = result[1]
#     elif juror.desires.Start_debate:
#         juror.desires.Start_debate = False
#         answer = juror.beliefs.facts
#         juror.context.set_message(Message(juror,answer))
#     return [answer,strength]

def get_my_debate_message_with_value_high_openness(juror: Juror):
    r = random.randint(1, 10)
    message = None
    if juror.agreeableness is Trait_Level.low:
        if r >= 4:
        # all
            message = get_all_beliefs_to_debate(juror, Trait_Level.high)
        else:
            #some
            message = get_some_beliefs_to_debate(juror, Trait_Level.high)
    elif juror.extraversion is Trait_Level.low and r >= 4:
        # some
        message = get_some_beliefs_to_debate(juror, Trait_Level.low)
    else:
        # all
        message = get_all_beliefs_to_debate(juror, Trait_Level.low)
    if juror.extraversion is Trait_Level.high:
        message[1] += 5
    return message

def get_some_beliefs_to_debate(juror: Juror, discrepance_level):
    """without considering majority or middle ground"""
    valid_facts_scores = 0
    valid_facts = {}
    for fact in juror.beliefs.facts.keys():
        for other_juror in juror.beliefs.other_jurors_beliefs.keys():
            if not fact in juror.beliefs.other_jurors_beliefs[other_juror]:
                continue
            difference = abs(juror.beliefs.other_jurors_beliefs[other_juror][fact].value - juror.beliefs.facts[fact].value)
            if difference != discrepance_level.value:
                continue
            valid_facts_scores += 1
            if fact not in valid_facts:
                valid_facts[fact] = juror.beliefs.facts[fact]
    if not valid_facts:
        return [valid_facts,0]
    return [valid_facts,valid_facts_scores/len(valid_facts)]

def get_all_beliefs_to_debate(juror, discrepance_level):
    discrepant_facts_scores = 0
    discrepant_facts = {}
    for fact in juror.beliefs.facts.keys():
        for other_juror in juror.beliefs.other_jurors_beliefs.keys():
            difference = 0
            if fact in juror.beliefs.other_jurors_beliefs[other_juror]:
                difference = abs(juror.beliefs.other_jurors_beliefs[other_juror][fact].value - juror.beliefs.facts[fact].value)
            
            if not difference:
                continue
            discrepant_facts_scores += 1
            if fact not in discrepant_facts:
                discrepant_facts[fact] = juror.beliefs.facts[fact]
    discrepant_facts_scores = 0 if len(discrepant_facts) == 0 else discrepant_facts_scores/len(discrepant_facts)
    return [discrepant_facts,discrepant_facts_scores]