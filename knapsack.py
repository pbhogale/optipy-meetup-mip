import pulp
import random
import pandas as pd

C = 1.0
L = ["torch", "food", "tent", "knife", "books"]
L.extend(["random_stuff" + str(i) for i in range(20)])
weight = {}
usefulness = {}
random.seed(3)
for o in L:
    weight[o] = random.uniform(0,1)
    usefulness[o] = random.uniform(0,1)

x = pulp.LpVariable.dicts('', L, lowBound = 0, upBound = 1, cat = pulp.LpInteger)

knapsack_model = pulp.LpProblem("knapsack", pulp.LpMaximize)
knapsack_model += sum([usefulness[thing]*x[thing] for thing in L]), "usefulness" ## cost function
knapsack_model += sum([weight[thing]*x[thing] for thing in L]) <= C

knapsack_model.solve()
print(pulp.LpStatus[knapsack_model.status])
total_weight = 0.0
things = {}
for variable in knapsack_model.variables():
    var = variable.name[1:]
    things[var] = variable.varValue
    total_weight += weight[var]*things[var]

print("the total weight taken is "+str(total_weight))
solution_data = pd.DataFrame([weight, usefulness, things]).T
solution_data.columns = ['weight', 'usefulness', 'taken']
print(solution_data.head())
