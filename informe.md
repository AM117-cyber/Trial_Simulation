
### Introducción a los Juicios

Los juicios son procesos legales fundamentales en los sistemas judiciales de todo el mundo. Su objetivo principal es resolver disputas entre partes, ya sean individuos, organizaciones o el Estado, de manera justa y equitativa. Los juicios buscan determinar la verdad de los hechos presentados y aplicar la ley de acuerdo con las pruebas y argumentos expuestos.

### Objeto Social de los Juicios

El objeto social de los juicios es garantizar la justicia y el orden en la sociedad. A través de los juicios, se intenta proteger los derechos de los individuos y asegurar que las leyes se apliquen correctamente. Además, los juicios sirven como un mecanismo para resolver conflictos de manera pacífica y estructurada, evitando así la violencia y la anarquía.

### Funcionamiento de los Juicios

El funcionamiento de los juicios varía según la jurisdicción y el tipo de caso, pero generalmente sigue una estructura similar:

1. **Presentación del Caso**: Las partes involucradas presentan sus argumentos y pruebas ante un juez o un jurado.
2. **Evaluación de Pruebas**: El juez o el jurado evalúa las pruebas presentadas, incluyendo testimonios, documentos y otros elementos relevantes.
3. **Argumentos de las Partes**: Los abogados de ambas partes presentan sus argumentos, tratando de persuadir al juez o al jurado sobre la veracidad de sus afirmaciones.
4. **Deliberación**: En el caso de un juicio con jurado, los miembros del jurado deliberan para llegar a un veredicto. En un juicio sin jurado, el juez toma la decisión.
5. **Veredicto y Sentencia**: Se emite un veredicto basado en las pruebas y argumentos presentados. Si se encuentra culpable a una de las partes, se dicta una sentencia que puede incluir multas, penas de prisión u otras sanciones.

Una parte fundamental de estos procesos son los miembros del jurado; ciudadanos convocados para analizar objetivamente los hechos presentados en un juicio y luego debatir las conclusiones alcanzadas. No todos los juicios tienen a un jurado decidiendo el veredicto final, sin embargo, esta práctica es muy frecuente debido a que se considera más justo que dejar la decisión únicamente en manos de un individuo (juez). 

En el transcurso de un juicio hay muchos elementos que pueden influenciar la opinión del jurado con respecto a los aspectos discutidos. Estos pueden estar relacionados con la personalidad de cada jurado y sus vivencias personales, por lo que con el surgimiento de las redes sociales y los científicos de datos no es de extrañar que varias compañías oferten entre sus servicios la creación de perfiles de personas con el objetivo de utilizarlos en un juicio. Con esta información antes del comienzo de la selección del jurado, los abogados pueden determinar qué estrategias resultarán más eficaces para los distintos miembros del pre-jurado y seleccionar los que puedan contribuir a llegar al veredicto que se persigue. Muchos abogados utilizan su experiencia ejerciendo para imaginar cómo se comportarán durante un juicio dados sus perfiles; sin embargo, mediante una simulación del juicio se puede llegar a resultados que tomen en cuenta más factores que los que un solo ser humano pueda considerar en un escenario reproducido en su mente. Es por esta razón que este proyecto busca hacer una simulación de los eventos de un jucio que afectan al jurado, con una simplificación de las etapas del juicio que fue necesario hacer para que el proyecto se terminara en el tiempo con el que se contaba.

### Descripción de un juicio en la simulación
 En la simulación se asume que se cuenta con perfiles con cierto grado de correctitud para cada miembro del jurado. Partimos de un conjunto de personas de las cuales se debe seleccionar al jurado; una vez hecho esto tienen lugar la examinación de testigos y la deliberación del jurado.

 En la simulación intervienen 3 tipos de agentes: Abogado, Testigo y Jurado. Estos fueron modelados con la arquitectura BDI (Belief-Desire-Intention) que se utiliza en la simulación de sistemas complejos debido a su capacidad para manejar múltiples tipos de agentes con diferentes roles y objetivos. Este modelo se basa en tres componentes principales:

