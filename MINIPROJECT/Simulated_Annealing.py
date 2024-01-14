import random
import math
import time
from ortools.sat.python import cp_model
import matplotlib.pyplot as plt

# For input of 10, computingTime = 6s, initial_temp = 1000 and no_attempts = 1000 (currentFitness = 1)
# For input of 100,computingTime = 120s, initial_temp = 1000 and no_attempts = 1000 (currentFitness = 13)
# For input of 1000, computingTime = 1000s, initial_temp = 10000 and no_attempts = 1000. (currentFitness = 9)
# For input of 5000, computingTime = 6000s, initial_temp = 100000 and no_attempts = 1000. (currentFitness = 89)
# For input of 10000, ...

computingTime = 6000
random.seed(0)

# INPUT: COPY INPUT ON HUSTACK AND Ctrl + Shift + V to paste into the Command Prompt AFTER RUNNING THIS FILE.
N, m, M = list(map(int, input().split()))
amount, lowerBound, upperBound = [], [], []
for i in range(N):
    d, s, e = list(map(int, input().split()))
    amount.append(d)
    lowerBound.append(s)
    upperBound.append(e)

begin, final = min(lowerBound), max(upperBound)
# NECESSARY COMPONENTS
def harvestedDays(fields: list, amount: list):
    ''' Return the amount of crops harvested in each day (if any)
        The days are obscured. '''
    # Taken into account the the value assignment process
    if fields.count(-1) != 0:
        j = fields.index(-1)
        fields = fields[:j]
        amount = amount[:j]
        
    # Elements of "fields" are in the form (amount of crop, harvesting day)
    fields = list(map(lambda x, y: (y, x), fields, amount))
    fields.sort(key = lambda x: x[1])
    
    common_days, i = [], 1
    while i <= len(fields):
        if i == len(fields):
            if len(fields) == 1:
                common_days.append(fields[0][0])
                return common_days
            else: break
        else:
            if fields[i-1][1] == fields[i][1]:
                if i == len(fields) - 1:
                    common_days.append(sum(x[0] for x in fields[:(i+1)]))
                i += 1
            else:
                common_days.append(sum(x[0] for x in fields[:i]))
                del fields[:i]
                i = 1
    return common_days

# The constraint
def factoryConstraint(plan: list, m: int, M: int):
    ''' Making sure that the factory capacity is respected in each harvesting day.
    Its input is the result returned by harvestedDays(). '''
    if min(plan) < m: return False
    else:
        if max(plan) > M: return False
        else: return True
        
# The objective function
def objectiveFunction(commonDays: list):
    ''' Its input is the result returned by harvestedDays(). '''
    return max(commonDays) - min(commonDays)

# Generation of neighbour
def shift(fields: list, previousSol: list):
    ''' Making sure that randomly generated point stay within bounds.
    Each infeasible solution is shift to value chosen uniformly at random between the violated bounds and the (feasible) value at the previous iteration.'''
    for i in range(len(fields)):
        if fields[i] < lowerBound[i] or fields[i] > upperBound[i]:
            a = random.randint(0, 1)
            if a == 0:
                fields[i] = random.randint(lowerBound[i], previousSol[i])
            elif a == 1:
                fields[i] = random.randint(previousSol[i], upperBound[i])
    return fields

def neighbour(currentSol: list):
    ''' Focusing in reducing the amount of crops in the largest day and increasing that in the smallest day'''
    distinct = sorted(list(set(currentSol)))
    days = harvestedDays(currentSol, amount)
    # Days having the largest and smallest amount of crops harvested
    largest_day = distinct[days.index(max(days))]
    smallest_day = distinct[days.index(min(days))]
    # Fields harvested in the largest(smallest)_day
    largestFields = [(i, amount[i]) for i in range(N) if currentSol[i] == largest_day]
    smallestFields = [(i, amount[i]) for i in range(N) if currentSol[i] == smallest_day]
    largestFields.sort(key = lambda x: x[1], reverse= True)
    smallestFields.sort(key = lambda x: x[1])
    # The index of the field with the largest(smallest) crops in largest(smallest)Fields
    largest_index = largestFields[0][0]
    smallest_index = smallestFields[0][0]
    a = random.randint(lowerBound[largest_index], upperBound[largest_index])
    b = random.randint(0, N-2)
    newSol = []
    for i in range(N):
        if i == largest_index:
            newSol.append(a)
        else: newSol.append(currentSol[i])
    newSol[b] = newSol[smallest_index]
    newSol = shift(newSol, currentSol)
    return newSol

