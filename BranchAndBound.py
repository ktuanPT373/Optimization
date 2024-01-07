# Have only be able to run for INPUT OF 10
# INPUT: COPY INPUT ON HUSTACK AND Ctrl + Shift + V to paste into the Command Prompt AFTER RUNNING THIS FILE.
import time
start = time.time()
N, m, M = list(map(int, input().split()))
amount, starts, ends = [], [], []
for i in range(N):
    d, s, e = list(map(int, input().split()))
    amount.append(d)
    starts.append(s)
    ends.append(e)

total_amount = sum(amount)

def upperBound(S: int, plan: list, k: int):
    ''' Making sure that the maximum difference
    between amount of crops harvested in any two days is no larger than k. '''
    n = len(plan)
    bound = int((S + (n-1)*k)/n)
    if max(plan) > bound: return False
    else: return True

def factoryConstraint(plan: list, m: int, M: int):
    ''' Making sure that the factory capacity is respected in each harvesting day'''
    if min(plan) < m: return False
    else:
        if max(plan) > M: return False
        else: return True
        
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

def max_diff(commonDays: list):
    ''' The objective function '''
    return max(commonDays) - min(commonDays)

fields = [-1 for i in range(N)]
maxDiff = 99999

def Solution(k: int, fields: list):
    ''' The maximum difference of crops harvested 
    between any 2 days is no more than k. '''
    global maxDiff
    a = max_diff(harvestedDays(fields, amount))
    if a < maxDiff:
        maxDiff = a
    if maxDiff <= k:
        return fields

def printAnswer(fields):
    print(N)
    for i in range(N):
        print(i+1, fields[i])
        
def Try(j, k):
    ''' Branch-and-Bound algorithm where k is the the value of the objective function. '''
    global break_out, checkCounter 
    break_out, checkCounter = False, 0
    if j in range(N):
        for day in range(starts[j], ends[j] + 1):
            if break_out: 
                break
            fields[j] = day
            days = harvestedDays(fields, amount)
            if upperBound(total_amount, days, k) and factoryConstraint(days, m, M):
                if j == N-1:
                    if bool(Solution(k, fields)):
                        checkCounter += 1
                        printAnswer(Solution(k, fields))
                        break_out = True       
                else: Try(j + 1, k)    
            else: Try(j + 1, k)

# Consider different cases with increasing maximum difference
for k in range(M+1):
    Try(0, k)
    if checkCounter == 1:
        break
end = time.time()
print('\nRunning time: ',end-start)