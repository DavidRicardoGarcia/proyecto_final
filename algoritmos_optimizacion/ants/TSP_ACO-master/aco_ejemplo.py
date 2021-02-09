import math
import random
import time as tm
from tqdm import tqdm
from matplotlib import pyplot as plt

import pandas as pd
import numpy as np
import copy

class ACO:

    def __init__(self, mode='ACS', colony_size=10, elitist_weight=1.0, min_scaling_factor=0.001, alpha=1.0, beta=3.0,
                 rho=0.1, pheromone_deposit_weight=1.0, initial_pheromone=1.0, steps=100, nodes=None, labels=None,mtiempo=None,morden=None,nj=None,nm=None):

        self.pt=mtiempo
        self.ms=morden
        self.num_job=nj
        self.num_mc=nm
        self.num_gen=nj*nm

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
        self.ants = [self.Ant(alpha, beta, self.num_nodes, self.edges,mtiempo,morden,nm,nj) for _ in range(self.colony_size)]
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

                u_v_a , cant_a= self.decode_position(state[:i])
                u_v_b , cant_b= self.decode_position(state[:i+1])  
                posicion_a=self.num_mc*u_v_a+cant_a-1
                posicion_b=self.num_mc*u_v_b+cant_b-1
                self.edges[posicion_a][posicion_b].pheromone += weight * pheromone_to_add

    #clase para representar el comportamiento y atributos de cada hormiga
    class Ant:
        def __init__(self, alpha, beta, num_nodes, edges,pt,ms,nm,nj):

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
            self.num_mc=nm
            self.num_job=nj
            self.pt=pt
            self.ms=ms


        #seleccionar el nodo siguiente
        def _select_node(self):
            roulette_wheel = 0.0
            posibles=list(range(self.num_mc))
            posible_neighborhood=[]
            #nodos posibles para la siguiente iteracion
            for i in range(self.num_mc):
                cont=0
                for j in range(len(self.tour)):
                    if(self.tour[j] == i):
                        cont+=1
                if(cont < num_mc):
                    posible_neighborhood.append(i)
            #se revisa en la lista de nodos cuales son los siguientes que no estan en la lista de nodos visitados * cambiar esto
            #unvisited_nodes = [node for node in range(self.num_nodes) if node not in self.tour]
            unvisited_nodes=posible_neighborhood
            heuristic_total = 0.0
            dist_curr=self.calcular_makespan(self.tour)
            #suma la distancia desde el ultimo nodo guardado en el tour hasta los no visitados (sum nij)
            for unvisited_node in unvisited_nodes:
                new_tour=[]
                #posible error por no tener el copy
                new_tour=self.tour.copy()
                new_tour.append(unvisited_node)
                new_dist=self.calcular_makespan(new_tour)
                heuristic_total += new_dist-dist_curr
            #sum (tij^a* ((sum dil)/dij)^b)
            for unvisited_node in unvisited_nodes:

                new_tour=[]
                #posible error por no tener el copy
                new_tour=self.tour.copy()
                new_tour.append(unvisited_node)
                new_dist=self.calcular_makespan(new_tour)
                u_v_a , cant_a= self.decode_position(self.tour)
                u_v_b , cant_b= self.decode_position(new_tour)  
                posicion_a=self.num_mc*u_v_a+cant_a-1
                posicion_b=self.num_mc*u_v_b+cant_b-1
                distance=new_dist-dist_curr
                if distance == 0:
                    distance = 1e-10
                roulette_wheel += pow(self.edges[posicion_a][posicion_b].pheromone, self.alpha) * \
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
                new_dist=self.calcular_makespan(new_tour)
                u_v_a , cant_a= self.decode_position(self.tour)
                u_v_b , cant_b= self.decode_position(new_tour)  
                posicion_a=self.num_mc*u_v_a+cant_a-1
                posicion_b=self.num_mc*u_v_b+cant_b-1
                distance=new_dist-dist_curr
                if distance == 0:
                    distance = 1e-10
                wheel_position += pow(self.edges[posicion_a][posicion_b].pheromone, self.alpha) * \
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
            self.tour = [random.randint(0, self.num_mc - 1)]
            #primero genera un punto de partida y comienza a construir el camino de la hormiga
            #hasta que la hormiga no haya pasado por todos los nodos
            while len(self.tour) < self.num_nodes:
                #va agregando un nuevo nodo en cada iteracion
                self.tour.append(self._select_node())
            return self.tour

        # este es el que tengo que cambiar por el algoritmo que evalua el vector
        def get_distance(self):

            j_keys=[j for j in range(self.num_job)]
            key_count={key:0 for key in j_keys}
            j_count={key:0 for key in j_keys}
            m_keys=[j+1 for j in range(self.num_mc)]
            m_count={key:0 for key in m_keys}

            for i in self.tour:
                gen_t=int(self.pt[i][key_count[i]])
                gen_m=int(self.ms[i][key_count[i]])
                j_count[i]=j_count[i]+gen_t
                m_count[gen_m]=m_count[gen_m]+gen_t
                
                if m_count[gen_m]<j_count[i]:
                    m_count[gen_m]=j_count[i]
                elif m_count[gen_m]>j_count[i]:
                    j_count[i]=m_count[gen_m]
                
                key_count[i]=key_count[i]+1

            makespan=max(j_count.values())
            self.distance=makespan
            return makespan


        def calcular_makespan(self,state):

            j_keys=[j for j in range(self.num_job)]
            key_count={key:0 for key in j_keys}
            j_count={key:0 for key in j_keys}
            m_keys=[j+1 for j in range(self.num_mc)]
            m_count={key:0 for key in m_keys}

            for i in state:
                gen_t=int(self.pt[i][key_count[i]])
                gen_m=int(self.ms[i][key_count[i]])
                j_count[i]=j_count[i]+gen_t
                m_count[gen_m]=m_count[gen_m]+gen_t
                
                if m_count[gen_m]<j_count[i]:
                    m_count[gen_m]=j_count[i]
                elif m_count[gen_m]>j_count[i]:
                    j_count[i]=m_count[gen_m]
                
                key_count[i]=key_count[i]+1

            makespan=max(j_count.values())
            return makespan


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
        return runtime, self.global_best_distance, self.global_best_tour

