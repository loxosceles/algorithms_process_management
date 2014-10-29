'''
Created on Oct 20, 2014

@authors: 
    Garrido Alan
    Henkel Magnus

@summary: 
    Programa que crea una serie de proceso con un determinado instante de inicio y una duración
    (ambos aleatorios) y que evalua los parámetros de 'T', 'E' y 'P'. Se define:
    T = tiempo que toma el trabajo con tiempo de espera incluido
    E = tiempo en espera
    P = Fracción de tiempo de respuesta durante P estuvo en espera.
'''

from random import randrange
from time import sleep

'''
def print_table(process_list):
    for p in process_list:
        print(p.name, '\t\t  ', p.time_of_arrival, '\t\t     ', p.execution_time)
    print()
'''

def testdummy():
    p_list = []
    A = VirtualProcess(0, 6)
    A.name = 'A'
    p_list.append(A)

    B = VirtualProcess(1, 10)
    B.name = 'B'
    p_list.append(B)

    C = VirtualProcess(4, 4)
    C.name = 'C'
    p_list.append(C)

    D = VirtualProcess(9, 9)
    D.name = 'D'
    p_list.append(D)

    E = VirtualProcess(12, 8)
    E.name = 'E'
    p_list.append(E)
    
    return p_list

def testdummy1():
    p_list = []
    A = VirtualProcess(0, 3)
    A.name = 'A'
    p_list.append(A)

    B = VirtualProcess(6, 15)
    B.name = 'B'
    p_list.append(B)

    C = VirtualProcess(11, 14)
    C.name = 'C'
    p_list.append(C)

    D = VirtualProcess(13, 3)
    D.name = 'D'
    p_list.append(D)

    E = VirtualProcess(15, 14)
    E.name = 'E'
    p_list.append(E)
    
    return p_list

def testdummy2():
    p_list = []
    A = VirtualProcess(0, 11)
    A.name = 'A'
    p_list.append(A)

    B = VirtualProcess(7, 11)
    B.name = 'B'
    p_list.append(B)

    C = VirtualProcess(10, 3)
    C.name = 'C'
    p_list.append(C)

    D = VirtualProcess(17, 13)
    D.name = 'D'
    p_list.append(D)

    E = VirtualProcess(21, 6)
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
    #global hook_in 
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
        statistics(process_list, "\nFirst Comes First Served")

        round_robin(process_list)
        statistics(process_list, "\nRound Robin")
        
        shortest_next(process_list)
        statistics(process_list, "\nShortest Process Next")
        
        print()
        print('=' * 65)
        

def first_comes_first_served(process_list):
    '''
    Algoritmo First-Comes-First-Served
    '''
    wait_time_all = 0

    process_list_copy = process_list[:]

    while process_list_copy:
        current_process = process_list_copy.pop(0)

        # calcula el tiempo que haya tenido que esperar un proceso hasta que sea atendido
        current_process.wait_time = wait_time_all - current_process.time_of_arrival

        if current_process.wait_time < 0:
            current_process.wait_time = 0
        wait_time_all = wait_time_all + current_process.execution_time

        current_process.tot_time = current_process.wait_time + current_process.execution_time 
        current_process.t_resp_wait = (current_process.tot_time / current_process.execution_time) 


def round_robin(process_list):
    '''
    Algortimo Round Robin
    '''

    # variable que guarda el tiempo de ejecución y idle time
    # de todos los procesos anteriores, es efectivamente el 
    # tiempo de espera para el último proceso 
    wait_time_all = 0

    process_list_copy = process_list[:]
    
    while process_list_copy:
        current_process = process_list_copy.pop(0)
        
        if wait_time_all < current_process.time_of_arrival:
            current_process.time_of_arrival = current_process.time_of_arrival - \
                (current_process.time_of_arrival - wait_time_all)
         
        if current_process.execution_countdown > 4:
            current_process.execution_countdown = current_process.execution_countdown - 4
            process_list_copy.append(current_process)
            wait_time_all = wait_time_all + 4
            

        elif current_process.execution_countdown < 4:
            current_process.execution_countdown = current_process.execution_countdown - 4
            wait_time_all = wait_time_all + (4 - abs(current_process.execution_countdown))
            current_process.execution_countdown = 0

        elif current_process.execution_countdown == 4:
            wait_time_all = wait_time_all + 4
            current_process.execution_countdown = 0

        current_process.tot_time = wait_time_all - current_process.time_of_arrival
        current_process.wait_time = current_process.tot_time - current_process.execution_time
        current_process.t_resp_wait = current_process.tot_time / current_process.execution_time

