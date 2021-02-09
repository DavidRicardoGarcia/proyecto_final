from operator import attrgetter
import random, sys
import pandas as pd
import numpy as np
import time
import copy

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

	def __init__(self, jss, iterations, size_population, beta=1, alfa=1):
		self.jss = jss # the graph
		self.iterations = iterations # max of iterations
		self.size_population = size_population # size population
		self.particles = [] # list of particles
		self.beta = beta # the probability that all swap operators in swap sequence (gbest - x(t-1))
		self.alfa = alfa # the probability that all swap operators in swap sequence (pbest - x(t-1))

		solutions=[]
		# initialized with a group of random particles (solutions)
		for i in range(self.size_population):
			solutions.append(self.jss.random_permutation())

		#print(solutions)
		# checks if exists any solution
		if not solutions:
			print('Initial population empty! Try run the algorithm again...')
			sys.exit(1)

		# creates the particles and initialization of swap sequences in all the particles
		for solution in solutions:
			# creates a new particle
			particle = Particle(solution=solution, cost=self.jss.calcular_makespan(solution))
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
				cost_current_solution = self.jss.calcular_makespan(solution_particle)
				# updates the cost of the current solution
				particle.setCostCurrentSolution(cost_current_solution)

				# checks if current solution is pbest solution
				if cost_current_solution < particle.getCostPBest():
					particle.setPBest(solution_particle)
					particle.setCostPBest(cost_current_solution)
		

class jssp:

	def __init__(self, num_job,num_mc,pt,ms):
		
		self.num_job=num_job
		self.num_mc=num_mc
		self.pt=pt
		self.ms=ms
		self.num_gene=num_mc*num_job 
		self.state=self.random_permutation()

	def calcular_makespan(self,a):

			self.state=a
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

	def random_permutation(self):
		nxm_random_num=list(np.random.permutation(self.num_gene))
		job_order=nxm_random_num
		for j in range(self.num_gene):
			job_order[j]=job_order[j]%self.num_job
		return job_order

	def set_state(self,a):
		self.state=a 



pt_tmp=pd.read_excel("JSP_dataset.xlsx",sheet_name="Processing Time",index_col =[0]) # processing time in excel 
ms_tmp=pd.read_excel("JSP_dataset.xlsx",sheet_name="Machines Sequence",index_col =[0]) # machines sequence in excel

dfshape=pt_tmp.shape # matrix shape
num_mc=dfshape[1] # number of machines
num_job=dfshape[0] # number of jobs
num_gene=num_mc*num_job # number of genes in a chromosome

pt=[list(map(int, pt_tmp.iloc[i])) for i in range(num_job)]
ms=[list(map(int,ms_tmp.iloc[i])) for i in range(num_job)]


problem=jssp(num_job,num_mc,pt,ms)

solver=PSO(problem,iterations=5000,size_population=30,beta=1,alfa=0.9)

solver.run()

solver.showsParticles()

print('gbest: %s | cost: %d\n' % (solver.getGBest().getPBest(), solver.getGBest().getCostPBest()))
 
#print(min(solver.particles, key=attrgetter('cost_pbest_solution')).solution)

