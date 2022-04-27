import math
import random
from scipy.optimize import rosen

#Hyper-Paremeters
#Harmony Memory Size
HMS = 10
#Harmony Memory Consideration Rate
HMCR = .95
#Pitch Adjustment Rate
PAR = .5
#Pitch Adjustment Bound +/-
PAB = .1

#-----
#Decision Space Bounds = -2.048 -> 2.048 for rosenbrock and -512 -> 512 for griewank, select accordingly
DB = 2.048
#DB = 512.0


#Harmony Memory
#Harmony memory will get filled with possible solution vectors (sol)
#Each solution vector (sol) is a list in the form: [fitness, x1, x2] where x1 and x2 are decision variables for the optimization function
HM = []

def rosenbrock(x):
    for xi in x:
        if(abs(xi)>DB):
            return float('inf')
    return rosen(x)

def griewank(x):
    for xi in x:
        if(abs(xi)>DB):
            return float('inf')
    dim = len(x)
    A = 0
    B = 1
    for i in range(dim):
        A += x[i]**2
        B *= math.cos(float(x[i]) / math.sqrt(i+1))
    return 1 + (float(A)/4000.0) - float(B)

def cost(x):
    return rosenbrock(x)
    #return griewank(x)

#Initialize Harmony Memory
for i in range(HMS):
    dimensions = 30
    newsol = [float('inf')]
    for _ in range(dimensions):
        newsol.append(random.uniform(-DB,DB))
    newsol[0] = cost(newsol[1:])
    HM.append(newsol)
HM.sort()

for _ in range(100000):
    #New Harmony is Improvised
    NH = [float('inf')]
    for _ in range(30):
        NH.append(0)
    #Choose each parameter
    for i in range(len(NH)-1):
        #Choose new parameter (note) from Harmony memory with prob HMCR, or else randomly
        if(random.random()<HMCR):
            #Note is chosen from Harmony Memory
            NH[i+1] = HM[random.randint(0,HMS-1)][i+1]
        else:
            #Note is chosen randomly
            NH[i+1] = random.uniform(-DB,DB)
        #Adjust chosen parameter (note) according to Pitch Adjustment Rate
        if(random.random()<PAR):
            #Add random number to parameter within PAB designated bound.
            NH[i+1] += random.uniform(-PAB,PAB)
    #Set fitness given the new notes
    NH[0] = cost(NH[1:])
    #Check if new solution is fit enough for Harmony Memory, replace least fit vector if so
    if(NH[0]<HM[-1][0]):
        HM.remove(HM[-1])
        HM.append(NH)
        HM.sort()

print(HM)
