import pulp
import random
import pandas as pd
random.seed(3)

R = ["suburb", "centre"] #regions
T = ["morning", "evening"] #times

p = {} # prices in the regions
d = {} #demand
zero = {} # min rides is 0
kone = {}
c = 3 # cost per ride
f = 500 # fixed costs
B = 2000 # total bikes available

for t in T:
    p[t] = {}
    d[t] = {}
    zero[t] = {}
    kone[t] = {}
    for r in R:
        p[t][r] = int(10*random.uniform(0,1)) + c
        d[t][r] = int(1000*(1-0.5*random.uniform(0,1)))
        if r=="centre":
            d[t][r] = int(d[t][r]*1.5)
            p[t][r] = int(p[t][r]*1.5)
            if t=="evening":
                d[t][r] = int(d[t][r]*1.5)
                p[t][r] = int(p[t][r]*1.5)
        else:
            if t=="morning":
                d[t][r] = int(d[t][r]*1.5)
                p[t][r] = int(p[t][r]*1.5)
        zero[t][r] = 0.0
        kone[t][r] = 50.0 # price dependence of demand

print("prices "+ str(p))
print("demand "+ str(d))

def rides_morn(b,r):
  r = b[r]-p["morning"][r]*(kone["morning"][r])
  return(r)

def ceeofr(b,r):
  c = (b[r] - (rides_morn(b,r)) + sum([rides_morn(b,rr) for rr in R if rr!=r]))
  return(c)

def rides_even(b,r):
  r = ceeofr(b,r)-p["evening"][r]*(kone["evening"][r])
  return(r)

b = pulp.LpVariable.dicts('', R, lowBound = 20, upBound = 2000, cat = pulp.LpInteger) # num bikes to be allocated in the morning
mobility = pulp.LpProblem("mobility", pulp.LpMaximize) # naming, declaring our model
mobility += sum([(rides_morn(b,r))*(p["morning"][r]-c) for r in R]) + sum([(rides_even(b,r))*(p["evening"][r]-c) for r in R]) - f#, "profit" # cost function

for r in R:
    mobility += (rides_morn(b,r)) >= zero["morning"][r]
    mobility += (rides_morn(b,r)) <= d["morning"][r]
    mobility += (rides_morn(b,r)) <= b[r]
    mobility += (rides_even(b,r)) >= zero["evening"][r]
    mobility += (rides_even(b,r)) <= d["evening"][r]
    mobility += (rides_even(b,r)) <= b[r]

mobility += sum([b[r] for r in R]) <= B
mobility += sum([ceeofr(b,r) for r in R]) <= B

mobility.solve()
print(pulp.LpStatus[mobility.status])
b = {}
for variable in mobility.variables():
    var = variable.name[1:]
    b[var] = variable.varValue
    print("{} = {}".format(var, variable.varValue))

profit = sum([(rides_morn(b,r))*(p["morning"][r]-c) for r in R]) + sum([(rides_even(b,r))*(p["evening"][r]-c) for r in R]) - f
print("profit " + str(profit))
