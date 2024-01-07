import time
import random
random.seed(0)
def best_brute_force(Fields, m, M, iterations=100):
    best_harvested = []
    for _ in range(iterations):
        random.shuffle(Fields)
        harvested = []
        day_product = [0] * (N+1)  
        for d, s, e, i in Fields:
            best_day = -1
            for day in range(s, e+1):
                if day_product[day] + d <= M and (best_day == -1 or day_product[day] + d > day_product[best_day] + d):
                    best_day = day
            if best_day != -1:
                day_product[best_day] += d
                harvested.append((i, best_day, d))
        harvested = [(i, day, d) for i, day, d in harvested if day_product[day] >= m]

        if sum(d for i, day, d in harvested) > sum(d for i, day, d in best_harvested):
            best_harvested = harvested
    return best_harvested

# Evaluate the given plan
def evaluate_plan(plan, fields, m, M):
    total_harvested = 0
    for i, day in enumerate(plan):
        if day > 0:
            total_harvested += fields[i][0] # Add the productivity of a day 
    return total_harvested
    
# consider whether the plan is valid or no
def is_valid_plan(plan, fields, m, M):
    for i, day in enumerate(plan):
        if day > 0:
            harvested_quantity = sum(fields[j][0] for j, value in enumerate(plan) if value == day)
            if not m <= harvested_quantity <= M:
                return False
    return True


def local_search(N, m, M, fields):
    harvested = best_brute_force(Fields, m, M)
    current_plan = [-1]*N
    for i, day, d in sorted(harvested, key=lambda x: x[0]):
        current_plan[i-1]=day

    iteration = 0
    while iteration < 10000:
       
        field_to_change = random.randint(0, N - 1)
        neighbor_plan = current_plan.copy()
        neighbor_plan[field_to_change] = random.randint(fields[field_to_change][1], fields[field_to_change][2])
        current_score = evaluate_plan(current_plan, fields, m, M)

        neighbor_score = evaluate_plan(neighbor_plan, fields, m, M)

        if neighbor_score > current_score and is_valid_plan(neighbor_plan, fields, m, M):
            current_plan = neighbor_plan 
        
        iteration += 1
        
    return current_plan

start = time.time()

N, m, M = map(int, input().split())
Fields = []
fields = []
for i in range(N):
    d, s, e = map(int, input().split())
    Fields.append((d, s, e, i+1))
    fields.append((d,s,e))

harvest_plan = local_search(N, m, M, fields)


print(sum(1 for day in harvest_plan if day > 0))
for i, day in enumerate(harvest_plan, start=1):
    if day > 0:
        print(i, day)

opt = sum(fields[i][0] for i, day in enumerate(harvest_plan))
end = time.time()

print('\n Optimal Productivity: ',opt)
print('\n')
print('Running Time: ',end-start)
'''
Pseudo code

N : number of fields
m : minimum amount of products harvested in a day 
M : naximum amount of products harvested in a day

Fields : array types, [d: product of a day, s: start day to harvest, e: end day to harvest, i: index of field] 
fields : array types, [d: product of a day, s: start day to harvest, e: end day to harvest]


def ranmoized_algorithms(Fields,m,M,iter=100)

def evaluate_plan(plan, fields, m, M)

def is_valid_plan(plan, fields, m, M)

def local_search(N, m, M, fields):

'''
