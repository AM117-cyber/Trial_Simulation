from environment import SimulationContext
from utils import Phase
from deliberation import simulate_deliberation
from lawyer import Lawyer
from agent_methods import update_veracity

def phase_witness_interrogation(testimonies, strategies, lawyer : Lawyer, jurors):
    context = SimulationContext()
    for testimony, strategy in zip(testimonies, strategies):
        context.set_phase(Phase.aplication_strategies)
        context.set_ongoing_strategy(strategy)
        witness = testimony[0]
        context.set_is_own_witness(witness.side)
        lawyer.perceive_world() # actualizar los desires e intentions del abogado
        lawyer.apply_strategy(witness, strategy)

        context.set_phase(Phase.witness_testimony)
        witness.perceive_world()
        update_veracity(jurors, witness, testimony[1])

def simulate_trial(jurors_strategies, n_jurors, testimonies, jury_pool, lawyer):
    jurors = [j for j in jurors_strategies[:n_jurors]]
    strategies = [s for s in jurors_strategies[n_jurors:]]
    print(f'Jurors {jurors}')
    jurors = [jury_pool[j-1] for j in jurors]
    phase_witness_interrogation(testimonies, strategies, lawyer, jurors)
    not_guilty, guilty = simulate_deliberation(jurors) # Ver que recibe esta funcion

    return not_guilty