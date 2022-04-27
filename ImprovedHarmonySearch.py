import math
import random
from scipy.optimize import rosen

#ITERATIONS
ITS = 100000

#-----
#Decision Space Bounds = -2.048 -> 2.048 for rosenbrock and -512 -> 512 for griewank, select accordingly
DB = 2.048
#DB = 512.0

#Hyper-Paremeters ---- FOR IMPROVED HARMONY SEARCH IMPLEMENTATION
#UNCOMMENT ALL FOR CHOSEN IMPLENTATION TO USE
#Harmony Memory Size
#HMS = 10
#Harmony Memory Consideration Rate
#HMCRMax = .99
#HMCRMin = .5
#HMCR = .95
#Pitch Adjustment Rate
#PARMax = .8
#PARMin = .05
#Pitch Adjustment Bound +/-
#PABMax = 2*DB/10
#PABMin = .00000001

#Hyper-Parameters ---- FOR MY IMPROVED HARMONY SEARCH IMPLEMENTATION
#Harmony Memory Size
HMS = 10
#Initial Harmony Memory Consideration Rate
IHMCR = .5
HMCR = IHMCR
#Initial Pitch Adjustment Rate
IPAR = .7
#PARMax = 1
#PARMin = .05
#Initial Pitch Adjustment Bound +/-
IPAB = DB/5

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

for it in range(ITS):
    #Update PAB, PAR, and HMCR in accordance with Improved Harmony Search
    #PAB = PABMax * math.exp(math.log(PABMin/PABMax)*it/ITS)
    #PAR = PARMin + (PARMin + PARMax)*it/ITS
    #NOT INCLUDED IN OFFICIAL IHS BUT HELPS:
    #HMCR = HMCRMin + (HMCRMin + HMCRMax)*it/ITS

    #In accordance to my ideas similar to IHS
    PAB = IPAB / math.sqrt(it+1)
    PAR = IPAR
    #PAR = it/(it+100)
    #PAR = PARMin + (PARMin + PARMax)*it/ITS
    HMCR = (1 - HMCR)/5 + HMCR


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
