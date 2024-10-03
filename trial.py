from environment import SimulationContext
from utils import Phase
from deliberation import simulate_deliberation
from lawyer import Lawyer
from agent_methods import update_veracity
import copy

def phase_witness_interrogation(testimonies, strategies, lawyer : Lawyer, jurors):
    context = SimulationContext()
    for testimony, strategy in zip(testimonies, strategies):
        context.set_phase(Phase.aplication_strategies)
        context.set_ongoing_strategy(strategy) 
        witness = testimony[0]
        context.set_witness_speaking(witness)
        lawyer.perceive_world()

        context.set_phase(Phase.witness_testimony)
        witness.perceive_world()
        witness.execute_actions()

        context.set_phase(Phase.juror_feedback)
        context.set_current_fact(testimony[1])
        for juror in jurors:
            juror.perceive_world()

def simulate_trial(jurors_strategies, n_jurors, testimonies, jury_pool, lawyer):
    jurors = [j for j in jurors_strategies[:n_jurors]]
    strategies = [s for s in jurors_strategies[n_jurors:]]
    print(f'Jurors {jurors}')
    jury_pool_copy = copy.deepcopy(jury_pool)
    jurors = [jury_pool_copy[j-1] for j in jurors]
    phase_witness_interrogation(testimonies, strategies, lawyer, jurors)
    not_guilty, guilty = simulate_deliberation(jurors) 

    return not_guilty