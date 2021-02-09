# -*- coding: utf-8 -*-
from __future__ import print_function
import math
import random
from simanneal import Annealer
import pandas as pd
import numpy as np
import time
import copy



class TravellingSalesmanProblem(Annealer):

    """Test annealer with a travelling salesman problem.
    """

    # pass extra data (the distance matrix) into the constructor
    def __init__(self, state, num_job,num_mc,pt,ms):
        self.num_job=num_job
        self.num_mc=num_mc
        self.pt=pt
        self.ms=ms
        super(TravellingSalesmanProblem, self).__init__(state)  # important!

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
        e=self.calcular_makespan()
        return e
    
    def calcular_makespan(self):

        j_keys=[j for j in range(self.num_job)]
        key_count={key:0 for key in j_keys}
        j_count={key:0 for key in j_keys}
        m_keys=[j+1 for j in range(self.num_mc)]
        m_count={key:0 for key in m_keys}

        for i in self.state:
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
        #chrom_fitness.append(1/makespan)
        #chrom_fit.append(makespan)
        #total_fitness=total_fitness+chrom_fitness[m]
        

if __name__ == '__main__':

    pt_tmp=pd.read_excel("JSP_dataset.xlsx",sheet_name="Processing Time",index_col =[0]) # processing time in excel 
    ms_tmp=pd.read_excel("JSP_dataset.xlsx",sheet_name="Machines Sequence",index_col =[0]) # machines sequence in excel

    dfshape=pt_tmp.shape # matrix shape
    num_mc=dfshape[1] # number of machines
    num_job=dfshape[0] # number of jobs
    num_gene=num_mc*num_job # number of genes in a chromosome

    pt=[list(map(int, pt_tmp.iloc[i])) for i in range(num_job)]
    ms=[list(map(int,ms_tmp.iloc[i])) for i in range(num_job)]

    nxm_random_num=list(np.random.permutation(num_gene))
    job_order=nxm_random_num
    for j in range(num_gene):
        job_order[j]=job_order[j]%num_job


    tsp = TravellingSalesmanProblem(job_order,num_job,num_mc,pt,ms)
    tsp.set_schedule(tsp.auto(minutes=0.2))
    # since our state is just a list, slice is the fastest way to copy
    tsp.copy_strategy = "slice"
    state, e = tsp.anneal()


    print()
    print("%i es el makespan total" % e)
    print("la mejor secuencia es")
    print(state)

'''--------plot gantt chart-------'''
import pandas as pd
import chart_studio.plotly as py
import plotly.figure_factory as ff
import datetime
from  plotly.offline import plot

m_keys=[j+1 for j in range(num_mc)]
j_keys=[j for j in range(num_job)]
key_count={key:0 for key in j_keys}
j_count={key:0 for key in j_keys}
m_count={key:0 for key in m_keys}
j_record={}
for i in state:
    gen_t=int(pt[i][key_count[i]])
    gen_m=int(ms[i][key_count[i]])
    j_count[i]=j_count[i]+gen_t
    m_count[gen_m]=m_count[gen_m]+gen_t
    
    if m_count[gen_m]<j_count[i]:
        m_count[gen_m]=j_count[i]
    elif m_count[gen_m]>j_count[i]:
        j_count[i]=m_count[gen_m]
    
    start_time=str(datetime.timedelta(seconds=j_count[i]-pt[i][key_count[i]])) # convert seconds to hours, minutes and seconds
    end_time=str(datetime.timedelta(seconds=j_count[i]))
        
    j_record[(i,gen_m)]=[start_time,end_time]
    
    key_count[i]=key_count[i]+1
        

df=[]
for m in m_keys:
    for j in j_keys:
        df.append(dict(Task='Machine %s'%(m), Start='2018-07-14 %s'%(str(j_record[(j,m)][0])), Finish='2018-07-14 %s'%(str(j_record[(j,m)][1])),Resource='Job %s'%(j+1)))
    
fig = ff.create_gantt(df, index_col='Resource', show_colorbar=True, group_tasks=True, showgrid_x=True, title='Job shop Schedule')
plot(fig, filename='GA_job_shop_scheduling')

