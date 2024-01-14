from ortools.linear_solver import pywraplp
# input
N, m, M = map(int, input().split())
fields = [list(map(int, input().split())) for i in range(N)]

first_day = 10000
last_day = 0
for i in range(N):
    if first_day >= fields[i][1]:
        first_day = fields[i][1]
for i in range(N):
    if last_day <= fields[i][2]:
        last_day = fields[i][2]

def harvestplan(N, m, M, fields):
    solver = pywraplp.Solver.CreateSolver('SCIP')
    # field harvested or not
    y = {}
    for i in range(N):
        y[i] = solver.IntVar(0, 1, 'harvested?')
    # day of harvest
    x = {}
    for i in range(N):
        x[i] = solver.IntVar(fields[i][1], fields[i][2], 'harvestday')
    # objective
    solver.Maximize(solver.Sum(fields[i][0]*y[i] for i in range(N)))
    # constraint: min and max products for a day
    for i in range(first_day, last_day + 1):
        sum_of_day = 0
        for j in range(N):
            if x[j].solution_value() == i:
                sum_of_day += fields[j][0]
        solver.Add(m <= sum_of_day <= M)
    solver.Solve()
    number_of_harvested_fields = 0
    for i in range(N):
        if y[i].solution_value() > 0:
            number_of_harvested_fields += 1
    print (number_of_harvested_fields)
    for i in range(N):
        if y[i].solution_value() > 0:
            print(i + 1, int(x[i].solution_value()))
        else:
            print(i + 1, -1)
harvestplan(N, m, M, fields)
