from ortools.sat.python import cp_model
import time

start = time.time()

# Reading input: number of fields (N), minimum and maximum total harvest (m, M)
N, m, M = map(int, input().split())
fields = []
for _ in range(N):
    d, s, e = map(int, input().split())
    fields.append((d, s, e))

# Creating a CP model
model = cp_model.CpModel()

# Defining variables: Whether each field is harvested on a particular day (boolean)
harvest = {}
for i in range(N):
    for day in range(fields[i][1], fields[i][2] + 1):
        harvest[(i, day)] = model.NewBoolVar(f'harvest_field_{i}_day_{day}')

# Adding constraints: Each field must be harvested exactly once within its available days
for i in range(N):
    model.Add(sum(harvest[(i, day)] for day in range(fields[i][1], fields[i][2] + 1)) == 1)

# Adding constraints for total harvested amount each day to be within the minimum and maximum limits
for day in range(1, max(fields[i][2] for i in range(N)) + 1):
    daily_harvest = sum(harvest[(i, day)] * fields[i][0] for i in range(N) if day in range(fields[i][1], fields[i][2] + 1))
    model.Add(daily_harvest >= m)
    model.Add(daily_harvest <= M)

# Objective: Maximize the total amount harvested
total_harvest = sum(harvest[(i, day)] * fields[i][0] for i in range(N) for day in range(fields[i][1], fields[i][2] + 1))
model.Maximize(total_harvest)

# Creating a solver and solving the model
solver = cp_model.CpSolver()
status = solver.Solve(model)

# Checking if an optimal solution was found
if status == cp_model.OPTIMAL:
    # Retrieving and printing the solution: which day each field should be harvested
    print(N)
    for i in range(N):
        for day in range(fields[i][1], fields[i][2] + 1):
            if solver.Value(harvest[(i, day)]):
                print(f"{i+1} {day}")

    # Retrieving and printing the optimal objective value (total amount harvested)
    optimal_objective = solver.ObjectiveValue()
    print(f"Optimal Objective Value (Total Harvest): {optimal_objective}")
else:
    print("không tìm thấy phương án")

end = time.time()
print('Taken Time: ', end - start)


