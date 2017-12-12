# Written by Amir Ilkhechi (Emir Yilkici)
# The printed result shows a list of customers and the route to which they belong, therefore there
# can be duplicate routes in the printed results.

import math
import random
from operator import itemgetter
from copy import deepcopy
import numpy as np
import pylab
import sys

sys.setrecursionlimit(15000)

#filename = str(sys.argv[1])
filename = "151_15_1.vrp"
f = open(filename, "r")
lines = f.readlines()

# depot and customers, [index, x, y, demand]
depot = [] #[0, 30.0, 40.0, 0]
customers = []

# template of data:
'''[[1, 37.0, 52.0, 7],
[2, 49.0, 49.0, 30],
[3, 52.0, 64.0, 16],
[4, 20.0, 26.0, 9],
[5, 40.0, 30.0, 21],
[6, 21.0, 47.0, 15],
[7, 17.0, 63.0, 19],
[8, 31.0, 62.0, 23],
[9, 52.0, 33.0, 11],
[10, 51.0, 21.0, 5],
[11, 42.0, 41.0, 19],
[12, 31.0, 32.0, 29],
[13, 5.0, 25.0, 23],
[14, 12.0, 42.0, 21],
[15, 36.0, 16.0, 10]] '''

numbers = lines[0].split()
customerCount = int(numbers[0])
k_ = int(numbers[1])
vehicleCount = int(numbers[1])
vehicleCapacity = int(numbers[2])
assigned = [-1] * customerCount

#depot = map(int, map(float, lines[1].split()))

for i in xrange(1, len(lines)):
    numbers = map(int, map(float, lines[i].split()))
    customers.append([i, numbers[1], numbers[2], numbers[0]])

distances = [[0 for x in range(customerCount)] for y in range(customerCount)]

for i in xrange(0, customerCount):
    for j in xrange(0, customerCount):
            distances[i][j] = math.sqrt((customers[i][0] - customers[j][0])**2 + (customers[i][1] - customers[j][1])**2)

def combine_routes(n1, n2, r1, r2, opt):
    newR = []
    if opt == 0:
        newR = [0, n1, n2, 0]
    elif opt == 1:
        if r2[-2] == n2:
            newR = newR + r2[0:-1]
            newR = newR + [n1, 0]
        if r2[1] == n2:
            newR = newR + [0, n1]
            newR = newR + r2[1:]
    else:
        if r1[1] == n1 and r2[1] == n2:
            rev_r1 = r1[::-1]
            newR = newR + rev_r1[:-1]
            newR = newR + r2[1:]
        elif r1[1] == n1 and r2[-2] == n2:
            newR = newR + r2[0:-1]
            newR = newR + r1[1:]
        elif r1[-2] == n1 and r2[1] == n2:
            newR = newR + r1[0:-1]
            newR = newR + r2[1:]
        else:
            rev_r2 = r2[::-1]
            newR = newR + r1[0:-1]
            newR = newR + rev_r2[1:]

    return  newR

def compute_tot_demand(r):
    demands = [customers[i][3] for i in r[1:-1]]
    return  sum(demands)

def is_external(n, r):
    if r[-2] == n or r[1] == n:
        return True
    return False

global routes, savings, node_to_route

routes = []
node_to_route = []

for i in xrange(0, customerCount):
    routes.append([0, i, 0])

savings = []
node_to_route = [[0, i, 0] for i in range(0, customerCount)]

# 1 - compute the savings
for i in xrange(1, customerCount):

    for j in xrange(i + 1, customerCount):
        if not i == j:
            sv = distances[0][i] + distances[0][j] - distances[i][j]
        else:
            sv = 0
        savings.append([[i, j], sv])

# 2 - sort according to the saving amount in descending order
savings = sorted(savings, key=itemgetter(1), reverse=True)

# 3 - CW loop
def CW():

    if len(savings) == 0:
        return

    chosen = savings[0]
    savings.remove(chosen)
    n1 = chosen[0][0]
    n2 = chosen[0][1]

    r1 = node_to_route[n1]
    r2 = node_to_route[n2]

    if len(r1) == 3 and len(r2) == 3:
        new_r = combine_routes(n1, n2, r1, r2, 0)
        if compute_tot_demand(new_r) <= vehicleCapacity:
            for i in xrange(0, len(new_r)):
                node = new_r[i]
                node_to_route[node] = new_r
    if len(r1) == 3 and len(r2) > 3:
        if is_external(n2, r2):
            new_r = combine_routes(n1, n2, r1, r2, 1)
            if compute_tot_demand(new_r) <= vehicleCapacity:
                for i in xrange(0, len(new_r)):
                    node = new_r[i]
                    node_to_route[node] = new_r
    if len(r1) > 3 and len(r2) == 3:
        if is_external(n1, r1):
            new_r = combine_routes(n2, n1, r2, r1, 1)
            if compute_tot_demand(new_r) <= vehicleCapacity:
                for i in xrange(0, len(new_r)):
                    node = new_r[i]
                    node_to_route[node] = new_r
    if len(r1) > 3 and len(r2) > 3:
        if is_external(n1, r1) and is_external(n2, r2):
            new_r = combine_routes(n1, n2, r1, r2, 2)
            if compute_tot_demand(new_r) <= vehicleCapacity:
                for i in xrange(0, len(new_r)):
                    node = new_r[i]
                    node_to_route[node] = new_r

    CW()

def main():
    CW()
    for i in xrange(0, customerCount):
        print "route for customer ", i, " ", node_to_route[i]
if __name__ == '__main__':
    main()
