import math
import random

#Hyper-Paremeters
#Harmony Memory Size
HMS = 15
#Harmony Memory Consideration Rate
HMCR = .90
#Pitch Adjustment Rate
PAR = .5
#Pitch Adjustment Bound +/-
PAB = .05

#Harmony Memory
#Harmony memory will get filled with possible solution vectors (sol)
#Each solution vector (sol) is a list in the form: [fitness, x1, x2]
HM = []

def rosenbrock(x1, x2):
    if(abs(x1)>10 or abs(x2)>10):
        return(float('inf'))
    else:
        return((x1-1)**2 + 100*(x2-x1**2)**2)

def griewank(x1, x2):
    x = [x1,x2]
    A = 0
    B = 1
    for i in range(2):
        A += x[i]**2
        B *= math.cos(float(x[i]) / math.sqrt(i+1))
    return 1 + (float(A)/4000.0) - float(B) 

#Initialize Harmony Memory
for i in range(HMS):
    newsol = [float('inf'), random.uniform(-10,10), random.uniform(-10,10)]
    newsol[0] = rosenbrock(newsol[1],newsol[2])
    #newsol[0] = griewank(newsol[1],newsol[2])
    HM.append(newsol)
HM.sort()

while(HM[0][0]>.00001):
    #New Harmony is Improvised
    NH = [float('inf'),0,0]
    #Choose each parameter
    for i in range(len(NH)-1):
        #Choose new parameter (note) from Harmony memory with prob HMCR, or else randomly
        if(random.random()<HMCR):
            #Note is chosen from Harmony Memory
            NH[i+1] = HM[random.randint(0,14)][i+1]
        else:
            #Note is chosen randomly
            NH[i+1] = random.uniform(-10,10)
        #Adjust chosen parameter (note) according to Pitch Adjustment Rate
        if(random.random()<PAR):
            #Add random number to parameter within PAB designated bound.
            NH[i+1] += random.uniform(-PAB,PAB)
    #Set fitness given the new notes
    NH[0] = rosenbrock(NH[1],NH[2])
    #NH[0] = griewank(NH[1],NH[2])
    #Cehck if new solution is fit enough for solution vector, replace least fit vector if so
    if(NH[0]<HM[-1][0]):
        HM.remove(HM[-1])
        HM.append(NH)
        HM.sort()

print(HM)
