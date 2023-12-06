from gurobipy import Model, quicksum, GRB
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import data
from color import Color

# Assign Data from data file
nodes = data.nodes  # all Locations with Deposit
staff_members = data.v
patients = data.c
n = data.n  # 10 Patienten
service_types = data.s
qualificiation = data.a
requirements = data.r
distanceservice_min = data.gmin
distanceservice_max = data.gmax
window_lowerbound = data.e
window_upperbound = data.l
processing_time = data.p
arcs = data.arcs
X = data.X
Y = data.Y
M = 100000
# Zuerst erstelle das Dictionary wie zuvor
distance = {(i, j): np.hypot(X[i]-X[j], Y[i]-Y[j])
            * 0.5 for i in nodes for j in nodes if i != j}
distance[(0, 0)] = 0

lambda1 = 0.9
lambda2 = 0.05
lambda3 = 1.0 - lambda1 - lambda2


# ---------Problem Definition----------#
model = Model('HHCRSP')
# Gurobi minimizes normally so this step is theoretically unecessary
model.ModelSense = GRB.MINIMIZE

arc_var = [(i, j, v, s)
           for i in nodes for j in nodes for v in staff_members for s in service_types if i != j]  # xijvs
arc_time = [(i, v, s)
            for i in nodes for v in staff_members for s in service_types]  # tivs
arc_tardiness = [(i, s) for i in nodes for s in service_types]  # zis

# Decision Variables:
x = model.addVars(arc_var, vtype=GRB.BINARY, name='x')
t = model.addVars(arc_time, vtype=GRB.CONTINUOUS, name='t')
z = model.addVars(arc_tardiness, vtype=GRB.CONTINUOUS, name='z')

D = model.addVar(vtype=GRB.CONTINUOUS, name='D')
T = model.addVar(vtype=GRB.CONTINUOUS, name='T')
Tmax = model.addVar(vtype=GRB.CONTINUOUS, name='Tmax')

model.setObjective(lambda1*D + lambda2*T + lambda3 * Tmax, GRB.MINIMIZE)
# model.setObjective(D, GRB.MINIMIZE)

# ---------Constraints----------
# Constraint 2
model.addConstr(D == quicksum(x[i, j, v, s] * distance[i, j]
                              for i in nodes for j in nodes for v in staff_members for s in service_types if i != j))

# Constraint 3
model.addConstr(T == quicksum(z[i, s]
                              for i in patients for s in service_types))

# Constraint 4
model.addConstrs(Tmax >= z[i, s] for i in patients for s in service_types)

# Constraint 5
model.addConstrs(quicksum(x[0, i, v, s]
                 for i in nodes if i != 0 for s in service_types) == 1 for v in staff_members)
model.addConstrs(quicksum(x[i, 0, v, s]
                 for i in nodes if i != 0 for s in service_types) == 1 for v in staff_members)  # evtl n+1/0 nehmen

# Constraint 6
model.addConstrs(quicksum(x[j, i, v, s] for j in nodes if j != i for s in service_types) == quicksum(
    x[i, j, v, s] for j in nodes if i != j for s in service_types) for i in patients for v in staff_members)

# Constraint 7
model.addConstrs(quicksum(qualificiation[v, s] * x[j, i, v, s]
                          for v in staff_members for j in nodes if j != i) == requirements[i, s] for i in patients for s in service_types)

# Constraint 8
model.addConstrs(t[i, v, s1] + (processing_time[i, s1] + distance[i, j]) <= (t[j, v, s2] + M * (1-x[i, j, v, s2]))
                 for i in nodes for j in patients if i != j for v in staff_members for s1 in service_types for s2 in service_types)

# Constraint 9
model.addConstrs(t[i, v, s] >= window_lowerbound[i]
                 for i in patients for v in staff_members for s in service_types)

# Constraint 10
model.addConstrs(t[i, v, s] <= window_upperbound[i]  # hier problem mit zis, löscht man die Zeile code kommen sinnvolle ergebnisse raus
                 for i in patients for v in staff_members for s in service_types)

# Constraint 11
model.addConstrs(t[i, v2, s2] - t[i, v1, s1] >= distanceservice_min[i] - M * (2 - quicksum(x[j, i, v1, s1] - x[j, i, v2, s2] for j in nodes if i != j))
                 for i in patients if sum(requirements[i, s] for s in service_types) > 1 for v1 in staff_members for v2 in staff_members for s1 in service_types for s2 in service_types)

# Constraint 12
model.addConstrs(t[i, v2, s2] - t[i, v1, s1] <= distanceservice_max[i] + M * (2 - quicksum(x[j, i, v1, s1] - x[j, i, v2, s2] for j in nodes if i != j))
                 for i in patients if sum(requirements[i, s] for s in service_types) > 1 for v1 in staff_members for v2 in staff_members for s1 in service_types for s2 in service_types)

# --6--#
model.addConstrs(window_lowerbound[i] <= t[i, k, s]
                 for k in staff_members for i in nodes if i == 0 or i == (n+1)for s in service_types)
model.addConstrs(t[i, k, s] <= window_upperbound[i]
                 for k in staff_members for i in nodes if i == 0 or i == (n+1) for s in service_types)

# Constraint 13
# model.addConstrs(
#    (x[i, j, v, s] >= 0 for i in nodes for j in nodes for v in staff_members for s in service_types if i != j))
# model.addConstrs((x[i, j, v, s] <= qualificiation[v, s] * requirements[j, s]
#                  for i in nodes for j in nodes for v in staff_members for s in service_types if i != j))

# Constraint 14
# siehe decision Variable

# Constraint 15

# Constraint 16
# Cosntraint 17
# Constraint 18
# Constraint 18


# ---------Optimizing the Model----------#
# Optimizing the Model
model.optimize()

# Überprüfen, ob das Modell erfolgreich gelöst wurde
if model.status == GRB.OPTIMAL:
    # Drucken Sie den Objective Value
    print("Objective Value: ", str(round(model.getAttr("ObjVal"), 2)))
    for v in model.getVars():
        if v.x > 0.9:
            print(str(v.VarName)+"="+str(v.x))

else:
    print("Gurobi Optimization was not successful. Status code:", model.status)
    print(model.setParam('OutputFlag', 1))
