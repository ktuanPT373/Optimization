import random

def randomized_algorithm(fields, m, M, iterations=100):
    def get_harvested(fields, m, M):
        day_product = [0] * (N+1)
        harvested = []
        for d, start, end, index in fields:
            best_day = max(
                range(start, end+1),
                key=lambda day: (day_product[day] + d, day_product[day]),
                default=-1
            )
            if best_day != -1 and day_product[best_day] + d <= M:
                day_product[best_day] += d
                harvested.append((index, best_day, d))
        return [(i, day, d) for i, day, d in harvested if day_product[day] >= m]

    best_harvest = []

    for _ in range(iterations):
        random.shuffle(fields)
        current_harvest = get_harvested(fields, m, M)
        if sum(d for _, _, d in current_harvest) > sum(d for _, _, d in best_harvest):
            best_harvest = current_harvest

    return best_harvest

def evaluate_plan(plan, fields):
    return -len({day for day in plan if day > 0}), -sum(fields[i][0] for i, day in enumerate(plan) if day > 0)

def is_valid_plan(plan, fields):
    return all(m <= sum(fields[j][0] for j, day_of_j in enumerate(plan) if day_of_j == day) <= M for day in set(plan) if day > 0)

def local_search(N, fields):
    best_harvested_fields = randomized_algorithm(fields, m, M)
    best_plan = [-1] * N
    for i, day, _ in best_harvested_fields:
        best_plan[i-1] = day
    
    for _ in range(10000):
        field_to_change = random.randint(0, N - 1)
        new_day = random.randint(fields[field_to_change][1], min(fields[field_to_change][2], M))
        new_plan = best_plan[:]
        new_plan[field_to_change] = new_day

        if evaluate_plan(new_plan, fields) > evaluate_plan(best_plan, fields) and is_valid_plan(new_plan, fields):
            best_plan = new_plan

    return best_plan

# Read input data
N, m, M = map(int, input().split())
fields_input = [tuple(map(int, input().split())) + (i+1,) for i in range(N)]
fields = [field[:-1] for field in fields_input]

# Find the harvest plan
harvest_plan = local_search(N, fields)

# Output the results
print(sum(day > 0 for day in harvest_plan))
for i, day in enumerate(harvest_plan, start=1):
    if day > 0:
        print(i, day)