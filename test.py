from scipy.stats import shapiro, levene
import matplotlib.pyplot as plt
import seaborn as sns
#ANOVA tradicional
from scipy.stats import f_oneway
#ANOVA de Welch
import statsmodels.api as sm
from statsmodels.formula.api import ols
from scipy.stats import bartlett, ttest_ind, mannwhitneyu, kruskal
from trial import simulate_trial
import random
import numpy as np

def verify_suppositions(groups):
    #Analizar si todos los grupos siguen una distribucion normal
    normality = True
    var_homo = True
    for group in groups:
        # Prueba de normalidad (Shapiro-Wilk)
        stat, p_value = shapiro(group)
        print(f'Shapiro-Wilk test: p-value = {p_value}')
        # Si el p-valor es mayor que 0.05, los datos son normales
        if p_value <= 0.05:
            print('Los datos no siguen una distribución normal')
            normality = False
            break
    if normality:
        print('Los datos siguen una distribución normal')
        #Si los datos siguen una distribución normal aplicarv Test de Bartlett
        
        # Prueba de Bartlett
        stat, p_value = bartlett(*groups)

        print(f"Estadístico de Bartlett: {stat}")
        print(f"Valor p: {p_value}")

        if p_value < 0.05:
            print("Rechazamos la hipótesis nula: Las varianzas no son homogéneas")
            var_homo = False
        else:
            print("No se rechaza la hipótesis nula: Las varianzas son homogéneas")
            var_homo = True

    else:
        #Si no se puede asegurar que los datos siguen una distribución normal, aplicar test de Levene
        stat, p_value = levene(*groups)
        print(f'Levene test: p-value = {p_value}')
        # Si el p-valor es mayor que 0.05, se asume homogeneidad de varianzas
        if p_value > 0.05:
            print('Hay homegeneidad de varianza')
            var_homo = True
        else:
            print('No hay homegeneidad de varianza')
            var_homo = False
    return normality, var_homo
    
def multiple_groups_test(groups):

    normality, var_homo = verify_suppositions(groups)
    if not normality:
        # Prueba de Kruskal-Wallis
        stat, p_value = kruskal(*groups)

        print(f"Estadístico: {stat}, Valor p: {p_value}")
        if p_value < 0.05:
            print("Rechazamos la hipótesis nula: Al menos uno de los grupos es diferente.")
            return True
        else:
            print("No se rechaza la hipótesis nula: Los grupos no son significativamente diferentes.")
            return False

    elif normality and var_homo:
        #Se cumplen las suposiciones, por tanto es posible aplicar Test de ANOVA
        # Aplicar ANOVA de una vía
        anova_result = f_oneway(*groups)

        print(f'Estadístico F: {anova_result.statistic}')
        print(f'Valor p: {anova_result.pvalue}')
        if anova_result.pvalue < 0.05:
            print('Hay diferencias significativas entre los grupos')
            return True
        else:
            print('No hay diferencias significativas entre los grupos')
            return False
    else:
        #Aplicar ANOVA de Welch
        return None
        # modelo = ols('valor ~ C(grupo)', data=data).fit()

        # # ANOVA de Welch: usamos el argumento `robust='hc3'` para ajustar por varianzas desiguales
        # anova_result = sm.stats.anova_lm(modelo, typ=2, robust='hc3')
        # if p_value < 0.05:
        #     print("Existen diferencias significativas entre los grupos")
        #     return True

def two_groups_test(groups):
    normality, var_homo = verify_suppositions(groups)

    if normality and var_homo:
        # Prueba t de Student para muestras independientes
        stat, p_value = ttest_ind(*groups)
        print(f'Prueba t: p-value = {p_value}')

        # Si el p-valor es menor que 0.05, hay diferencias significativas entre los dos grupos
        if p_value < 0.05:
            print('Hay diferencias significativas entre los grupos')
            return True
        else:
            print('No hay diferencias significativas entre los grupos')
            return False
    else:
        # Prueba Mann-Whitney U
        stat, p_value = mannwhitneyu(*groups)
        print(f'Mann-Whitney U test: p-value = {p_value}')

        # Si el p-valor es menor que 0.05, hay diferencias significativas entre los dos grupos
        if p_value < 0.05:
            print('Hay diferencias significativas entre los grupos')
            return True
        else:
            print('No hay diferencias significativas entre los grupos')
            return False

def tester(jury_pool, testimonies, lawyer, jury_size, case):
    """Method for run the tests of simulation"""

    # Compare the deliberation time between jurors by jury size
    groups = []
    for jury_amount in range(6,13):
        group = []
        for i in range(10):
            n_people = len(jury_pool)
            n_strategies = len(lawyer.strategies[0])
            n_testimonies = len(testimonies)
            jurors_strategies = tuple(random.sample(range(1, n_people+1), jury_amount)) + tuple(np.random.randint(1, n_strategies+1) for _ in range(n_testimonies))
            _, time = simulate_trial(jurors_strategies, jury_amount, testimonies, jury_pool, lawyer, case)
            group.append(time)
        groups.append(group)
    anova_test = multiple_groups_test(groups)

    # Compare the time deliberation such that there is a single leader on the jury.
    two_groups = []
    leaders = [j for j in jury_pool if j.role == "Leader"]
    non_leaders = [j for j in jury_pool if j.role != "Leader"]

    if len(leaders) > 2:
        for i in range(2):
            group = []
            for _ in range(10):
                if i == 0:
                    selected_leaders = [random.choice(leaders)]
                    selected_non_leaders = random.sample(non_leaders, jury_size - 1)
                else:
                    n_selections = random.choice(range(2,min(jury_size, len(leaders))+1))
                    selected_leaders = random.sample(leaders, n_selections)
                    selected_non_leaders = random.sample(non_leaders, jury_size - n_selections)
                
                n_people = len(jury_pool)
                n_strategies = len(lawyer.strategies[0])
                n_testimonies = len(testimonies)
                selected_jury = [j.id for j in selected_leaders] + [j.id for j in selected_non_leaders]
                jurors_strategies = tuple(selected_jury) + tuple(np.random.randint(1, n_strategies+1) for _ in range(n_testimonies))
                _, time = simulate_trial(jurors_strategies, jury_amount, testimonies, jury_pool, lawyer)
                group.append(time)
            two_groups.append(group)

        t_student_test = two_groups_test(two_groups)
        