'''
Created on Oct 20, 2014

@authors: 
    Garrido Alan
    Henkel Magnus

@summary: 
    Programa que crea una serie de proceso con un determinado instante de inicio y una duración
    (ambos aleatorios) y que evalua los parámetros de 'Total', 'Idle' y 'Penalización'. Se define:
    Total = tiempo que toma el trabajo con tiempo de espera incluido
    Idle = tiempo en espera
    Penalización = Fracción de tiempo de respuesta durante P estuvo en espera.
    
    El programa arroja 3 estadísticas para los 3 algoritmos y calcula los promedios para el total, 
    el tiempo idle y la penalización. 
    
    La creación de los procesos es aleatoria, es decir que los tiempos de llegada y ejecución se 
    determinan aleatoriamente. Sin embargo, los procesos vienen en orden, es decir que el proceso 
    A llega antes que B, B antes que C, etc.
'''

from random import randrange

def testdummy(inp_list):
    '''
    La clase testdummy(list) sirve para testing.
    Recibe una lista con valres de los que se conozca el resultado y con esto se compruebe el correcto
    funcionamiento del programa.
    '''
    # comentar esta lista para pasar una lista propia
    inp_list = [(0, 6), (1, 10), (4, 4), (9, 9), (12, 8)]

    p_list = []
    A = VirtualProcess(*inp_list[0])
    A.name = 'A'
    p_list.append(A)

    B = VirtualProcess(*inp_list[1])
    B.name = 'B'
    p_list.append(B)

    C = VirtualProcess(*inp_list[2])
    C.name = 'C'
    p_list.append(C)

    D = VirtualProcess(*inp_list[3])
    D.name = 'D'
    p_list.append(D)

    E = VirtualProcess(*inp_list[4])
    E.name = 'E'
    p_list.append(E)
    
    return p_list

class VirtualProcess():
    '''
    La clase VirtualProcess sirve solamente para guardar los valores de cada proceso virtual. Se
    inicializa cada objeto de un proceso virtual con dos parámetros: el tiempo de llegada y el
    tiempo que se va a ejecutar. El nombre se le da posteriormente para la impresión de las estadísticas.
    '''
    def __init__(self, time_of_arrival, execution_time):
        self.name = '' 
        self.time_of_arrival = time_of_arrival
        self.execution_countdown = execution_time
        self.execution_time = execution_time
        self.tot_time = 0
        self.wait_time = 0
        self.t_resp_wait = 0

def create_virtual_processes():
    '''
    Esta función crea los procesos virtuales con valores de tiempo de llegada y de tiempo de
    ejecución aleatorios. Se crean 5 procesos y se les da nombres desde A a E, A llega primero,
    después B, C, D y al final E.
    La variable hook_in determina el valor a partir del cual se generan tiempos de llegada para
    procesos posteriores. Esto asegura que proceso B no llegue antes que proceso A, etc
    '''
    global wait_time_all
    # la variable hook_in (enganche) guarda el límite máximo del rango de valores del proceso anterior
    # y lo pone como límite mínimo para el tiempo de llegada para siguiente proceso. Así se 
    # mantiene el orden de llegada. Los nombres de los procesos se asignan dinámicamente a 
    # través del código ASCII
    hook_in = 0
    process_list = []

    for count in range(5):
        f_name = VirtualProcess(*randomize_process_parameters(hook_in, process_list))
        f_name.name = chr(count + 65)
        hook_in = f_name.time_of_arrival + 1
        process_list.append(f_name)

    return process_list

def randomize_process_parameters(start_val, process_list):
    '''
    Función auxiliar a la función create_virtual_processes().
    Aquí es donde ocurre la generación de los valores mimos. Si la lista de procesos está vacia
    quiere decir que llega el proceso A que no tiene que esperar ya que llega primero. Por lo tanto
    el tiempo de llega es '0'
    '''
    if not process_list:
        return (0, randrange(15) + 3)
    else:
        return (randrange(start_val, start_val + 7), randrange(15) + 3)

def caller():
    '''
    Función que llama a los diferentes algoritmos con la misma lista de procesos.
    Al final de cada llamada de un algoritmo llama a la función 'statistics' para
    imprimir los resultados y cálculos.
    '''
    global process_list
    
    print('=' * 65)
    
    for iter in range(3):
        process_list = create_virtual_processes()

        first_comes_first_served(process_list)
        statistics(process_list, "\n++++++ First Comes First Served ++++++")

        round_robin(process_list)
        statistics(process_list, "\n++++++ Round Robin +++++++")
        
        shortest_next(process_list)
        statistics(process_list, "\n++++++ Shortest Process Next ++++++")
        
        print()
        print('=' * 65)
        

def first_comes_first_served(process_list):
    '''
    Algoritmo First-Comes-First-Served
    '''
    # variable que guarda el tiempo de ejecución y idle time
    # de todos los procesos anteriores, es efectivamente el 
    # tiempo de espera para el último proceso 
    wait_time_all = 0

    # se copia la lista para no tocar el original
    process_list_copy = process_list[:]

    while process_list_copy:
        current_process = process_list_copy.pop(0)

        # calcula el tiempo que haya tenido que esperar un proceso hasta que sea atendido
        current_process.wait_time = wait_time_all - current_process.time_of_arrival

        # si los tiempos de espera son negativos quiere decir que el proceso no tuvo que esperar
        if current_process.wait_time < 0:
            current_process.wait_time = 0
        wait_time_all = wait_time_all + current_process.execution_time

        # se actualizan las estadísticas
        current_process.tot_time = current_process.wait_time + current_process.execution_time 
        current_process.t_resp_wait = (current_process.tot_time / current_process.execution_time) 


