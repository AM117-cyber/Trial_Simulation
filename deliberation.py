from LLM_use import Trial_summary_generator
from agent_methods import order_for_info_pooling, set_foreperson
from utils import Debating_points, Fact, Fact_Info, Fact_Types, Info_pooling_data, Message, Phase, Roles, Testimony_Impressions, Vote
from environment import SimulationContext

def simulate_deliberation(jury):
    context = SimulationContext()
    context.set_phase(Phase.info_pooling)
    foreperson = set_foreperson(jury)
    print(f"Foreperson is : juror {foreperson.id}")
    jury = order_for_info_pooling(jury)
    for juror in jury:
        context.set_juror_to_speak(juror.id)
        print(f"Age: {juror.age}, Confidence Level: {juror.confidence_level(juror.beliefs.facts_with_value)}, Extraversion: {juror.extraversion}, Openness: {juror.openness}")       
        juror.perceive_world()
    # all jurors shared their beliefs
    context.set_juror_to_speak(-1)
    print("Creencias compartidas en info pooling:")
    for messsage in context.message:
        beliefs = ""
        for fact, value in messsage.beliefs_debated.items():
            beliefs += fact.text + value.name
        print(f"{messsage.sender_juror.id}: {beliefs}")
    for juror in jury:
        juror.perceive_world()
    print(Phase.belief_confrontation)
    context.set_phase(Phase.belief_confrontation)
    context.set_message([])
    # asumamos que foreperson siempre inicia el debate
    current_debater = foreperson
    time = 0
    context.set_message([current_debater.perceive_world()[0]])
    beliefs_to_debate = context.message[0].beliefs_debated
    while current_debater and time <= len(jury) *20: #si llega a ese límite ha dado tiempo a que hablen todos los del jurado 20 veces. time representa la cantidad de intervenciones
        time+=1
        
        max_value = 30 # debating threshold
        for juror in jury:
            points_to_debate = ""
            for fact in beliefs_to_debate.keys():
                points_to_debate+= fact.text + " - " + beliefs_to_debate[fact].name + ", "
            print(f"Juror {current_debater.id} is debating this points: {points_to_debate}")
            if juror.id != current_debater.id:
                if answer:
                    print("nn")
                answer = juror.perceive_world()
                if answer:
                    print("nn")
                if answer and answer[1] > max_value:
                    context.set_message([answer[0]])
                    max_value = answer[1]
        if max_value <= 30: # no ha cambiado, entonces no hay persona que continúe el debate
            break
        current_debater = context.message[0].sender_juror
        beliefs_to_debate = context.message[0].beliefs_debated
    not_guilty = 0
    guilty = 0
    for juror in jury:
        # desire to hide my opinion
        vote = juror.vote()

        if vote is Vote.not_guilty:
            not_guilty +=1
        else:
            guilty +=1
        context.sequence_of_events += "Juror " + str(juror.id) + " voted for " + vote.name + ".\n"
    context.sequence_of_events += "Votes for not guilty: " + str(not_guilty) + ".\n"
    context.sequence_of_events += "Votes for guilty: " + str(guilty) + ".\n"
    print(f"Votes for not guilty: {not_guilty}")
    print(f"Votes for guilty: {guilty}")
    # tsg = Trial_summary_generator()
    # write_to_file("Case 1", tsg.generate_summary(context.sequence_of_events))
    context.message = []
    context.juror_to_speak = -1
    context.phase = None
    context.pooling_speakers_count = 0
    context.jury_size = 6
    context.ongoing_strategy = None
    context.witness_intention = None
    context.sequence_of_events = ''
    context.witness_speaking = None
    context.current_fact = None
    return (not_guilty,guilty, time) 


# fact1 = Fact(Fact_Types.oportunity, "fact1")
# fact2 = Fact(Fact_Types.motive, "fact2")
# fact3 = Fact(Fact_Types.character, "fact3")


