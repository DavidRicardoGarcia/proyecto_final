# -*- coding: utf-8 -*-
"""
Created on Fri Jul 13 17:24:51 2018
Author: cheng-man wu
LinkedIn: www.linkedin.com/in/chengmanwu
Github: https://github.com/wurmen
"""

'''==========Solving job shop scheduling problem by gentic algorithm in python======='''
# importing required modules
import pandas as pd
import numpy as np
import time
import copy
import json
import os.path
import Funcion_objetivo as fo

funcion=fo

''' ================= initialization setting ======================'''

def get_id_list(lista):

    newlist=[]
    for i in lista:
        newlist.append(i['id'])
    return newlist

def calcular(state,tareas):

    x=ordenar_Tareas(state,tareas)
    a=funcion.Calcular_Costo(x)
    return a

def ordenar_Tareas(state,tareas):
    h={}
    newtareas=[]
    for i in state:
        for x in tareas:
            if(i == x['id']):
                newtareas.append(x)
    h['pedidos']=newtareas
    return h

def terminado_algoritmo(res):
        
    save_path = '/home/david/Desktop/optimizacion_final/datos_json'

    name_of_file = 'estado'

    completeName = os.path.join(save_path, name_of_file+".txt") 

    with open(completeName) as json_file:
        data = json.load(json_file)

    data['GA']['estado']='terminado'
    data['GA']['resultado']=res

    #se ejecuta el algoritmo en cuestion

    with open(completeName,'w') as outfile:
        json.dump(data,outfile)

def charts(x,y):
        
    save_path = '/home/david/Desktop/optimizacion_final/datos_json'

    name_of_file = 'charts'

    completeName = os.path.join(save_path, name_of_file+".txt") 

    with open(completeName) as json_file:
        data = json.load(json_file)

    data['GA']['y']=y
    data['GA']['x']=x

    #se ejecuta el algoritmo en cuestion

    with open(completeName,'w') as outfile:
        json.dump(data,outfile)

x=funcion.cargar_tareas()

lista_id=get_id_list(x['pedidos'])

num_gene=len(lista_id) # number of genes in a chromosome

# raw_input is used in python 2
population_size=int(10) #int(input('Please input the size of population: ') or 30) # default value is 30
crossover_rate=float(0.8)#float(input('Please input the size of Crossover Rate: ') or 0.8) # default value is 0.8
mutation_rate=float(0.2)#float(input('Please input the size of Mutation Rate: ') or 0.2) # default value is 0.2
mutation_selection_rate=float(0.2)#float(input('Please input the mutation selection rate: ') or 0.2)
num_mutation_jobs=round(num_gene*mutation_selection_rate)
num_iteration=int(1000)#int(input('Please input number of iteration: ') or 2000) # default value is 2000
    
start_time = time.time()

'''==================== main code ==============================='''
'''----- generate initial population -----'''
Tbest=999999999999999
best_list,best_obj=[],[]
population_list=[]
makespan_record=[]
index_record=[]
# it generates a random permutation array for each one in the population
for i in range(population_size):
    nxm_random_num=list(np.random.permutation(num_gene)) # generate a random permutation of 0 to num_job*num_mc-1
    population_list.append(nxm_random_num) # add to the population_list
        
