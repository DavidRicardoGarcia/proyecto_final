import matplotlib
import matplotlib.pyplot as plt
import math

inf=math.inf
fig, ax = plt.subplots()

sa=[41.51,16.63,106.71,66.98,30.54]
pso=[39.94,inf,7.85,1.57,inf]
ga=[78.62,158.46,30.99,190.01,562.35]
aco=[inf,inf,inf,inf,inf ]

listamin=[]
listamin.append(min(sa))
listamin.append(min(pso))
listamin.append(min(ga))
listamin.append(min(aco))
cmin=min(listamin)
rsa=[numbers/cmin for numbers in sa]
rpso=[numbers/cmin for numbers in pso]
rga=[numbers/cmin for numbers in ga]
raco=[numbers/cmin for numbers in aco]
t=rsa+rpso+rga+raco
t.sort()
cont=0

tn=list(dict.fromkeys(t))
tn.remove(inf)

psa=[]
ppso=[]
pga=[]
paco=[]

for i in t:
    sumsa=0
    for k in rsa:
        if(k<=i):
            sumsa+=1
    psa.append(sumsa/len(rsa))
    sumpso=0
    for k in rpso:
        if(k<=i):
            sumpso+=1
    ppso.append(sumpso/len(rpso))
    sumga=0
    for k in rga:
        if(k<=i):
            sumga+=1
    pga.append(sumga/len(rga))
    sumaco=0
    for k in raco:
        if(k<=i):
            sumaco+=1
    paco.append(sumaco/len(raco))
        
# rsa.sort()
# rpso.sort()
# rga.sort()
# raco.sort()
#print("hola")
ax.plot(t, psa,label='SA')
ax.plot(t, ppso,label='PSO')
ax.plot(t, pga, label='GA')
ax.plot(t, paco, label='ACO')

ax.set(xlabel='performance ratio', ylabel='Problems solved',
    title='Performance profile')
ax.grid()
ax.legend()

s="performance_profile" + ".png"

fig.savefig(s)