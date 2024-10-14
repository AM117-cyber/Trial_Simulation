from juror import Juror, JurorBeliefs, Rule1, Rule16, Rule2, Rule3, Rule5, Rule6, Rule7, Rule8, Rule9, Rule10, Rule11, Rule12, Rule13, Rule14, Rule15, execute_actions_juror, perceive_world_juror
from lawyer import Lawyer, perceive_world_lawyer
from agent_methods import vote, update_pool
from witness import Witness, perceive_world_witness, execute_actions_witness
from utils import Fact, Fact_Types, Fact_Info, Roles, map_trait_level
from genetic_algorithm import genetic_algorithm
from environment import SimulationContext
from test import tester
import json

def start_simulation(lawyer, testimonies,jury_pool,jury_amount, facts):
    update_pool(jury_pool) # actualiza la relevancia de los hechos por cada jurado y determina su rol
    # top_results = genetic_algorithm(n_strategies=len(lawyer.strategies[0]), n_jurors=jury_amount, n_people=len(jury_pool), 
    #                                 n_testimonies=len(facts))
    context = SimulationContext()
    context.set_sequence_of_events('')
    top_results = genetic_algorithm(lawyer=lawyer, n_jurors=jury_amount, jury_pool=jury_pool, testimonies=testimonies)
    print("It's over")
    print(top_results)
    # for element in top_results:
    #     print(element.verdict)

def generate_jury_pool(json_file_path, case, assert_rules, generate_desires_rules):
    with open(json_file_path, 'r') as f:
        jurors_data = json.load(f)
    
    # Crear instancias de la clase Juror
    jury_pool = []
    for juror_data in jurors_data:
        juror = Juror(
            perceive_world_func=perceive_world_juror,
            execute_action_func=execute_actions_juror,
            assert_rules=assert_rules,
            generate_desires_rules=generate_desires_rules,
            vote_function=vote,
            id=juror_data['id'],
            openness=map_trait_level(juror_data['openness']),
            conscientiousness=map_trait_level(juror_data['conscientiousness']),
            extraversion=map_trait_level(juror_data['extraversion']),
            agreeableness=map_trait_level(juror_data['agreeableness']),
            neuroticism=map_trait_level(juror_data['neuroticism']),
            locus_of_control=juror_data['locus_of_control'],
            social_norms=map_trait_level(juror_data['social_norms']),
            value_emotional_exp=map_trait_level(juror_data['value_emotional_exp']),
            takes_risks=map_trait_level(juror_data['takes_risks']),
            takes_decisions_by_fear=map_trait_level(juror_data['takes_decisions_by_fear']),
            bias=juror_data['bias'],
            age=juror_data['age'],
            gender=juror_data['gender'],
            race=juror_data['race'],
            socioeconomic_status=map_trait_level(juror_data['socioeconomic_status']),
            beliefs=JurorBeliefs(case)
        )
        jury_pool.append(juror)

    return jury_pool

