from ortools.linear_solver import pywraplp

N, m, M = map(int, input().split())
fields = []
for i in range(N):
    d, s, e = map(int, input().split())
    fields.append((d, s, e, i+1))
def solve(N, m, M, fields):
    solver = pywraplp.Solver.CreateSolver('SCIP')
    # field i is harvested or not
    x = {}
    for i in range(1, N + 1):
        x[i] = solver.IntVar(-1, 0, 'harvested[%i]' % i)
    # day of harvest
    y = solver.IntVar(1, 10000, 'harvestday')

# constraints
    for i in range(1, N + 1):

        solver.Add(x[i] == 0).OnlyEnforceIf(x[i] * (fields[i-1][1] - 1) < 0)

        solver.Add(solver.Sum(fields[j-1][0] * x[j] for j in range(1, N + 1) if fields[j-1][1] <= fields[i-1][2]) <= M).OnlyEnforceIf(x[i] == 1)

        solver.Add(y >= fields[i-1][1] * x[i]).OnlyEnforceIf(x[i] == 1)
   
   # objective
    solver.Maximize(solver.Sum(fields[i-1][0] * x[i] for i in range(1, N + 1)))

    solver.Solve()

    print(int(sum(x[i].solution_value() for i in range(1, N + 1))))
    for i in range(1, N + 1):
        if x[i].solution_value() > 0:
            print(i, int(y.solution_value()))


solve(N, m, M, fields)
