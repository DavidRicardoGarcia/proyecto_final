# -*- coding: utf-8 -*-
from __future__ import print_function
import math
import random
import time
import copy
import json
import os.path
# some_file.py
#import sys
# insert at 1, 0 is the script path (or '' in REPL)
#sys.path.insert(1, '/home/david/Desktop/optimizacion_final')
import Funcion_objetivo as fo

funcion=fo


def terminado_algoritmo(res):
        
    save_path = '/home/david/Desktop/optimizacion_final/datos_json'

    name_of_file = 'estado'

    completeName = os.path.join(save_path, name_of_file+".txt") 

    with open(completeName) as json_file:
        data = json.load(json_file)

    data['SA']['estado']='terminado'
    data['SA']['resultado']=res

    #se ejecuta el algoritmo en cuestion

    with open(completeName,'w') as outfile:
        json.dump(data,outfile)

def charts(x,y):
        
    save_path = '/home/david/Desktop/optimizacion_final/datos_json'

    name_of_file = 'charts'

    completeName = os.path.join(save_path, name_of_file+".txt") 

    with open(completeName) as json_file:
        data = json.load(json_file)

    data['SA']['y']=y
    data['SA']['x']=x

    #se ejecuta el algoritmo en cuestion

    with open(completeName,'w') as outfile:
        json.dump(data,outfile)

class SA():

    # pass extra data (the distance matrix) into the constructor
    def __init__(self, state,tareas):

        self.tareas=tareas
                # defaults
        self.Tmax = 25000.0
        self.Tmin = 2.5
        self.steps = 10000
        self.updates = 100
        self.copy_strategy = 'deepcopy'

        # placeholders
        self.state=state
        self.best_state = state
        self.best_energy = self.calcular()
        self.start = None

    def move(self):
        """Swaps two cities in the route."""
        # no efficiency gain, just proof of concept
        # demonstrates returning the delta energy (optional)
        initial_energy = self.energy()

        a = random.randint(0, len(self.state) - 1)
        b = random.randint(0, len(self.state) - 1)
        self.state[a], self.state[b] = self.state[b], self.state[a]

        return self.energy() - initial_energy

    def energy(self):
        """Calculates the length of the route."""
        e = 0
        e=self.calcular()
        return e
    
    def calcular(self):

        x=self.ordenar_Tareas()
        a=funcion.Calcular_Costo(x)
        return a

    def ordenar_Tareas(self):
        h={}
        newtareas=[]
        for i in self.state:
            for x in self.tareas:
                if(i == x['id']):
                    newtareas.append(x)
        h['pedidos']=newtareas
        return h

    def anneal(self):

        step = 0
        
        self.makespan_record=[]
        self.index_record=[]

        Tfactor = -math.log(self.Tmax / self.Tmin)

        # Note initial state
        T = self.Tmax
        E = self.energy()
        prevState = self.copy_state(self.state)
        prevEnergy = E
        self.best_state = self.copy_state(self.state)
        self.best_energy = E
        trials, accepts, improves = 0, 0, 0
        if self.updates > 0:
            updateWavelength = self.steps / self.updates
            #self.update(step, T, E, None, None)

        # Attempt moves to new states
        while step < self.steps:
            step += 1
            T = self.Tmax * math.exp(Tfactor * step / self.steps)
            dE = self.move()
            if dE is None:
                E = self.energy()
                dE = E - prevEnergy
            else:
                E += dE
            trials += 1
            if dE > 0.0 and math.exp(-dE / T) < random.random():
                # Restore previous state
                self.state = self.copy_state(prevState)
                E = prevEnergy
            else:
                # Accept new state and compare to best state
                accepts += 1
                if dE < 0.0:
                    improves += 1
                prevState = self.copy_state(self.state)
                prevEnergy = E
                if E < self.best_energy:
                    self.best_state = self.copy_state(self.state)
                    self.best_energy = E
            if self.updates > 1:
                if (step // updateWavelength) > ((step - 1) // updateWavelength):
                    trials, accepts, improves = 0, 0, 0
            self.makespan_record.append(self.best_energy)
            self.index_record.append(step)

        self.state = self.copy_state(self.best_state)


        # Return best state and energy
        return self.best_state, self.best_energy
        
    def copy_state(self, state):
        """Returns an exact copy of the provided state
        Implemented according to self.copy_strategy, one of

        * deepcopy : use copy.deepcopy (slow but reliable)
        * slice: use list slices (faster but only works if state is list-like)
        * method: use the state's copy() method
        """
        if self.copy_strategy == 'deepcopy':
            return copy.deepcopy(state)
        elif self.copy_strategy == 'slice':
            return state[:]
        elif self.copy_strategy == 'method':
            return state.copy()
        else:
            raise RuntimeError('No implementation found for ' +
                               'the self.copy_strategy "%s"' %
                               self.copy_strategy)


        
def get_id_list(lista):

    newlist=[]
    for i in lista:
        newlist.append(i['id'])
    return newlist

if __name__ == '__main__':

    start_time = time.time()

    x=funcion.cargar_tareas()

    lista_id=get_id_list(x['pedidos'])

    tsp = SA(lista_id,x['pedidos'])
    # since our state is just a list, slice is the fastest way to copy
    tsp.copy_strategy = "slice"
    state, e = tsp.anneal()


    print()
    print("%i es el makespan total" % e)
    print("la mejor secuencia es")
    print(state)
    print('the elapsed time:%s'% (time.time() - start_time))
    terminado_algoritmo(state)
    charts(tsp.index_record,tsp.makespan_record)

# '''--------plot gantt chart-------'''
# import pandas as pd
# import chart_studio.plotly as py
# import plotly.figure_factory as ff
# import datetime
# from  plotly.offline import plot

# m_keys=[j+1 for j in range(num_mc)]
# j_keys=[j for j in range(num_job)]
# key_count={key:0 for key in j_keys}
# j_count={key:0 for key in j_keys}
# m_count={key:0 for key in m_keys}
# j_record={}
# for i in state:
#     gen_t=int(pt[i][key_count[i]])
#     gen_m=int(ms[i][key_count[i]])
#     j_count[i]=j_count[i]+gen_t
#     m_count[gen_m]=m_count[gen_m]+gen_t
    
#     if m_count[gen_m]<j_count[i]:
#         m_count[gen_m]=j_count[i]
#     elif m_count[gen_m]>j_count[i]:
#         j_count[i]=m_count[gen_m]
    
#     start_time=str(datetime.timedelta(seconds=j_count[i]-pt[i][key_count[i]])) # convert seconds to hours, minutes and seconds
#     end_time=str(datetime.timedelta(seconds=j_count[i]))
        
#     j_record[(i,gen_m)]=[start_time,end_time]
    
#     key_count[i]=key_count[i]+1
        

# df=[]
# for m in m_keys:
#     for j in j_keys:
#         df.append(dict(Task='Machine %s'%(m), Start='2018-07-14 %s'%(str(j_record[(j,m)][0])), Finish='2018-07-14 %s'%(str(j_record[(j,m)][1])),Resource='Job %s'%(j+1)))
    
# fig = ff.create_gantt(df, index_col='Resource', show_colorbar=True, group_tasks=True, showgrid_x=True, title='Job shop Schedule')
#plot(fig, filename='GA_job_shop_scheduling')