# se ejecutan las n iteraciones elegidas previamente
for n in range(num_iteration):
    Tbest_now=99999999999           
   
    '''-------- two point crossover --------'''
    parent_list=copy.deepcopy(population_list)
    offspring_list=copy.deepcopy(population_list)
    S=list(np.random.permutation(population_size)) # generate a random sequence to select the parent chromosome to crossover
    #crossover
    for m in range(int(population_size/2)):
        crossover_prob=np.random.rand()
        if crossover_rate>=crossover_prob:
            parent_1= population_list[S[2*m]][:]
            parent_2= population_list[S[2*m+1]][:]
            child_1=parent_1[:]
            child_2=parent_2[:]
            cutpoint=list(np.random.choice(num_gene, 2, replace=False))
            cutpoint.sort()
        
            child_1[cutpoint[0]:cutpoint[1]]=parent_2[cutpoint[0]:cutpoint[1]]
            child_2[cutpoint[0]:cutpoint[1]]=parent_1[cutpoint[0]:cutpoint[1]]
            offspring_list[S[2*m]]=child_1[:]
            offspring_list[S[2*m+1]]=child_2[:]
        
    
    '''----------repairment-------------'''
    for m in range(population_size):
        job_count={}
        larger,less=[],[] # 'larger' record jobs appear in the chromosome more than m times, and 'less' records less than m times.
        for i in range(len(lista_id)):
            if i in offspring_list[m]:
                count=offspring_list[m].count(i)
                pos=offspring_list[m].index(i)
                job_count[i]=[count,pos] # store the above two values to the job_count dictionary
            else:
                count=0
                job_count[i]=[count,0]
            if count>1:
                larger.append(i)
            elif count<1:
                less.append(i)
            1
                
        for k in range(len(larger)):
            chg_job=larger[k]
            while job_count[chg_job][0]>1:
                for d in range(len(less)):
                    if job_count[less[d]][0]<1:                    
                        offspring_list[m][job_count[chg_job][1]]=less[d]
                        job_count[chg_job][1]=offspring_list[m].index(chg_job)
                        job_count[chg_job][0]=job_count[chg_job][0]-1
                        job_count[less[d]][0]=job_count[less[d]][0]+1                    
                    if job_count[chg_job][0]==1:
                        break     
    
    '''--------mutation--------'''   
    for m in range(len(offspring_list)):
        mutation_prob=np.random.rand()
        if mutation_rate >= mutation_prob:
            m_chg=list(np.random.choice(num_gene, num_mutation_jobs, replace=False)) # chooses the position to mutation
            t_value_last=offspring_list[m][m_chg[0]] # save the value which is on the first mutation position
            for i in range(num_mutation_jobs-1):
                offspring_list[m][m_chg[i]]=offspring_list[m][m_chg[i+1]] # displacement
            
            offspring_list[m][m_chg[num_mutation_jobs-1]]=t_value_last # move the value of the first mutation position to the last mutation position
  
    
    '''--------fitness value(calculate makespan)-------------'''
    total_chromosome=copy.deepcopy(parent_list)+copy.deepcopy(offspring_list) # parent and offspring chromosomes combination
    chrom_fitness,chrom_fit=[],[]
    total_fitness=0

    for i in total_chromosome:
        makespan=calcular(i,x['pedidos'])
        chrom_fitness.append(1/makespan)
        chrom_fit.append(makespan)
        total_fitness=total_fitness+1/makespan

    
    '''----------selection(roulette wheel approach)----------'''
    pk,qk=[],[]
    
    for i in range(population_size*2):
        pk.append(chrom_fitness[i]/total_fitness)
    for i in range(population_size*2):
        cumulative=0
        for j in range(0,i+1):
            cumulative=cumulative+pk[j]
        qk.append(cumulative)
    
    selection_rand=[np.random.rand() for i in range(population_size)]
    
    for i in range(population_size):
        if selection_rand[i]<=qk[0]:
            population_list[i]=copy.deepcopy(total_chromosome[0])
        else:
            for j in range(0,population_size*2-1):
                if selection_rand[i]>qk[j] and selection_rand[i]<=qk[j+1]:
                    population_list[i]=copy.deepcopy(total_chromosome[j+1])
                    break
    '''----------comparison----------'''
    for i in range(population_size*2):
        if chrom_fit[i]<Tbest_now:
            Tbest_now=chrom_fit[i]
            sequence_now=copy.deepcopy(total_chromosome[i])
    if Tbest_now<=Tbest:
        Tbest=Tbest_now
        sequence_best=copy.deepcopy(sequence_now)
        
    makespan_record.append(Tbest)
    index_record.append(n)


'''----------result----------'''
print("optimal sequence",sequence_best)
print("optimal value:%f"%Tbest)
print('the elapsed time:%s'% (time.time() - start_time))
terminado_algoritmo(sequence_best)
charts(index_record,makespan_record)
# import matplotlib.pyplot as plt

# plt.plot([i for i in range(len(makespan_record))],makespan_record,'b')
# plt.ylabel('makespan',fontsize=15)
# plt.xlabel('generation',fontsize=15)
# plt.show()


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
# for i in sequence_best:
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