if __name__ == '__main__':
    case = {Fact(Fact_Types.oportunity, "Vio al sospechoso cerca de la escena") : Fact_Info(0,0),
            Fact(Fact_Types.motive, "El acusado tenía razones para estar molesto") : Fact_Info(0,0),
            Fact(Fact_Types.character, "El acusado es conocido por su honestidad") : Fact_Info(0,0),
            Fact(Fact_Types.oportunity, "No recuerda exactamente la hora del incidente") : Fact_Info(0,0),
            Fact(Fact_Types.motive, "El acusado tuvo una discusión con la víctima") : Fact_Info(0,0),
            Fact(Fact_Types.character, "El acusado tiene un carácter violento") : Fact_Info(0,0),
            Fact(Fact_Types.oportunity, "El acusado estaba cerca del lugar del crimen") : Fact_Info(0,0),
            Fact(Fact_Types.motive, "El acusado había perdido su trabajo"): Fact_Info(0,0)}
    items_case = list(case.items()) 

    witness1 = Witness(1, perceive_world_witness, execute_actions_witness, facts=items_case[:3], age=35, socioeconomic_status="medio", education="high", ineptitude=0.2, side=True)
    witness2 = Witness(2, perceive_world_witness, execute_actions_witness, facts=items_case[3:5], age=50, socioeconomic_status="alto", education="medium", ineptitude=0.4, side=True)
    witness3 = Witness(3, perceive_world_witness, execute_actions_witness, facts=items_case[5:], age=29, socioeconomic_status="bajo", education="low", ineptitude=0.6, side=True)
    
    witnesses = [witness1, witness2, witness3]
    testimonies = [] # testigo, hecho a testificar
    for wit in witnesses:
        for fact in wit.facts:
            testimonies.append((wit, fact))

    lawyer = Lawyer(perceive_world_lawyer, None, witnesses)
    assert_rules = [Rule1, Rule5, Rule6, Rule16]
    generate_desires_rules = [Rule2, Rule3, Rule7, Rule8, Rule9, Rule10, Rule11, Rule12, Rule13, Rule14, Rule15]
    # jury_pool = generate_jury_pool('data.json', case)
    # Creating 6 instances of the juror class
    jury1 = Juror(perceive_world_juror, execute_actions_juror, assert_rules, generate_desires_rules , vote, 1,map_trait_level("High"), map_trait_level("Low"), map_trait_level("High"), map_trait_level("Low"), map_trait_level("High"), "Internal", map_trait_level("High"), map_trait_level("High"), map_trait_level("High"), map_trait_level("Low"), "None", 30, "Male", "Asian", map_trait_level("Middle"),JurorBeliefs(case)) 
    jury1.role = Roles.holdout
    jury2 = Juror(perceive_world_juror, execute_actions_juror, assert_rules, generate_desires_rules , vote, 2, map_trait_level("Low"), map_trait_level("High"), map_trait_level("Low"), map_trait_level("High"), map_trait_level("Low"), "External", map_trait_level("Low"), map_trait_level("Low"), map_trait_level("Low"), map_trait_level("High"), "Some", 45, "Female", "Caucasian", map_trait_level("High"), JurorBeliefs(case))
    jury2.role = Roles.follower
    jury3 = Juror(perceive_world_juror, execute_actions_juror, assert_rules, generate_desires_rules , vote, 3,map_trait_level("High"), map_trait_level("High"), map_trait_level("Low"), map_trait_level("Low"), map_trait_level("High"), "Internal", map_trait_level("High"), map_trait_level("Low"), map_trait_level("High"), map_trait_level("Low"), "None", 25, "Male", "African American", map_trait_level("Low"),JurorBeliefs(case))
    jury3.role = Roles.filler
    jury4 = Juror(perceive_world_juror, execute_actions_juror, assert_rules, generate_desires_rules , vote, 4, map_trait_level("Low"), map_trait_level("Low"), map_trait_level("High"), map_trait_level("High"), map_trait_level("Low"), "External", map_trait_level("Low"), map_trait_level("High"), map_trait_level("Low"), map_trait_level("High"), "Some", 35, "Female", "Hispanic", map_trait_level("Middle"),JurorBeliefs(case))
    jury4.role = Roles.follower
    jury5 = Juror(perceive_world_juror, execute_actions_juror, assert_rules, generate_desires_rules , vote, 5,map_trait_level("High"), map_trait_level("Low"), map_trait_level("High"), map_trait_level("High"), map_trait_level("Low"), "Internal", map_trait_level("High"), map_trait_level("High"), map_trait_level("High"), map_trait_level("Low"), "None", 40, "Male", "Asian", map_trait_level("High"),JurorBeliefs(case))
    jury5.role = Roles.leader #leader
    jury6 = Juror(perceive_world_juror, execute_actions_juror, assert_rules, generate_desires_rules , vote, 6, map_trait_level("Low"), map_trait_level("High"), map_trait_level("Low"), map_trait_level("High"), map_trait_level("Low"), "External", map_trait_level("Low"), map_trait_level("Low"), map_trait_level("Low"), map_trait_level("High"), "Some", 50, "Female", "Caucasian", map_trait_level("Low"),JurorBeliefs(case))
    jury6.role = Roles.follower
    jury_pool= [jury1,jury2,jury3,jury4,jury5,jury6]

    start_simulation(lawyer, testimonies, jury_pool, 4, case)
    tester(jury_pool, testimonies, lawyer, 4)