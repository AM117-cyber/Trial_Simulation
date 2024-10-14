from environment import SimulationContext
from juror import JurorBeliefs
from utils import Phase
from deliberation import simulate_deliberation
from lawyer import Lawyer
import copy

def phase_witness_interrogation(testimonies, strategies, lawyer : Lawyer, jurors):
    context = SimulationContext()
    context.set_jury_size(len(jurors))
    context.sequence_of_events += '''Following this, the phase of questioning witnesses for and against the deffendant lawyer will be conducted.
                                     Testimony is the combination of a witness and a fact itself. I am going to give you a series of 
                                     testimonies, for each of which I will provide the strategy that the deffendant lawyer applies and the 
                                     influence they provoke in the witness.\n'''
    for testimony, strategy in zip(testimonies, strategies):
        context.sequence_of_events += f'The current testimony is about the following fact: {testimony[1].text}.\n'
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

def simulate_trial(jurors_strategies, n_jurors, testimonies, jury_pool, lawyer,case):
    jurors = [j for j in jurors_strategies[:n_jurors]]
    strategies = [s for s in jurors_strategies[n_jurors:]]
    print(f'Jurors {jurors}')
    jury_pool_copy = copy.deepcopy(jury_pool)
    jurors = [jury_pool_copy[j-1] for j in jurors]
    for juror in jurors:
        juror.beliefs = JurorBeliefs(case)
    phase_witness_interrogation(testimonies, strategies, lawyer, jurors)
    not_guilty, guilty, time, sequence_of_events = simulate_deliberation(jurors) 

    return not_guilty, time, sequence_of_events