def acceptance_prob(newSol: list, currentSol: list, temp: float, amount: list):
    ''' Return the acceptance of a new neighbour. '''
    f1 = objectiveFunction(harvestedDays(currentSol, amount))
    f2 = objectiveFunction(harvestedDays(newSol, amount))
    if f2 < f1:
        return 1
    else: 
        p = math.exp((f1 - f2)/temp)
        return p

def printAnswer(fields):
    print(N)
    for i in range(N):
        print(i+1, fields[i])
        
# The generation of an intial solution
def initialSol(N, m, M, amount, lowerBound, upperBound):
    ''' Create the initial solution. This solution satisfies all constraints. '''
    model = cp_model.CpModel()
    fields = []
    for i in range(N):
        field = []
        for d in range(begin, final + 1):
            field.append(model.NewIntVar(0, 1, 'field[' + str(i+1) + ',' + str(d) + ']'))
        fields.append(field)
    # Each field can only be harvested once.
    for i in range(N):
        model.Add(sum(fields[i][d] for d in range(final - begin + 1)) == 1)
    # The amount of crops harvested in a day must be in between m and M.
    for d in range(final - begin + 1):
        a = model.NewBoolVar('a')
        model.Add(sum(fields[i][d]*amount[i] for i in range(N)) != 0).OnlyEnforceIf(a)
        model.Add(sum(fields[i][d]*amount[i] for i in range(N)) >= m).OnlyEnforceIf(a)
        model.Add(sum(fields[i][d]*amount[i] for i in range(N)) == 0).OnlyEnforceIf(a.Not())
        b = model.NewBoolVar('b')
        model.Add(sum(fields[i][d]*amount[i] for i in range(N)) != 0).OnlyEnforceIf(b)
        model.Add(sum(fields[i][d]*amount[i] for i in range(N)) <= M ).OnlyEnforceIf(b)
        model.Add(sum(fields[i][d]*amount[i] for i in range(N)) == 0).OnlyEnforceIf(b.Not())
    # A field i can only be harvested in the period from starts[i] to ends[i].
    for i in range(N):
        for d in range(final - begin + 1):
            original_d = d + begin
            if original_d not in range(lowerBound[i], upperBound[i] + 1):
                model.Add(fields[i][d] == 0)
    # CALL THE SOLVER
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    # DISPLAYING THE SOLUTION
    results = []
    if status == cp_model.FEASIBLE or status == cp_model.OPTIMAL:
        for i in range(N):
            for d in range(final - begin + 1):
                if solver.BooleanValue(fields[i][d]):
                    results.append(d + begin)
    return results

initial_sol = initialSol(N, m, M, amount, lowerBound, upperBound)

# Temperature schedule and number of attempts for each temperature
initial_temp = 100000
cooling_const = 0.95

# Initial solution: A solution satisfying all constraints which is generated by CP

currentTemp = initial_temp
currentSol = initial_sol
currentFitness = objectiveFunction(harvestedDays(currentSol, amount))
record = []

# THE ALGORITHM WITH TIME STOPPING CONDITIONS
start = time.time()
no_attempts = 1000
while True:  
    for j in range(no_attempts):
        newSol = neighbour(currentSol)
        newDays = harvestedDays(newSol, amount)
        if factoryConstraint(newDays, m, M):
            newFitness = objectiveFunction(harvestedDays(newSol, amount))
            if newFitness < currentFitness:
                accept = True
            else:
                if random.random() < acceptance_prob(newSol, currentSol, currentTemp, amount):
                    accept = True
                else: accept = False
            if accept == True:
                currentSol = newSol
                currentFitness = newFitness
    
    record.append(currentFitness)
    currentTemp = currentTemp * cooling_const
    end = time.time()
    if end-start >= computingTime:
        break


# UNCOMMENT THIS TO SEE THE RESULT
printAnswer(currentSol)
print('Running Time: ',end-start)
# Checking results
# print(currentSol)
# print(currentFitness)
# # Showing the performance of the algorithm
# plt.plot(record)
# plt.ylabel('Objective function', color = 'red', fontstyle = 'italic')
# plt.xlabel('Number of iterations', color = 'red', fontstyle = 'italic')
# plt.title('Simulated Annealing Performance')
# plt.show()