def print_plist(plist, message): 
    print(message)
    for item in plist:
        print("Name: ", item.name, "Arr.Time", item.time_of_arrival, "Exec.Time", item.execution_time)

def shortest_next(process_list):
    '''
    TODO: Algoritmo Shortest Process Next
    '''
    
    wait_time_all = 0
    process_list_copy = process_list[:]
    
    #print_plist(process_list_copy, "\nAfter processs_list_copy assignment")

    while process_list_copy:
        concurrent_processes = []
        current_process = process_list_copy.pop(0)
        #print("-------")
        #print("\nCurrent before check: ", current_process.name)
        #print("-------")
        other_processes = process_list_copy[:]
        #print_plist(other_processes, "Others unsorted: ")

        current_process.wait_time = wait_time_all - current_process.time_of_arrival
        
        if current_process.wait_time < 0:
            current_process.wait_time = 0
            
        current_process.tot_time = current_process.execution_time + current_process.wait_time
        current_process.t_resp_wait = current_process.tot_time / current_process.execution_time
        
        wait_time_all = wait_time_all + current_process.execution_time
        #print('\nInside while after wait_time_all set: ', wait_time_all)

        for item in other_processes: 
            #print("Inside for, Item name: ", item.name)
            #if item.time_of_arrival < wait_time_all and item.time_of_arrival > wait_time_all_before_current:
            if item.time_of_arrival < wait_time_all:
                concurrent_processes.append(item)
        #        print(item.name, " appended")

        concurrent_processes.sort(key = lambda x: x.execution_time)
        #print("\nconcurrent processes of process: ", current_process.name)
        
        #print_plist(concurrent_processes, "Concurrent processes: ")

        if concurrent_processes:
            dispatched_process = concurrent_processes.pop(0)
            process_list_copy.remove(dispatched_process)
            process_list_copy.insert(0, dispatched_process) 
        #print_plist(process_list_copy, "New process_list_copy")

def statistics(process_list, message):
    '''
    La función 'statistics' imprime un mensaje de que algoritmo se trata y formatea la lista de
    procesos. Un proceso en este momento de la impresión tiene valores actualizados de un algoritmo
    que se ejecutó justo antes.
     '''
    t_average = 0
    e_average = 0
    p_average = 0

    print(message,'\n')
    print('Virtual    Time of    Execution    T         E            P\nProcess    Arrival    Time')
    print("_" * 65)
    for p in process_list:
        print(p.name, '\t  ', p.time_of_arrival, '\t     ', p.execution_time, '\t ', p.tot_time, '\t    ', p.wait_time, ' \t', '%.4f'%(p.t_resp_wait))
        t_average = t_average + float(p.tot_time)
        e_average = e_average + float(p.wait_time)
        p_average = p_average + float(p.t_resp_wait)

    print('_' * 65)
    print('Promedio: \t\t\t ',  '%.2f'%(t_average / 5), '    ', '%.2f'%(e_average / 5), '\t', '%.2f'%(p_average / 5))


'''
Main
'''

process_list = create_virtual_processes()
caller()

#process_listB = testdummy1()
#first_comes_first_served(process_listB)
#statistics(process_listB, 'tst')

#process_listA = testdummy2()
#round_robin(process_listA)
#shortest_next(process_listA)
#statistics(process_listA, 'test')

#statistics(process_listA, 'test')
