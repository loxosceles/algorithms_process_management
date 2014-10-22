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

class VirtualProcess():
    def __init__(self, time_of_arrival, execution_time):
        self.name = '' 
        self.time_of_arrival = time_of_arrival
        self.execution_time = execution_time
        self.tot_time = 0
        self.wait_time = 0
        self.t_resp_wait = 0

def create_virtual_process(start_val):
    return (randrange(start_val, start_val + 7), randrange(15) + 3)

def print_table(process_list):
    for p in process_list:
        print(p.name, '\t\t  ', p.time_of_arrival, '\t\t     ', p.execution_time)

def first_comes_first_served(process_list):
    global wait_time_all
    process_list_copy = process_list[:]

    while process_list_copy:
        current_process = process_list_copy.pop(0)
        current_process.wait_time = wait_time_all - current_process.time_of_arrival

        if current_process.wait_time < 0:
            current_process.wait_time = 0
        
        if current_process.time_of_arrival <= current_process.execution_time:
            wait_time_all = wait_time_all + current_process.execution_time
        else:
            wait_time_all = wait_time_all + current_process.time_of_arrival

        current_process.tot_time = wait_time_all
        current_process.t_resp_wait = (current_process.tot_time / current_process.execution_time) 

def round_robin():
    pass

def shortest_next():
    pass

def statistics(message):
    print(message)
    print()
    print('Virtual Process    Time of Arrival    Execution Time\t T\t\t E\t\t P')
    print("_" * 100)
    for p in process_list:
        print(p.name, '\t\t  ', p.time_of_arrival, '\t\t     ', p.execution_time, '\t\t', p.tot_time, '\t\t', p.wait_time, '\t\t', '%.4f'%(p.t_resp_wait))


'''
Main
'''
for count in range(5):

    wait_time_all = 0
    hook_in = 0
    process_list = []

    A = VirtualProcess(hook_in, randrange(15) + 3)
    process_list.append(A)
    A.name = 'A'
    hook_in = A.time_of_arrival + 1

    B = VirtualProcess(*create_virtual_process(hook_in))
    process_list.append(B)
    B.name = 'B'
    hook_in = B.time_of_arrival + 1

    C = VirtualProcess(*create_virtual_process(hook_in))
    process_list.append(C)
    C.name = 'C'
    hook_in = C.time_of_arrival + 1

    D = VirtualProcess(*create_virtual_process(hook_in))
    process_list.append(D)
    D.name = 'D'
    hook_in = D.time_of_arrival + 1

    E = VirtualProcess(*create_virtual_process(hook_in))
    process_list.append(E)
    E.name = 'E'

    #print_table(process_list)

    first_comes_first_served(process_list)
    statistics("First Comes First Served")
#for count in range(len(process_list)):
    #f_name = count + 65 
    #f_name.name

#for letter in 'ABCDE':
#  print(letter, '\t\t  ', letter.time_of_arrival, '\t\t     ', letter.execution_time)