class jobs:

    def __init__(self,j,o,i):
        self.job=j
        self.ope=o
        self.index=i





if __name__ == '__main__':

    _colony_size = 40
    _steps = 100
    #_nodes = [(random.uniform(-400, 400), random.uniform(-400, 400)) for _ in range(0, 10)]
    pt_tmp=pd.read_excel("JSP_dataset.xlsx",sheet_name="Processing Time",index_col =[0]) # processing time in excel 
    ms_tmp=pd.read_excel("JSP_dataset.xlsx",sheet_name="Machines Sequence",index_col =[0]) # machines sequence in excel

    dfshape=pt_tmp.shape # matrix shape
    num_mc=dfshape[1] # number of machines
    num_job=dfshape[0] # number of jobs
    num_gene=num_mc*num_job # number of genes in a chromosome

    pt=[list(map(int, pt_tmp.iloc[i])) for i in range(num_job)]
    ms=[list(map(int,ms_tmp.iloc[i])) for i in range(num_job)]

    #crear nodos del grafo
    jl=[]
 
    for i in range(num_job):
        for j in range(num_mc):
            jl.append(jobs(str(i),ms[i][j],j))
 

  
    acs=ACO(mode='ACS', colony_size=_colony_size, steps=_steps, nodes=jl, mtiempo=pt, morden=ms, nj=num_job, nm=num_mc)
    time, dist, tour =acs.run()

    s='el algoritmo ACS     :' + repr(dist) +" con tiempo de:" + repr(time) + " para la combinación: " + repr(tour)
    print(s)

    #print(_nodes)