# # Creating 6 instances of the juror class
# jury1 = Juror(perceive_world_general, execute_actions_general, vote, 1,"High", "Low", "High", "Low", "High", "Internal", "High", "High", "High", "Low", "None", 30, "Male", "Asian", "Middle", JurorBeliefs({fact1: Fact_Info(5.6,30), fact2: Fact_Info(7.3, -47), fact3: Fact_Info(5,20)})) 
# jury1.role = Roles.holdout
# jury2 = Juror(perceive_world_general, execute_actions_general, vote, 2, "Low", "High", "Low", "High", "Low", "External", "Low", "Low", "Low", "High", "Some", 45, "Female", "Caucasian", "High", JurorBeliefs({fact1: Fact_Info(2.7,-20), fact2: Fact_Info(4.3, -40), fact3: Fact_Info(3.4,35)}))
# jury2.role = Roles.follower
# jury3 = Juror(perceive_world_general, execute_actions_general, vote, 3,"High", "High", "Low", "Low", "High", "Internal", "High", "Low", "High", "Low", "None", 25, "Male", "African American", "Low", JurorBeliefs({fact1: Fact_Info(4.1, 15), fact2: Fact_Info(4.3, -50), fact3: Fact_Info(3,8)}))
# jury3.role = Roles.filler
# jury4 = Juror(perceive_world_general, execute_actions_general, vote, 4, "Low", "Low", "High", "High", "Low", "External", "Low", "High", "Low", "High", "Some", 35, "Female", "Hispanic", "Middle", JurorBeliefs({fact1: Fact_Info(3.2,43), fact2: Fact_Info(6.7, -19), fact3: Fact_Info(4.7,33)}))
# jury4.role = Roles.follower
# jury5 = Juror(perceive_world_general, execute_actions_general, vote, 5,"High", "Low", "High", "High", "Low", "Internal", "High", "High", "High", "Low", "None", 40, "Male", "Asian", "High", JurorBeliefs({fact1: Fact_Info(6.2,40), fact2: Fact_Info(8.4, -33), fact3: Fact_Info(5.9,45)}))
# jury5.role = Roles.leader #leader
# jury6 = Juror(perceive_world_general, execute_actions_general, vote, 6, "Low", "High", "Low", "High", "Low", "External", "Low", "Low", "Low", "High", "Some", 50, "Female", "Caucasian", "Low", JurorBeliefs({fact1: Fact_Info(3.1,10), fact2: Fact_Info(4.3, -42), fact3: Fact_Info(3.5,40)}))
# jury6.role = Roles.follower


# List of jurors
# jurors = [jury1, jury2, jury3, jury4, jury5, jury6]

# simulate_deliberation(jurors)

def write_to_file(filename, content):
    """
    Write content to a file. If the file already exists, append the content two lines below the current content.
    
    Parameters:
    filename (str): The name of the file.
    content (str): The content to write to the file.
    """
    try:
        with open(filename, 'a+') as file:
            file.seek(0)
            data = file.read()
            if data:
                file.write('\n\n')  # Add two new lines before appending new content
            file.write(content)
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
# filename = 'example.txt'
# content = 'This is the new content to add.'
# write_to_file(filename, content)


   

# def simulate_deliberation(jury):

#     # foreperson speaks more and is more influential
#     foreperson = set_foreperson(jury) # selects a foreperson from the jury and adds foreperson desires to their desires
#     jury = order_for_info_pooling(jury) # orders according to confidence levels in what they belief, extraversion and openness
#     jurors_that_have_talked = 0
#     for juror in jury:
#         juror.turn_to_speak = True
#         print(f"Age: {juror.beliefs.age}, Confidence Level: {juror.confidence_level()}, Extraversion: {juror.beliefs.extraversion}, Openness: {juror.beliefs.openness}")
#         for juror_recipient in jury:
#             juror_recipient.desires.listen_testimonies = False
#             juror_recipient.desires.participate_in_info_pooling = True
#             if juror_recipient.id != juror.id:
#                 juror_recipient.perceive_world(Info_pooling_data(jurors_that_have_talked,get_facts_in_format(juror.beliefs.facts), juror))
#         jurors_that_have_talked+=1
#         juror.turn_to_speak = False
#     # asumamos que foreperson siempre inicia el debate
#     current_debater = foreperson
#     time = 0
#     while current_debater and time <= len(jury) *20: #si llega a ese límite a dado tiempo a que hablen todos los del jurado 20 veces. time representa la cantidad de intervenciones
#         time+=1
#         beliefs_to_debate = current_debater.beliefs.facts_with_discrepancy_value
#         if not beliefs_to_debate:
#             beliefs_to_debate = get_facts_in_format(current_debater.beliefs.facts)
#         max_value = len(jury)/2 * 25 # debating threshold
#         for juror in jury:
#             points_to_debate = ""
#             for fact in beliefs_to_debate.keys():
#                 points_to_debate+= fact.name + " - "
#                 points_to_debate+= beliefs_to_debate[fact][0].name + ", "
#             print(f"Juror {current_debater.id} is debating this points: {points_to_debate}")
#             if juror.number != current_debater:
#                 value = juror.perceive_world(Debating_points(current_debater,beliefs_to_debate, None))
#                 if value > max_value:
#                     current_debater = juror
#         if max_value <= 100: # no ha cambiado, entonces no hay persona que continúe el debate
#             break
#     for juror in jury:
#         vote = juror.vote()
#         not_guilty = 0
#         guilty = 0
#         if vote is Vote.not_guilty:
#             not_guilty +=1
#         else:
#             guilty +=1
#     print(f"Votes for not guilty: {not_guilty}")
#     print(f"Votes for guilty: {guilty}")
#     return (not_guilty,guilty)