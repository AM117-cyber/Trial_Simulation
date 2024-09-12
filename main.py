case = {} # Se compone de hechos con su relación con el caso y testimonios

jury_pool = generate_jury_pool()

def start_simulation(lawyer, testimonies,jury_pool,jury_amount, facts):
    update_pool(jury_pool, facts) # añade relevance per fact y roles del jurado
    top_results = genetic_algorithm(jury_pool,lawyer,testimonies,facts,jury_amount,facts)
    print("It's over")
    for element in top_results:
        print(element.verdict)

