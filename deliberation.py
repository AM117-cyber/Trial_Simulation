from jurors import Juror, get_facts_in_format, order_for_info_pooling, set_foreperson
from utils import Debating_points, Fact, Fact_Types, Info_pooling_data, Roles, Testimony_Impressions, Vote


def simulate_deliberation():

    # foreperson speaks more and is more influential
    foreperson = set_foreperson(jury) # selects a foreperson from the jury and adds foreperson desires to their desires
    jury = order_for_info_pooling(jury) # orders according to confidence levels in what they belief, extraversion and openness
    jurors_that_have_talked = 0
    for juror in jury:
        juror.desires.listen_testimonies = False
        juror.participate_in_info_pooling = True
        print(f"Age: {juror.age}, Confidence Level: {juror.confidence_level()}, Extraversion: {juror.extraversion}, Openness: {juror.openness}")
        for juror_recipient in jury:
            if juror_recipient.id != juror.id:
                juror_recipient.perceive_world(Info_pooling_data(jurors_that_have_talked,get_facts_in_format(juror.beliefs.facts), juror))
        jurors_that_have_talked+=1
    # asumamos que foreperson siempre inicia el debate
    current_debater = foreperson
    time = 0
    while current_debater and time <= len(jury) *20: #si llega a ese límite a dado tiempo a que hablen todos los del jurado 20 veces. time representa la cantidad de intervenciones
        time+=1
        beliefs_to_debate = current_debater.beliefs.facts_with_discrepancy_value
        if not beliefs_to_debate:
            beliefs_to_debate = get_facts_in_format(current_debater.beliefs.facts)
        max_value = len(jury)/2 * 25 # debating threshold
        for juror in jury:
            if juror.number != current_debater:
                value = juror.perceive_world(Debating_points(current_debater,beliefs_to_debate, None))
                if value > max_value:
                    current_debater = juror
        if max_value <= 100: # no ha cambiado, entonces no hay persona que continúe el debate
            break
    for juror in jury:
        vote = juror.vote()
        not_guilty = 0
        guilty = 0
        if vote is Vote.not_guilty:
            not_guilty +=1
        else:
            guilty +=1
    print(f"Votes for not guilty: {not_guilty}")
    print(f"Votes for guilty: {guilty}")
    return (not_guilty,guilty)

fact1 = Fact(Fact_Types.oportunity, "fact1")
fact2 = Fact(Fact_Types.motive, "fact2")
fact3 = Fact(Fact_Types.character, "fact3")

# Creating 6 instances of the juror class
jury1 = Juror("High", "Low", "High", "Low", "High", "Internal", "High", "High", "High", "Low", "None", 30, "Male", "Asian", "Middle", {fact1: (5.6,30), fact2: (7.3, -47), fact3: (5,20)}, [Testimony_Impressions.nervous_witness,Testimony_Impressions.caught_lying,Testimony_Impressions.relatable], Roles.holdout)
jury2 = Juror("Low", "High", "Low", "High", "Low", "External", "Low", "Low", "Low", "High", "Some", 45, "Female", "Caucasian", "High", {fact1: (2.7,-20), fact2: (4.3, -40), fact3: (3.4,35)}, [Testimony_Impressions.nervous_witness,Testimony_Impressions.caught_lying,Testimony_Impressions.relatable], Roles.follower)
jury3 = Juror("High", "High", "Low", "Low", "High", "Internal", "High", "Low", "High", "Low", "None", 25, "Male", "African American", "Low", {fact1: (4.1, 15), fact2: (4.3, -50), fact3: (3,8)}, [Testimony_Impressions.nervous_witness,Testimony_Impressions.caught_lying,Testimony_Impressions.relatable], Roles.filler)
jury4 = Juror("Low", "Low", "High", "High", "Low", "External", "Low", "High", "Low", "High", "Some", 35, "Female", "Hispanic", "Middle", {fact1: (3.2,43), fact2: (6.7, -19), fact3: (4.7,33)}, [Testimony_Impressions.nervous_witness,Testimony_Impressions.caught_lying,Testimony_Impressions.relatable], Roles.follower)
jury5 = Juror("High", "Low", "High", "High", "Low", "Internal", "High", "High", "High", "Low", "None", 40, "Male", "Asian", "High", {fact1: (6.2,40), fact2: (8.4, -33), fact3: (5.9,45)}, [Testimony_Impressions.nervous_witness,Testimony_Impressions.caught_lying,Testimony_Impressions.relatable], Roles.leader) #leader
jury6 = Juror("Low", "High", "Low", "High", "Low", "External", "Low", "Low", "Low", "High", "Some", 50, "Female", "Caucasian", "Low", {fact1: (3.1,10), fact2: (4.3, -42), fact3: (3.5,40)}, [Testimony_Impressions.nervous_witness,Testimony_Impressions.caught_lying,Testimony_Impressions.relatable], Roles.follower)

# List of jurors
jurors = [jury1, jury2, jury3, jury4, jury5, jury6]

   