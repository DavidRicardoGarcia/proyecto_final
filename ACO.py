import math
import random
import time as tm
from tqdm import tqdm
from matplotlib import pyplot as plt
import json
import os.path
import pandas as pd
import numpy as np
import copy
import booking as book
import matplotlib
import matplotlib.pyplot as plt
funcion=book.planificador()

def terminado_algoritmo(res,tiempo,valor):
        
    save_path = '/home/david/Desktop/optimizacion_final/datos_json'

    name_of_file = 'estado'

    completeName = os.path.join(save_path, name_of_file+".txt") 

    with open(completeName) as json_file:
        data = json.load(json_file)

    data['ACO']['estado']='terminado'
    data['ACO']['resultado']=res
    data['ACO']['tiempo']=tiempo
    data['ACO']['valor']=valor

    #se ejecuta el algoritmo en cuestion

    with open(completeName,'w') as outfile:
        json.dump(data,outfile)

def charts(x,y):
        
    save_path = '/home/david/Desktop/optimizacion_final/datos_json'

    name_of_file = 'charts'

    completeName = os.path.join(save_path, name_of_file+".txt") 

    with open(completeName) as json_file:
        data = json.load(json_file)

    data['ACO']['y']=y
    data['ACO']['x']=x

    #se ejecuta el algoritmo en cuestion

    with open(completeName,'w') as outfile:
        json.dump(data,outfile)

def graficas_png(d,n,x,y):
    fig, ax = plt.subplots()
    ax.plot(x, y)

    ax.set(xlabel='gen (k)', ylabel='f (d)',
        title='cost function')
    ax.grid()

    s="ACOtest" +repr(d)+"-"+repr(n) + ".png"

    fig.savefig(s)

