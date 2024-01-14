import time
# from operator import itemgetter
def solve(N,m,M,fields):
    fields.sort(key=lambda x:x[0])
    
    print(fields)
    days = [0] * (N+1) 
    harvested = []  
    for d, s, e, i in fields:
        for day in range(s, e+1):
            if days[day] + d <= M:
                days[day] += d
                harvested.append((i, day))
                break
    harvested = [(i, day) for i, day in harvested if days[day] >= m]
    harvested.sort(key=lambda x:x[0])

    print(len(harvested))
    for i, day in harvested:
        print(i, day)
    opt = sum(fields[i-1][0] for i,day in harvested)
    print('\nOptimal productivity: ',opt)

start = time.time()
N, m, M = map(int, input().split())
fields = []
for i in range(N):
    
    d, s, e = map(int, input().split())
    fields.append((d, s, e, i+1))

solve(N,m,M,fields)

end = time.time()
print('\nRunning Time: ', end-start)
