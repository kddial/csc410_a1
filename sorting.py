import sys
from z3 import *

# Checks the usage in the command line
if len(sys.argv) != 2:
    print("Usage: python sorting.py <input_file>")
    sys.exit(0)

# Opens the file passed in the command line for reading
_in = open(sys.argv[1], "r")

# read the list
in_list = _in.readline().strip("[]\n").split(",")
in_list = [i for i in in_list if i!='']
in_list = map(int, in_list)

#########################################################
#     Helper variables, functions, and Z3 variables     #
######################################################### 

# Make n integer variables for input list, and same for out
n = len(in_list)
# X is the input list, where every item must be the same as the input 
X = [Int("x%i" % i) for i in range(n)]
# Y is the output list, which is X but sorted
Y = [Int("y%i" % i) for i in range(n)]

##################  Your Code Here  #####################

#########################################################
#        The actual constraints for the problem         #
#########################################################

##################  Your Code Here  #####################
from itertools import permutations
items = range(n)
P = []
for x in permutations(items):
    P.append(list(x))
# The final formula going in. Change this to your actual formula

# Set X constraints
X_const = ([X[i] == in_list[i] for i in range(n)])

# Set Y constraints
Y_const1 = ([(Y[i] <= Y[i+1]) for i in range(n-1)])
Y_const2 =  [And([Y[i] == X[P[j][i]]  for i in range(n) ]) for j in range(len(P))]

F = And(X_const + Y_const1 + [Or(Y_const2)])

print F
#########################################################
#         Call the solver and print the answer          #
#########################################################

# a Z3 solver instance
solver = Solver()
# add all constraints
solver.add(F)
# run Z3
isSAT = solver.check()
# print the result
if isSAT == sat:
    m = solver.model()
    print([m[Y[i]] for i in range(n)])
else:
    print("Inconceivable! The specification must always be satisfiable.") 