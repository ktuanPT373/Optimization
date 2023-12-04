import time
import numpy as np
d = [8,8,4,8,7,7,1,2,6,7]
s = [3,2,2,1,3,1,1,1,1,1]
e = [7,6,6,4,7,4,4,4,4,3]
N, m, M = 10, 7, 24

# d,s,e = [],[],[]
# N, m, M = map(int,input().split())
# for _ in range(N):
#     de, se, ee = map(int,input().split())
#     d.append(de)
#     s.append(se)
#     e.append(ee)
d_min = min(d)   
x = [-1]*N
day = [0]*max(e)
ts = 0
config = [-1]*N
config2 = [0]*max(e)
def constraint(i,j):
    if m <= day[j-1]+ d[i] <= M:
         return True
    return False
    
def backtrack(i):
    global ts, config, config2
    for j in range(s[i], e[i] + 1):
        if constraint(i,j):
            day[j-1] += d[i]
            x[i] = j
            if i == N-1:
                if sum(day) > ts:
                    ts = sum(day)
                    config = x.copy()
                    config2 = day.copy()
            else:
                if ts < sum(d):
                    backtrack(i+1)
            day[j-1] -= d[i]
            x[i] = -1
start = time.time()
backtrack(0)
print(len(config))
for i in range(len(config)):
    print(i+1,config[i])
end = time.time()
print("Running time:", end-start)