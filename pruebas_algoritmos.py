#import booking as book
import ACO
import GA
import PSO
import SA

def pruebaSA(d,k):

    for i in range(5):
        SA.ejecutarSA(d,i,k)
def pruebaPSO(d,k):

    for i in range(5):
        PSO.ejecutarPSO(d,i,k)
def pruebaACO(d,k):

    for i in range(5):
        ACO.ejecutarACO(d,i,k)
def pruebaGA(d,k):

    for i in range(5):
        GA.ejecutarGA(d,i,k)
pruebaSA(5,300)
pruebaPSO(5,150)
pruebaGA(5,300)
pruebaACO(5,10)