**Beliefs (Creencias)**: Representan el conocimiento del agente sobre el mundo. En los agentes mencionados anteriormente se puede interpretar como los hechos que se defienden en un testimonio (en el caso del testigo) o las opiniones de cada jurado relacionadas con los hechos discutidos en el juicio.

**Desires (Deseos)**: Son los objetivos que el agente quiere alcanzar.Para un abogado puede ser ganar el caso, mientras que un testigo puede querer testificar honestamente o no y los jurados pueden querer hacer llegar a otros su opinión o debatir las creencias más discrepantes entre ellos y los otros jurados, así como apoyar las opiniones de un jurado que actúe como líder.

**Intentions (Intenciones)**: Son los planes que el agente tiene para alcanzar sus deseos. Esto incluye las acciones específicas que el agente tomaría.

También es necesario considerar la comunicación entre agentes, puesto que en la deliberación del jurado cada persona tiene que ser capaz de escuchar las opiniones de la otra y tomar la decisión de si vale la pena debatir o no con ella, en correspondencia con la diferencia que haye entre sus opiniones y la confianza que se tenga en las opiniones propias y las de la otra persona. Para lograr un comportamiento parecido se separó la deliberación en dos fases: info pooling y belief confrontation. En la primera fase cada jurado expresa sus creencias al resto del grupo, que actualiza a su vez sus creencias con respecto a las opiniones de ese miembro del jurado. En la fase belief confrontation los jurados que consideran que tienen grandes discrepancias con los demás las expresan en un intento por persuadir las creencias que ellos consideran erróneas. Las creencias que un jurado comparta con los demás no tienen por qué ser las reales, sino que pueden ser las creencias que ese jurado considera que encajan mejor con la opinión de la mayoría o que responden a algún deseo que el jurado tenga, como apoyar las ideas de otro integrante del jurado

### Agentes:

**Agente Miembro del Jurado (Juror Agent)**:

La modelación de un agente miembro del jurado en un sistema BDI se centra en la representación de las creencias, la generación de opciones basadas en estas creencias, la selección de intenciones y acciones basadas en estas opciones, y la actualización de las creencias a medida que el agente interactúa con otros jurados y el entorno del juicio. Este enfoque permite que el agente tome decisiones informadas y adaptativas basadas en su conocimiento actual y las condiciones del entorno, reflejando la lógica de toma de decisiones y la interacción con el entorno de una manera que imita la deliberación humana.

Las creencias actuales del agente incluyen información sobre los hechos del caso, la relevancia y veracidad de cada uno, y las opiniones de otros jurados. Durante la fase de escuchar los testimonios los abogados aplican una estrategia, la cual genera una reacción en el testigo que se encuentra en el estrado en ese momento. Esta reacción es percibida por cada miembro del jurado, provocando que actualice sus creencias con respecto a la relevancia y veracidad de los hechos que se están discutiendo. Durante la deliberación, una vez compartidas las impresiones de cada jurado con respecto a los hechos, se inicia el debate. El jurado designado como cabecilla (foreperson) se encarga de hablar primero y los demás perciben su discurso con la función perceive_world, en la cual se ajustan sus creencias para luego generar deseos y finalmente compartir aspectos de ciertos hechos, que se determinan por los deseos que tenga en el momento. La función de generación de opciones evalúa las creencias actuales para determinar los deseos disponibles, y el conjunto de posibles intenciones representa las distintas formas en las que puede elegir expresar una opinión para cumplir con el deseo que el agente busca alcanzar.


### Uso de la inteligencia artificial en el proyecto:

El uso de la inteligencia artificial (IA) en la simulación de juicios ha permitido mejorar la precisión y realismo al modelar el comportamiento de los actores clave en un juicio, como son los abogados, jurados y testigos. En este proyecto, la IA se utiliza para simular las reacciones de los jurados y cómo sus emociones y características afectan su percepción de la veracidad del testimonio. El sistema experto basado en lógica difusa es una herramienta central en este enfoque, ya que permite clasificar a los jurados y ajustar sus decisiones de manera más precisa y realista.

