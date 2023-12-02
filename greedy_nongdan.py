# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 10:10:25 2023

@author: Admin
"""

from operator import itemgetter
N, m, M = map(int, input().split())
fields = []
for i in range(N):
    d, s, e = map(int, input().split())
    fields.append((d, s, e, i+1))
def solve(N,m,M,fields):
    fields.sort(key=itemgetter(1, 2))
    days = [0] * (N+1) 
    harvested = []  
    for d, s, e, i in fields:
        for day in range(s, e+1):
            if days[day] + d <= M:
                days[day] += d
                harvested.append((i, day))
                break
    harvested = [(i, day) for i, day in harvested if days[day] >= m]
    harvested.sort(key=itemgetter(0))

    print(len(harvested))
    for i, day in harvested:
        print(i, day)
solve(N,m,M,fields)
