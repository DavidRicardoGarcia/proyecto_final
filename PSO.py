from operator import attrgetter
import random, sys
import pandas as pd
import numpy as np
import time
import copy

import json
import os.path
import matplotlib
import matplotlib.pyplot as plt
import booking as book

funcion=book.planificador()

def terminado_algoritmo(res,tiempo,valor):
        
	save_path = '/home/david/Desktop/optimizacion_final/datos_json'

	name_of_file = 'estado'

	completeName = os.path.join(save_path, name_of_file+".txt") 

	with open(completeName) as json_file:
		data = json.load(json_file)

	data['PSO']['estado']='terminado'
	data['PSO']['resultado']=res
	data['PSO']['tiempo']=tiempo
	data['PSO']['valor']=valor
	#se ejecuta el algoritmo en cuestion

	with open(completeName,'w') as outfile:
		json.dump(data,outfile)

def charts(x,y):
        
    save_path = '/home/david/Desktop/optimizacion_final/datos_json'

    name_of_file = 'charts'

    completeName = os.path.join(save_path, name_of_file+".txt") 

    with open(completeName) as json_file:
        data = json.load(json_file)

    data['PSO']['y']=y
    data['PSO']['x']=x

    #se ejecuta el algoritmo en cuestion

    with open(completeName,'w') as outfile:
        json.dump(data,outfile)

def graficas_png(d,n,x,y):
    fig, ax = plt.subplots()
    ax.plot(x, y)

    ax.set(xlabel='gen (k)', ylabel='f (d)',
        title='cost function')
    ax.grid()

    s="PSOtest" +repr(d)+"-"+repr(n) + ".png"

    fig.savefig(s)


class Particle:

	def __init__(self, solution, cost):

		# current solution
		self.solution = solution

		# best solution (fitness) it has achieved so far
		self.pbest = solution

		# set costs
		self.cost_current_solution = cost
		self.cost_pbest_solution = cost

		# velocity of a particle is a sequence of 4-tuple
		# (1, 2, 1, 'beta') means SO(1,2), prabability 1 and compares with "beta"
		self.velocity = []

	# set pbest
	def setPBest(self, new_pbest):
		self.pbest = new_pbest

	# returns the pbest
	def getPBest(self):
		return self.pbest

	# set the new velocity (sequence of swap operators)
	def setVelocity(self, new_velocity):
		self.velocity = new_velocity

	# returns the velocity (sequence of swap operators)
	def getVelocity(self):
		return self.velocity

	# set solution
	def setCurrentSolution(self, solution):
		self.solution = solution

	# gets solution
	def getCurrentSolution(self):
		return self.solution

	# set cost pbest solution
	def setCostPBest(self, cost):
		self.cost_pbest_solution = cost

	# gets cost pbest solution
	def getCostPBest(self):
		return self.cost_pbest_solution

	# set cost current solution
	def setCostCurrentSolution(self, cost):
		self.cost_current_solution = cost

	# gets cost current solution
	def getCostCurrentSolution(self):
		return self.cost_current_solution

	# removes all elements of the list velocity
	def clearVelocity(self):
		del self.velocity[:]