### Clasificación de jurados utilizando un sistema experto y lógica difusa

El sistema experto desarrollado en esta simulación se centra en clasificar a los jurados en función de sus características psicológicas y sociodemográficas, lo que resulta en un perfil que influye en su comportamiento durante el juicio. Utilizando lógica difusa, el sistema evalúa diversas características del jurado, tales como:

- **Apertura**: Tendencia a aceptar nuevas ideas y experiencias.
- **Extraversión**: Nivel de sociabilidad y energía.
- **Amabilidad**: Capacidad de cooperar y ser empático con los demás.
- **Conciencia**: Grado de responsabilidad y meticulosidad.
- **Neuroticismo**: Tendencia a experimentar emociones negativas como ansiedad.
- **Locus de control**: Grado de percepción de control sobre los eventos.
- **Experencia emocional**: Valor que el jurado otorga a las experiencias emocionales.
- **Toma de riesgos**: Propensión a actuar frente a la incertidumbre.
- **Decisiones motivadas por miedo**: Inclinación a tomar decisiones basadas en evitar riesgos.
- **Estatus socioeconómico**: Nivel de ingreso y posición social del jurado.

La lógica difusa permite modelar estas características de manera flexible, manejando la incertidumbre y la variabilidad inherente en las respuestas humanas. Por ejemplo, no todos los jurados que muestran altos niveles de extraversión tendrán exactamente el mismo comportamiento, pero el sistema puede clasificar sus tendencias generales y cómo estas influirán en su juicio.

####  Clasificación de los jurados

El sistema utiliza las características mencionadas para clasificar a los jurados en cinco grupos:

- **Líderes**: Carismáticos y seguros de sí mismos, son quienes tienen opiniones fuertes y tienden a influir en el resto del jurado.
- **Seguidores**: Más conformistas, suelen adherirse a las opiniones de los líderes o la mayoría.
- **Indecisos**: Tienen opiniones neutrales o débiles, pero son susceptibles de ser convencidos por argumentos sólidos.
- **Negociadores**: Hábiles en mediar y encontrar puntos en común, se enfocan en encontrar soluciones.
- **Resistentes**: Tienen opiniones firmes y son difíciles de cambiar o influenciar.

Estas clasificaciones permiten que el sistema simule cómo los jurados interactúan entre sí y cómo sus características influyen en las decisiones de los otros. Por ejemplo, un jurado clasificado como líder influirá de manera significativa en la decisión del grupo, mientras que un jurado resistente será más difícil de convencer, incluso frente a evidencia contundente.

### Impacto en la simulación

El sistema experto y el uso de lógica difusa en la clasificación de jurados son fundamentales para simular con precisión cómo los diferentes tipos de jurados responden a los testimonios. Este enfoque no solo mejora la precisión del modelo, sino que también proporciona información valiosa sobre la dinámica interna del jurado. Con este nivel de detalle, la simulación permite entender mejor cómo las emociones y percepciones afectan el juicio final del jurado, permitiendo anticipar posibles resultados y mejorar las estrategias legales en un juicio.

###  Búsqueda de la mejor combinación de estrategias legales y jurados mediante un algoritmo genético

El problema de optimizar las estrategias de los abogados y la selección de jurados en el contexto de una simulación de juicio es intrínsecamente complejo y multidimensional. Al igual que en otros problemas de optimización, no existe una solución lineal simple para determinar qué combinación de estrategias y jurados proporcionará el mejor resultado en el veredicto final. Las interacciones entre las emociones de los testigos, las reacciones de los jurados y las estrategias aplicadas por los abogados generan un espacio de búsqueda vasto y no polinomial, lo que requiere una solución avanzada como un algoritmo genético para encontrar la mejor combinación.

