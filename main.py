from lawyer import Lawyer, perceive_world_lawyer
from agent_methods import perceive_world_general, Juror, vote, update_pool, JurorBeliefs
from witness import Witness, perceive_world_witness
from utils import Fact, Fact_Types, Fact_Info, map_trait_level
from genetic_algorithm import genetic_algorithm
from environment import SimulationContext
from intentions import execute_actions_general
import json

def start_simulation(lawyer, testimonies,jury_pool,jury_amount, facts):
    update_pool(jury_pool) # actualiza la relevancia de los hechos por cada jurado y determina su rol
    # top_results = genetic_algorithm(n_strategies=len(lawyer.strategies[0]), n_jurors=jury_amount, n_people=len(jury_pool), 
    #                                 n_testimonies=len(facts))
    context = SimulationContext()
    context.set_sequence_of_events('')
    top_results = genetic_algorithm(lawyer=lawyer, n_jurors=jury_amount, jury_pool=jury_pool, testimonies=testimonies)
    print("It's over")
    for element in top_results:
        print(element.verdict)

def generate_jury_pool(json_file_path, case):
    with open(json_file_path, 'r') as f:
        jurors_data = json.load(f)
    
    # Crear instancias de la clase Juror
    jury_pool = []
    for juror_data in jurors_data:
        juror = Juror(
            perceive_world_func=perceive_world_general,
            execute_action_func=execute_actions_general,
            vote_function=vote,
            id=juror_data['id'],
            openness=map_trait_level(juror_data['openness']),
            conscientiousness=map_trait_level(juror_data['conscientiousness']),
            extraversion=map_trait_level(juror_data['extraversion']),
            agreeableness=map_trait_level(juror_data['agreeableness']),
            neuroticism=map_trait_level(juror_data['neuroticism']),
            locus_of_control=juror_data['locus_of_control'],
            social_norms=juror_data['social_norms'],
            value_emotional_exp=juror_data['value_emotional_exp'],
            takes_risks=juror_data['takes_risks'],
            takes_decisions_by_fear=juror_data['takes_decisions_by_fear'],
            bias=juror_data['bias'],
            age=juror_data['age'],
            gender=juror_data['gender'],
            race=juror_data['race'],
            socioeconomic_status=juror_data['socioeconomic_status'],
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

    witness1 = Witness(1, perceive_world_witness, None, facts=items_case[:3], age=35, socioeconomic_status="medio", education="high", ineptitude=0.2, side=True)
    witness2 = Witness(2, perceive_world_witness, None, facts=items_case[3:5], age=50, socioeconomic_status="alto", education="medium", ineptitude=0.4, side=True)
    witness3 = Witness(3, perceive_world_witness, None, facts=items_case[5:], age=29, socioeconomic_status="bajo", education="low", ineptitude=0.6, side=True)
    
    witnesses = [witness1, witness2, witness3]
    testimonies = [] # testigo, hecho a testificar
    for wit in witnesses:
        for fact in wit.facts:
            testimonies.append((wit, fact))

    lawyer = Lawyer(perceive_world_lawyer, None, witnesses)
    jury_pool = generate_jury_pool('data.json', case)

    start_simulation(lawyer, testimonies, jury_pool, 12, case)