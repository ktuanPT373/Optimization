from ortools.linear_solver import pywraplp

def solve(N, m, M, fields):
    solver = pywraplp.Solver.CreateSolver('SCIP')

    x = {}
    for i in range(N):
        for j in range(fields[i][1], fields[i][2] + 1):
            x[(i, j)] = solver.IntVar(0, 1, '')
    # Constraints
    for i in range(N):
        solver.Add(solver.Sum([x[(i, j)] for j in range(fields[i][1], fields[i][2] + 1)]) <= 1)
        
    for j in range(1, max(e for d, s, e in fields) + 1):
        solver.Add(solver.Sum([x[(i, j)] * fields[i][0] for i in range(N) if j >= fields[i][1] and j <= fields[i][2]]) <= M)
        solver.Add(solver.Sum([x[(i, j)] * fields[i][0] for i in range(N) if j >= fields[i][1] and j <= fields[i][2]]) >= m)

    # Objective
    objective = solver.Objective()
    for i in range(N):
        for j in range(fields[i][1], fields[i][2] + 1):
            objective.SetCoefficient(x[(i, j)], fields[i][0])
    objective.SetMaximization()

    
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        # print('Total harvested =', objective.Value())
        harvested_fields = [(i+1, j) for i in range(N) for j in range(fields[i][1], fields[i][2] + 1) if x[(i, j)].solution_value() > 0]
        print(len(harvested_fields))
        for field, day in harvested_fields:
            print(field, day)
        #check_solution(harvested_fields, fields, m, M)
    else:
        print('The problem does not have an optimal solution.')

N, m, M = map(int, input().split())
fields = []
for i in range(N):
    d, s, e = map(int, input().split())
    fields.append((d, s, e))
solve(N, m, M, fields)



