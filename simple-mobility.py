import pulp
import random
import pandas as pd
random.seed(3)

R = ["suburb", "centre"] #regions
p = {} # prices in the regions
d = {} #demand
zero = {} # min rides is 0
kone = {}
c = 3 # cost per ride
f = 500 # fixed costs
B = 2000 # total bikes available

for r in R:
    p[r] = int(10*random.uniform(0,1)) + c
    d[r] = int(1000*(1-0.5*random.uniform(0,1)))
    zero[r] = 0.0
    kone[r] = 50.0 # price dependence of demand

print("regions " + str(R))
print("prices "+ str(p))
print("demand "+ str(d))

b = pulp.LpVariable.dicts('', R, lowBound = 1, upBound = 2000, cat = pulp.LpInteger) # num_bikes

simple_mobility = pulp.LpProblem("simple_mobility", pulp.LpMaximize) # naming, declaring our model
simple_mobility += sum([(b[r]-p[r]*(kone[r]))*(p[r]-c) for r in R])-f, "profit" # cost function
for r in R:
    simple_mobility += (b[r]-p[r]*(kone[r])) >= zero[r]
    simple_mobility += (b[r]-p[r]*(kone[r])) <= d[r]
    simple_mobility += (b[r]-p[r]*(kone[r])) <= b[r]
simple_mobility += sum([b[r] for r in R]) <= B

simple_mobility.solve()
print(pulp.LpStatus[simple_mobility.status])
bikes = {}
profit = 0.0
for variable in simple_mobility.variables():
    var = variable.name[1:]
    bikes[var] = variable.varValue
    profit += (bikes[r]-p[r]*(kone[r]))*(p[r]-c)
    print("{} = {}".format(var, variable.varValue))
profit += -f
print("profit " + str(profit))
