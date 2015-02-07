import sys
from z3 import *

# Checks the usage in the command line
if len(sys.argv) != 2:
    print("Usage: python knapsack.py <input_file>")
    sys.exit(0)

# Opens the file passed in the command line for reading
_in = open(sys.argv[1], "r")

# Value required 
V = int(_in.readline())
# knapsack weight
W = int(_in.readline())

# items, as a list of value-weight pairs
items = _in.readline().strip("[]\n").split("],[")
items = [i for i in items if i!='']
items = map(lambda p: map(int, p.split(",")), items)

#########################################################
#     Helper variables, functions, and Z3 variables     #
######################################################### 


##################  Your Code Here  #####################


#########################################################
#        The actual constraints for the problem         #
#########################################################

##################  Your Code Here  #####################

# Setup for python variables
n = len(items)

# Setup for Z3 variables
Vl = [Int("V%i" % i) for i in range(n)] # value list
Wl = [Int("W%i" % i) for i in range(n)] # weight list
CV = [Int("CV%i" % i) for i in range(n)] # chosen values
CW = [Int("CW%i" % i) for i in range(n)] # chosen weights
CVi = [Int("CVi%i" % i) for i in range(n)] # chosen value index
CWi = [Int("CWi%i" % i) for i in range(n)] # chosen weight index
TV = Int("TV") # chosen value total
TW = Int("TW") # chosen weight total
Z = Int("Z") # maximizing value
K = Int("K") # all other values
S = [Int("S%i" % i) for i in range(n)] # solution array

# Functions
def z3sum(X): # From instructors hint on Piazza @58
   if X == []:
      return 0
   else:
      return X[0] + z3sum(X[1:])

def range_j(n, j):
   result = range(0, j) + range(j + 1, n)
   return result

def knapsack(items, Z, Vl, Wl, CV, CW, CVi, CWi, TV, TW, S): # Maximizing Z
    return And(knapsack_helper(items, Z, Vl, Wl, CV, CW, CVi, CWi, TV, TW, S), 
               ForAll(K, Implies(knapsack_helper(items, K, Vl, Wl, CV, CW, CVi, CWi, TV, TW, S), K <= Z)))

def knapsack_helper(items, Z, Vl, Wl, CV, CW, CVi, CWi, TV, TW, S):
	c1 = And([Vl[i] == items[i][0] for i in range(n)]) # Loading in value values
	c2 = And([Wl[i] == items[i][1] for i in range(n)]) # Loading in weight values
	c3 = (z3sum(Vl) >= V) # Max possible value of summing all items must exceed min value
	c4 = And([Or([And(CW[j] == Wl[i], CWi[j] == i) for i in range(n)] + [And(CW[j] == 0, CWi[j] == -1)]) for j in range(n)]) # Choosing item weights and setting the index for the choice made
	c5 = And([Or([And(CV[j] == Vl[i], CVi[j] == i) for i in range(n)] + [And(CV[j] == 0, CVi[j] == -1)]) for j in range(n)]) # Choosing item values and setting the index for the choice made
	c6 = (TW <= W) # total weight cannot exceed specified maximum
	c7 = (TV >= V) # total value must exceed specified minimum
	c8 = And([Implies(CWi[i] == CVi[j], CWi[i] == -1) for i in range(n) for j in range_j(n,i)]) # The only shared index should be negative 1. The helper takes i out of range(n)
	c9 = And([CWi[i] == CVi[i] for i in range(n)]) # Matching indexes
	c10 = And([Implies((TW + Wl[i]) <= W, Or([CWi[z] == i for z in range(n)])) for i in range(n)]) # An item being addable implies that it should have been added. Maximizing locally
	c11 = And([Implies(CVi[i] == j, S[j] == True) for i in range(n) for j in range(n)]) # Building solution array using chosen indexes
	c12 = And([Implies(And([CVi[j] != i for j in range(n)]), S[i] == False) for i in range(n)]) # Building solution array using chosen indexes
	c13 = (TV == z3sum(CV)) # Setting values for the totals
	c14 = (TW == z3sum(CW)) # Setting values for the totals
	c15 = (Z <= TV) # Variable to be maximized by the quantifier one step up
	return And(c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, c13, c14, c15)

F = knapsack(items, Z, Vl, Wl, CV, CW, CVi, CWi, TV, TW, S)

##########################################################
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
   	# print F
    # print'Values:'
    # print([m[Vl[i]] for i in range(n)])
    # print'Weights:'
    # print([m[Wl[i]] for i in range(n)])
    # print'Chosen Values:'
    # print([m[CV[i]] for i in range(n)])
    # print'Chosen Weights:'
    # print([m[CW[i]] for i in range(n)])
    # print'Value Index:'
    # print([m[CVi[i]] for i in range(n)])
    # print'Weight Index:'
    # print([m[CWi[i]] for i in range(n)])
    # print'Total:'
    # print(m[Z])
    # print'Total Value'
    # print(m[TV])
    # print'Total Weight:'
    # print(m[TW])
    # print'Solution:'
    # print([m[S[i]] for i in range(n)])
    print([m[S[i]] for i in range(n)])
    print(m[Z])
    print(m[TW])
    ##################  Your Code Here  #####################
    #           print the answer using the model            #
    ##################  Your Code Here  #####################
    
    print("NP-Completed.")
else:
    print("This is NP too hard.")