####  Algoritmo genético aplicado a la simulación del juicio

El algoritmo genético es una metaheurística basada en la teoría evolutiva de la selección natural. Se utiliza para generar soluciones de alta calidad para problemas complejos mediante la reproducción y mutación de combinaciones de variables. En esta simulación, las variables son las **estrategias legales** y los **jurados seleccionados**, que se evalúan según su capacidad para influir positivamente en el veredicto final del caso.

El algoritmo comienza con una población inicial de combinaciones de estrategias y jurados, donde cada individuo en esta población representa una solución potencial, es decir, una configuración específica de estrategia aplicada a los testigos y una selección particular de jurados. El proceso de evolución busca mejorar la calidad de estas combinaciones a lo largo de múltiples generaciones, utilizando operadores de cruce y mutación.

#### Funcionamiento del algoritmo genético

Cada combinación de estrategias y jurados es evaluada utilizando una **función de aptitud**, que mide la efectividad de esa combinación en relación con el veredicto del jurado. Cuanto mejor sea la decisión del jurado, más alta será la aptitud de la solución.

El ciclo del algoritmo sigue los siguientes pasos:

- **Población inicial**: Se genera una primera población de combinaciones de estrategias y jurados de forma aleatoria.
- **Selección**: Los individuos con mejor aptitud, es decir, las combinaciones que obtienen veredictos más favorables, son seleccionados para la próxima generación. Se utilizó la estrategia de ranking para esta acción, la cual consiste en ordenar a los individuos en base al fitness, de tal forma que se elijan los N individios que mejor fitness hayan tenido.
- **Cruce**: Los individuos seleccionados se cruzan entre sí para generar nuevos individuos (descendientes) que combinan las características de sus "padres". Para realizar este cruce se utlizó una heurística basada en el cruce en un punto, que consiste en partir en dos los alelos de los "padres" en un punto y así combinarlos. En esta simulación, al tener como variables del algoritmo genético a los jurados, no es posible repetir el id que los identifica en variables de un mismo individuo, por lo que la información después del punto de cruzamiento se ordena como está ordenada en el otro padre. Por ejemplo, si nuestros dos padres son ABCDEFGHI e IGAHFDBEC y nuestro punto de cruzamiento se establece después del cuarto carácter, entonces los hijos que resultan serían ABCDIGHFE e IGAHBCDEF.
- **Mutación**: La mutación introduce cambios aleatorios para generar diversidad en las nuevas generaciones y evitar la convergencia prematura. En este caso, solo se cambia un alelo de forma aleatoria, por cada individuo de la población.
- **Reemplazo**: La nueva población reemplaza a la anterior, y el proceso se repite durante varias generaciones, buscando una mejora continua en la calidad de las combinaciones.

En cada iteración, el sistema busca maximizar el valor del veredicto, es decir, que las estrategias implementadas por los abogados logren impactar favorablemente en los testigos y que los jurados seleccionados respondan de manera óptima. A medida que el algoritmo progresa, las combinaciones que logran mejores veredictos sobreviven y mejoran la simulación del juicio.

#### Resultados esperados

A través de este proceso iterativo, el algoritmo genético identifica las configuraciones más exitosas, proporcionando a los abogados una guía sobre qué estrategias son más efectivas y qué perfiles de jurados tienden a responder mejor bajo determinadas circunstancias. Este enfoque permite mejorar la precisión y realismo de la simulación del juicio, ofreciendo una herramienta poderosa para estudiar y prever resultados en escenarios legales complejos.

### LLM:
Como durante los juicios se reúnen una serie de datos de lo que ocurre(estrategias que aplica el abogado, las reacciones del testigo a estas estrategias, intervenciones en la deliberación del jurado, etc), se utiliza un LLM para que escriba un resumen de los acontecimientos del juicio a modo de cronista o corresponsal. Para esto se utilizó el modelo "gemini-1.5-flash", que es gratis y al cual se puede acceder a través de una api key que también se puede crear de forma gratis.