class PSO:

	def __init__(self, modelo, iterations, size_population, beta=1, alfa=1):
		self.modelo = modelo # the graph
		self.iterations = iterations # max of iterations
		self.size_population = size_population # size population
		self.particles = [] # list of particles
		self.beta = beta # the probability that all swap operators in swap sequence (gbest - x(t-1))
		self.alfa = alfa # the probability that all swap operators in swap sequence (pbest - x(t-1))
		self.makespan_record=[]
		self.index_record=[]

		solutions=[]
		# initialized with a group of random particles (solutions)
		for i in range(self.size_population):
			solutions.append(self.modelo.random_permutation())

		#print(solutions)
		# checks if exists any solution
		if not solutions:
			print('Initial population empty! Try run the algorithm again...')
			sys.exit(1)

		# creates the particles and initialization of swap sequences in all the particles
		for solution in solutions:
			# creates a new particle
			particle = Particle(solution=solution, cost=self.modelo.calcular(solution))
			# add the particle
			self.particles.append(particle)
		#print(self.particles[0].solution)
		# updates "size_population"
		self.size_population = len(self.particles)


	# set gbest (best particle of the population)
	def setGBest(self, new_gbest):
		self.gbest = new_gbest

	# returns gbest (best particle of the population)
	def getGBest(self):
		return self.gbest


	# shows the info of the particles
	def showsParticles(self):

		print('Showing particles...\n')
		for particle in self.particles:
			print('pbest: %s\t|\tcost pbest: %d\t|\tcurrent solution: %s\t|\tcost current solution: %d' \
				% (str(particle.getPBest()), particle.getCostPBest(), str(particle.getCurrentSolution()),
							particle.getCostCurrentSolution()))
		print('')


	def run(self):

		# for each time step (iteration)


		for t in range(self.iterations):

			# updates gbest (best particle of the population)
			self.gbest = min(self.particles, key=attrgetter('cost_pbest_solution'))

			# for each particle in the swarm
			for particle in self.particles:

				particle.clearVelocity() # cleans the speed of the particle
				temp_velocity = []
				solution_gbest = copy.copy(self.gbest.getPBest()) # gets solution of the gbest
				solution_pbest = particle.getPBest()[:] # copy of the pbest solution
				solution_particle = particle.getCurrentSolution()[:] # gets copy of the current solution of the particle

				# generates all swap operators to calculate (pbest - x(t-1))
				for i in range(len(particle.solution)):
					if solution_particle[i] != solution_pbest[i]:
						# generates swap operator
						swap_operator = (i, solution_pbest.index(solution_particle[i]), self.alfa)

						# append swap operator in the list of velocity
						temp_velocity.append(swap_operator)

						# makes the swap
						aux = solution_pbest[swap_operator[0]]
						solution_pbest[swap_operator[0]] = solution_pbest[swap_operator[1]]
						solution_pbest[swap_operator[1]] = aux

				# generates all swap operators to calculate (gbest - x(t-1))
				for i in range(len(particle.solution)):
					if solution_particle[i] != solution_gbest[i]:
						# generates swap operator
						swap_operator = (i, solution_gbest.index(solution_particle[i]), self.beta)

						# append swap operator in the list of velocity
						temp_velocity.append(swap_operator)

						# makes the swap
						aux = solution_gbest[swap_operator[0]]
						solution_gbest[swap_operator[0]] = solution_gbest[swap_operator[1]]
						solution_gbest[swap_operator[1]] = aux

				
				# updates velocity
				particle.setVelocity(temp_velocity)

				# generates new solution for particle
				for swap_operator in temp_velocity:
					if random.random() <= swap_operator[2]:
						# makes the swap
						aux = solution_particle[swap_operator[0]]
						solution_particle[swap_operator[0]] = solution_particle[swap_operator[1]]
						solution_particle[swap_operator[1]] = aux
				
				# updates the current solution
				particle.setCurrentSolution(solution_particle)
				# gets cost of the current solution
				cost_current_solution = self.modelo.calcular(solution_particle)
				# updates the cost of the current solution
				particle.setCostCurrentSolution(cost_current_solution)

				# checks if current solution is pbest solution
				if cost_current_solution < particle.getCostPBest():
					particle.setPBest(solution_particle)
					particle.setCostPBest(cost_current_solution)
			self.makespan_record.append(self.gbest.getCostPBest())
			self.index_record.append(t)

class modelo:

	def __init__(self, tareas, estado):
		
		self.tareas=tareas
		self.estado=estado
		self.tamano=len(estado)
		self.state=self.random_permutation()

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


	def random_permutation(self):
		nxm_random_num=list(np.random.permutation(self.tamano))
		return nxm_random_num

	def set_state(self,a):
		self.state=a 


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

def ejecutarPSO(d,n,k):
	
	start_time = time.time()
	x=cargar_tareas()

	lista_id=get_id_list(x['pedidos'])

	problem=modelo(x['pedidos'],lista_id)

	solver=PSO(problem,iterations=k,size_population=10,beta=1,alfa=0.9)

	solver.run()

	solver.showsParticles()

	print('gbest: %s | cost: %d\n' % (solver.getGBest().getPBest(), solver.getGBest().getCostPBest()))
	tiempo=time.time() - start_time
	print('the elapsed time:%s'% (time.time() - start_time))
	lista=[int(i) for i in solver.getGBest().getPBest()]
	cost=solver.getGBest().getCostPBest()
	terminado_algoritmo(lista,tiempo,cost)
	#charts(solver.index_record,solver.makespan_record)
	graficas_png(d,n,solver.index_record,solver.makespan_record)
	#print(min(solver.particles, key=attrgetter('cost_pbest_solution')).solution)


#ejecutarPSO(1,1,1)