from lawyer import Lawyer
from agent_methods import perceive_world_general, Juror, vote, update_pool
from witness import Witness
from utils import Fact, Fact_Types
from genetic_algorithm import genetic_algorithm
import json

def start_simulation(lawyer, testimonies,jury_pool,jury_amount, facts):
    update_pool(jury_pool) # actualiza la relevancia de los hechos por cada jurado y determina su rol
    top_results = genetic_algorithm(n_strategies=len(lawyer.strategies[0]), n_jurors=jury_amount, n_people=len(jury_pool), 
                                    n_testimonies=len(facts))
    print("It's over")
    for element in top_results:
        print(element.verdict)

def generate_jury_pool(json_file_path):
    with open(json_file_path, 'r') as f:
        jurors_data = json.load(f)
    
    # Crear instancias de la clase Juror
    jury_pool = []
    for juror_data in jurors_data:
        juror = Juror(
            perceive_world_func=perceive_world_general,
            execute_action_func=None,
            vote_function=vote,
            id=juror_data['id'],
            openness=juror_data['openness'],
            conscientiousness=juror_data['conscientiousness'],
            extraversion=juror_data['extraversion'],
            agreeableness=juror_data['agreeableness'],
            neuroticism=juror_data['neuroticism'],
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
            beliefs=None
        )
        jury_pool.append(juror)
    
    return jury_pool

if __name__ == '__main__':
    case = [Fact(Fact_Types.oportunity, "Vio al sospechoso cerca de la escena"),
            Fact(Fact_Types.motive, "El acusado tenía razones para estar molesto"),
            Fact(Fact_Types.character, "El acusado es conocido por su honestidad"),
            Fact(Fact_Types.oportunity, "No recuerda exactamente la hora del incidente"),
            Fact(Fact_Types.motive, "El acusado tuvo una discusión con la víctima"),
            Fact(Fact_Types.character, "El acusado tiene un carácter violento"),
            Fact(Fact_Types.oportunity, "El acusado estaba cerca del lugar del crimen"),
            Fact(Fact_Types.motive, "El acusado había perdido su trabajo")] 

    lawyer = Lawyer(perceive_world_general, None)

    witness1 = Witness(1, perceive_world_general, None, facts=[case[0],case[1],case[2]], age=35, socioeconomic_status="medio", education="high", ineptitude=0.2)
    witness2 = Witness(2, perceive_world_general, None, facts=[case[3],case[4]], age=50, socioeconomic_status="alto", education="medium", ineptitude=0.4)
    witness3 = Witness(3, perceive_world_general, None, facts=[case[5],case[6],case[7]], age=29, socioeconomic_status="bajo", education="low", ineptitude=0.6)
    
    witnesses = [witness1, witness2, witness3]
    testimonies = [] # testigo, hecho a testificar
    for wit in witnesses:
        for fact in wit.facts:
            testimonies.append((wit.id, fact))

    jury_pool = generate_jury_pool()

    start_simulation(lawyer, testimonies, jury_pool, 12, case)