class ACO:

    def __init__(self, mode='ACS', colony_size=10, elitist_weight=1.0, min_scaling_factor=0.001, alpha=1.0, beta=3.0,
                 rho=0.1, pheromone_deposit_weight=1.0, initial_pheromone=1.0, steps=100, nodes=None, labels=None,tareas=None):

        self.tareas=tareas

        self.mode = mode
        self.colony_size = colony_size
        self.elitist_weight = elitist_weight
        self.min_scaling_factor = min_scaling_factor
        self.rho = rho
        self.pheromone_deposit_weight = pheromone_deposit_weight
        self.steps = steps
        self.num_nodes = len(nodes)
        self.nodes = nodes
        #se crean n aristas que conectan todos los nodos entre si
        self.edges = [[None] * self.num_nodes for _ in range(self.num_nodes)]

        #se da el valor inicial de weight a cada arista entre el nodo i-j y el nodo j-i. matriz de distancias
        for i in range(self.num_nodes):
            for j in range(i + 1, self.num_nodes):
                self.edges[i][j] = self.edges[j][i] = self.Edge(i, j, 1,
                                                                initial_pheromone)
        #se inicializan las n hormigas y se les pasa los nodos y la matriz de distancias
        self.ants = [self.Ant(alpha, beta, self.num_nodes, self.edges,tareas) for _ in range(self.colony_size)]
        self.global_best_tour = None
        self.global_best_distance = float("inf")

    def decode_position(self,state):

        cont=[int(0) for _ in range(self.num_mc)]
        for i in range(self.num_mc):
            for j in range(len(state)):
                if(state[j] == i):
                    cont[i]+=1
                    ultimo_valor=i
        return state[-1], cont[state[-1]]

    def _add_pheromone(self, tour, distance, weight=1.0):
        state=tour.copy()
        #el valor de 1/dij
        pheromone_to_add = self.pheromone_deposit_weight / distance
        #se actualiza el valor de feromonas entre cada lugar que va de i a j correspondiente al tour de cada hormiga
        for i in range(self.num_nodes):
            if(i>0):

                # u_v_a , cant_a= self.decode_position(state[:i])
                # u_v_b , cant_b= self.decode_position(state[:i+1])  
                # posicion_a=self.num_mc*u_v_a+cant_a-1
                # posicion_b=self.num_mc*u_v_b+cant_b-1
                self.edges[state[-2]][state[-1]].pheromone += weight * pheromone_to_add

    #clase para representar el comportamiento y atributos de cada hormiga
    class Ant:
        def __init__(self, alpha, beta, num_nodes, edges,tareas):

            #constantes de probabilidad 
            self.alpha = alpha
            self.beta = beta
            #nodos
            self.num_nodes = num_nodes
            #aristas
            self.edges = edges
            #valor inicial de tour y distancia total
            self.tour = None
            self.distance = 0.0
            self.tareas=tareas


        #seleccionar el nodo siguiente
        def _select_node(self):
            roulette_wheel = 0.0
            posibles=list(range(self.num_nodes))
            posible_neighborhood=[]
            #nodos posibles para la siguiente iteracion
            for i in range(self.num_nodes):
                cont=0
                for j in range(len(self.tour)):
                    if(self.tour[j] == i):
                        cont+=1
                if(cont < 1):
                    posible_neighborhood.append(i)
            #se revisa en la lista de nodos cuales son los siguientes que no estan en la lista de nodos visitados * cambiar esto
            #unvisited_nodes = [node for node in range(self.num_nodes) if node not in self.tour]
            unvisited_nodes=posible_neighborhood
            heuristic_total = 0.0
            dist_curr=self.calcular(self.tour)
            #suma la distancia desde el ultimo nodo guardado en el tour hasta los no visitados (sum nij)
            for unvisited_node in unvisited_nodes:
                new_tour=[]
                #posible error por no tener el copy
                new_tour=self.tour.copy()
                new_tour.append(unvisited_node)
                new_dist=self.calcular(new_tour)
                heuristic_total += new_dist-dist_curr
            #sum (tij^a* ((sum dil)/dij)^b)
            for unvisited_node in unvisited_nodes:

                new_tour=[]
                #posible error por no tener el copy
                new_tour=self.tour.copy()
                new_tour.append(unvisited_node)
                new_dist=self.calcular(new_tour)
                # u_v_a , cant_a= self.decode_position(self.tour)
                # u_v_b , cant_b= self.decode_position(new_tour)  
                # posicion_a=self.num_mc*u_v_a+cant_a-1
                # posicion_b=self.num_mc*u_v_b+cant_b-1
                distance=new_dist-dist_curr
                if distance == 0:
                    distance = 1e-10
                roulette_wheel += pow(self.edges[self.tour[-1]][new_tour[-1]].pheromone, self.alpha) * \
                                  pow((heuristic_total / (distance)), self.beta)
            #Funcion de probabilidad
            random_value = random.uniform(0.0, roulette_wheel)
            wheel_position = 0.0

            #probabilidad acumulativa para seleccionar el proximo nodo a visitar
            for unvisited_node in unvisited_nodes:

                new_tour=[]
                #posible error por no tener el copy
                new_tour=self.tour.copy()
                new_tour.append(unvisited_node)
                new_dist=self.calcular(new_tour)
                # u_v_a , cant_a= self.decode_position(self.tour)
                # u_v_b , cant_b= self.decode_position(new_tour)  
                # posicion_a=self.num_mc*u_v_a+cant_a-1
                # posicion_b=self.num_mc*u_v_b+cant_b-1
                distance=new_dist-dist_curr
                if distance == 0:
                    distance = 1e-10
                wheel_position += pow(self.edges[self.tour[-1]][new_tour[-1]].pheromone, self.alpha) * \
                                  pow((heuristic_total / (distance)), self.beta)
                if wheel_position >= random_value:
                    return unvisited_node

        def decode_position(self,state):

            cont=[int(0) for _ in range(self.num_mc)]
            for i in range(self.num_mc):
                for j in range(len(state)):
                    if(state[j] == i):
                        cont[i]+=1
                        ultimo_valor=i
            return state[-1], cont[state[-1]]

        #encuentra un tour para la hormiga
        def find_tour(self):
            #genera un entero aleatorio en el rango de 0 a nodos-1
            self.tour = [random.randint(0, self.num_nodes - 1)]
            #primero genera un punto de partida y comienza a construir el camino de la hormiga
            #hasta que la hormiga no haya pasado por todos los nodos
            while len(self.tour) < self.num_nodes:
                #va agregando un nuevo nodo en cada iteracion
                self.tour.append(self._select_node())
            return self.tour

        # este es el que tengo que cambiar por el algoritmo que evalua el vector
        def get_distance(self):
            self.distance=self.calcular(self.tour)
            return self.distance

        def calcular(self,state):

            x=self.ordenar_Tareas(state)
            a=funcion.Calcular_Costo(x)
            return a

        def ordenar_Tareas(self,state):
            h={}
            newtareas=[]
            for i in state:
                for x in self.tareas:
                    if(i == x['id']):
                        newtareas.append(x)
            h['pedidos']=newtareas
            return h

    #clase para guardar los atributos entre 2 nodos
    class Edge:
        def __init__(self, a, b, weight, initial_pheromone):
            self.a = a
            self.b = b
            # cambiar esto
            if weight == 0:
                weight = 1e-10
            self.weight = weight
            self.pheromone = initial_pheromone

    def _acs(self):
        self.makespan_record=[]
        self.index_record=[]
        for step in range(self.steps):
            for ant in self.ants:
                # calcula un tour para esa hormiga
                #calcula la distancia total del tour
                self._add_pheromone(ant.find_tour(),ant.get_distance())
                #si la distancia de la hormiga es menor que la global se actualizan los datos
                if ant.distance < self.global_best_distance:
                    self.global_best_tour = ant.tour
                    self.global_best_distance = ant.distance
            #se actualiza la cantida de feromona en los caminos (evaporacion)
            for i in range(self.num_nodes):
                for j in range(i + 1, self.num_nodes):
                    self.edges[i][j].pheromone *= (1.0 - self.rho)
            
            self.makespan_record.append(self.global_best_distance)
            self.index_record.append(step)

    def run(self):
        start = tm.time()
        # print('Started : {0}'.format(self.mode))
        if self.mode == 'ACS':
            self._acs()
        elif self.mode == 'Elitist':
            self._elitist()
        else:
            self._max_min()
        # print('Ended : {0}'.format(self.mode))
        # print('Sequence : <- {0} ->'.format(' - '.join(str(self.labels[i]) for i in self.global_best_tour)))
        # print('Total distance travelled to complete the tour : {0}\n'.format(round(self.global_best_distance, 2)))
        runtime = tm.time() - start
        return runtime, self.global_best_distance , self.global_best_tour



def get_id_list(lista):

    newlist=[]
    for i in lista:
        newlist.append(i['id'])
    return newlist
def cargar_tareas():
        save_path = '/home/david/Desktop/optimizacion_final/datos_json'
        name_of_file = 'data'
        completeName = os.path.join(save_path, name_of_file+".json") 
        with open(completeName) as json_file:
            clientes = json.load(json_file)
        return clientes


def ejecutarACO(d,n,k):

    #start_time = tm.time()
    _colony_size = 3
    _steps = k
    x=cargar_tareas()

    lista_id=get_id_list(x['pedidos'])


    acs=ACO(mode='ACS', colony_size=_colony_size, steps=_steps, nodes=lista_id, tareas=x['pedidos'])
    time, dist, tour =acs.run()

    s='el algoritmo ACS     :' + repr(dist) +" con tiempo de:" + repr(time) + " tour de: " + repr(tour)
    print(s)
    #print('the elapsed time:%s'% (tm.time() - start_time))
    terminado_algoritmo(tour,time,dist)
    #charts(acs.index_record,acs.makespan_record)
    #graficas_png(d,n,acs.index_record,acs.makespan_record)
    #print(_nodes)

ejecutarACO(1,1,1)