def round_robin(process_list):
    '''
    Algortimo Round Robin
    '''
    wait_time_all = 0

    process_list_copy = process_list[:]
    
    while process_list_copy:
        current_process = process_list_copy.pop(0)
        
        # se comprueba si un proceso tuvo que esperar o no.
        # si hubo espera entonces se calcula el hueco (idle time) y se  adelanta el tiempo de
        # llegada del proceso
        if wait_time_all < current_process.time_of_arrival:
            current_process.time_of_arrival = current_process.time_of_arrival - \
                (current_process.time_of_arrival - wait_time_all)
         
        # si el valor de la operacón anterior es positivo quiere decir que va a ejecutar
        # los 4 quantums completos
        if current_process.execution_countdown > 4:
            current_process.execution_countdown = current_process.execution_countdown - 4
            process_list_copy.append(current_process)
            wait_time_all = wait_time_all + 4
            

        # si el valor de la operación anterior es negativo se calcula el tiempo que le queda 
        # al proceso y solamente estos quantums se suma al tiempo total de ejecución
        elif current_process.execution_countdown < 4:
            current_process.execution_countdown = current_process.execution_countdown - 4
            wait_time_all = wait_time_all + (4 - abs(current_process.execution_countdown))
            current_process.execution_countdown = 0

        # si el valor de la operación anterior es  igual a 4 (el número de quantums por 
        # tiempo de ejecución) entonces ya terminó este proceso
        elif current_process.execution_countdown == 4:
            wait_time_all = wait_time_all + 4
            current_process.execution_countdown = 0

        current_process.tot_time = wait_time_all - current_process.time_of_arrival
        current_process.wait_time = current_process.tot_time - current_process.execution_time
        current_process.t_resp_wait = current_process.tot_time / current_process.execution_time

def shortest_next(process_list):
    '''
    Algoritmo Shortest Process Next
    '''
    wait_time_all = 0
    process_list_copy = process_list[:]

    while process_list_copy:
        concurrent_processes = []
        # se ejecuta el primer proceso de la lista
        current_process = process_list_copy.pop(0)
        # los demás procesos se agregan a una lista nueva
        other_processes = process_list_copy[:]

        # se calcula el tiempo de espera para el proceso en ejecución
        current_process.wait_time = wait_time_all - current_process.time_of_arrival
        
        # si los tiempos de espera son negativos quiere decir que el proceso no tuvo que esperar
        if current_process.wait_time < 0:
            current_process.wait_time = 0
            
        # se actualizan las estadísticas para el proceso en ejecution, después éste desaparece para siempre
        current_process.tot_time = current_process.execution_time + current_process.wait_time
        current_process.t_resp_wait = current_process.tot_time / current_process.execution_time
        
        wait_time_all = wait_time_all + current_process.execution_time

        # para el proceso en ejecución se checa los procesos que son concurrentes.
        # y se agregan a una lista
        for item in other_processes: 
            if item.time_of_arrival < wait_time_all:
                concurrent_processes.append(item)

        # se ordena la lista de procesos concurrentes del proceso en ejecución por el criterio del
        # tiempo de ejecución. Ahora se sabe que el primero de la lista es el siguiente que se 
        # va a ejecutar. Este proceso se inserta nuevamente a la lista de procesos en primer lugar. 
        # Por eso sabemos que va a ser elegido como siguiente.
        concurrent_processes.sort(key = lambda x: x.execution_time)
        
        if concurrent_processes:
            dispatched_process = concurrent_processes.pop(0)
            process_list_copy.remove(dispatched_process)
            process_list_copy.insert(0, dispatched_process) 

def statistics(process_list, message):
    '''
    La función 'statistics' imprime un mensaje de que algoritmo se trata y formatea la lista de
    procesos. Un proceso en este momento de la impresión tiene valores actualizados de un algoritmo
    que se ejecutó justo antes.
     '''
    t_average = 0
    i_average = 0
    p_average = 0

    print(message,'\n')
    print('Virtual    Time of    Execution   Total     Idle    Penalty\nProcess    Arrival    Time')
    print("_" * 60)
    for p in process_list:
        print(p.name, '\t  ', p.time_of_arrival, '\t     ', p.execution_time, '     \t ', p.tot_time, '\t   ', p.wait_time, '\t   ', '%.4f'%(p.t_resp_wait))
        t_average = t_average + float(p.tot_time)
        i_average = i_average + float(p.wait_time)
        p_average = p_average + float(p.t_resp_wait)

    print('_' * 60)
    print('Promedio:              ', '\t',  '%.2f'%(t_average / 5), '\t  ', '%.2f'%(i_average / 5), '  ', '%.2f'%(p_average / 5))

'''
Main
'''
process_list = create_virtual_processes()
caller()
