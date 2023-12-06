# Data Definition#
import random
import numpy as np
n = 10  # Number of Patients LocationsC
c = [i for i in range(n+1) if i != 0]  # List of Patien Locations C
nodes = [0] + c   # List Patient Locations incl. depots CU{0}

# Service Types S
s = [0, 1, 2, 3, 4]

# Set of Staff Members V:
v = [0, 1, 2, 3, 4]

# a equal 1 if employee v is qualified to provide service operation s (5 Staff 5 Types)
a = {(0, 0): 1, (0, 1): 1, (0, 2): 1, (0, 3): 0, (0, 4): 1,
     (1, 0): 1, (1, 1): 0, (1, 2): 0, (1, 3): 1, (1, 4): 0,
     (2, 0): 0, (2, 1): 1, (2, 2): 1, (2, 3): 1, (2, 4): 0,
     (3, 0): 1, (3, 1): 1, (3, 2): 1, (3, 3): 1, (3, 4): 1,
     (4, 0): 1, (4, 1): 0, (4, 2): 1, (4, 3): 0, (4, 4): 1}


# r equal 1 if patient i requires servictype s #ris
"""r = [[0, 0, 0, 0, 1], [0, 0, 0, 1, 0], [0, 1, 0, 0, 0], [1, 0, 0, 0, 0], [0, 0, 0, 0, 1], [
    0, 0, 0, 0, 1], [0, 1, 0, 1, 0], [1, 0, 0, 0, 0], [1, 0, 0, 0, 0], [1, 1, 0, 0, 0]]  # 7+10 eintrag in der Liste ist "Double" (Cd)"""
r = {(0, 0): 0, (0, 1): 0, (0, 2): 0, (0, 3): 0, (0, 4): 0,  # kein Eintrag da Depot
     (1, 0): 0, (1, 1): 0, (1, 2): 0, (1, 3): 1, (1, 4): 0,
     (2, 0): 0, (2, 1): 0, (2, 2): 0, (2, 3): 1, (2, 4): 0,
     (3, 0): 1, (3, 1): 0, (3, 2): 0, (3, 3): 0, (3, 4): 0,
     (4, 0): 0, (4, 1): 0, (4, 2): 0, (4, 3): 0, (4, 4): 1,
     (5, 0): 0, (5, 1): 1, (5, 2): 0, (5, 3): 0, (5, 4): 1,  # doppelt
     (6, 0): 1, (6, 1): 0, (6, 2): 0, (6, 3): 0, (6, 4): 0,
     (7, 0): 0, (7, 1): 1, (7, 2): 1, (7, 3): 0, (7, 4): 0,  # doppelt
     (8, 0): 0, (8, 1): 0, (8, 2): 0, (8, 3): 0, (8, 4): 1,
     (9, 0): 0, (9, 1): 0, (9, 2): 0, (9, 3): 0, (9, 4): 1,
     (10, 0): 0, (10, 1): 0, (10, 2): 1, (10, 3): 0, (10, 4): 0,
     }

# Coordinates
# Fixed X Coordinates for Patients + Depot
X = [55, 10, 80, 85, 65, 5, 80, 50, 55, 145, 140]

# Fixed Y Coordinates for Patients + Depot
Y = [70, 35, 5, 105, 95, 100, 60, 85, 25, 80, 115]
# VP  D   1   2   3   4   5   6   7   8   9   10   D


arcs = [(i, j) for i in nodes for j in nodes if i != j]  # Every Possible Route

# Times Windows {ei;li}: # Time Logic in min: 1440min = 1 day
e = {0: 420,   1: 430,  2: 440,  3: 560,  4: 800,  5: 850,  6: 900,  7: 900,  8: 900,
     9: 920,  10: 1020}  # lower bound for time window
l = {0: 1200, 1: 600, 2: 610, 3: 620, 4: 880, 5: 910, 6: 960, 7: 1020, 8: 960,
     9: 920, 10: 1050}  # upper bound for time window

# Time Distance(gmin, gmax)
gmin = {0: 0,   1: 0,  2: 0,  3: 0,  4: 0,  5: 5,  6: 0,  7: 250,  8: 0,
        9: 0,  10: 0}  # minimal time distance between service start times
gmax = {0: 0,   1: 0,  2: 0,  3: 0,  4: 0,  5: 35,  6: 0,  7: 250,  8: 0,
        9: 0,  10: 0}  # maximal time distance between service start times
# Location 7 wird nun in Csim, Location 10 wird Cprec (siehe ris, doppelter Type)

# processing time p of a servicetype s at patient i
p = {(0, 0): 0, (0, 1): 0, (0, 2): 0, (0, 3): 0, (0, 4): 0,  # kein Eintrag da Depot
     (1, 0): 100, (1, 1): 200, (1, 2): 150, (1, 3): 300, (1, 4): 70,
     (2, 0): 100, (2, 1): 200, (2, 2): 150, (2, 3): 300, (2, 4): 70,
     (3, 0): 100, (3, 1): 200, (3, 2): 150, (3, 3): 300, (3, 4): 70,
     (4, 0): 100, (4, 1): 200, (4, 2): 150, (4, 3): 300, (4, 4): 70,
     (5, 0): 100, (5, 1): 200, (5, 2): 150, (5, 3): 300, (5, 4): 70,  # doppelt
     (6, 0): 100, (6, 1): 200, (6, 2): 150, (6, 3): 300, (6, 4): 70,
     (7, 0): 100, (7, 1): 200, (7, 2): 150, (7, 3): 300, (7, 4): 70,  # doppelt
     (8, 0): 100, (8, 1): 200, (8, 2): 150, (8, 3): 300, (8, 4): 70,
     (9, 0): 100, (9, 1): 200, (9, 2): 150, (9, 3): 300, (9, 4): 70,
     (10, 0): 100, (10, 1): 200, (10, 2): 150, (10, 3): 300, (10, 4): 70,
     }
