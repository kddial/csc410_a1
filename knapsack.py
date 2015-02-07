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

# The final formula going in. Change this to your actual formula

z,k = Ints('z k')
#setup python variables
n = len(items)
CV = [Int("CV%i" % i) for i in range(n)] # chosen values
CW = [Int("CW%i" % i) for i in range(n)] # chosen weights

#z3 helper functions
def z3sum(X): # From instructors hint on Piazza @58
   if X == []:
      return 0
   else:
      return X[0] + z3sum(X[1:])

def range_j(n, j):
   result = range(0, j) + range(j + 1, n)
   #if j != -1:
   		#result.append(-1)
   return result

def gcd(items,z,CV,CW):
    return And(common_divisor(items,z,CV,CW), 
               ForAll(k,Implies(common_divisor(items,k,CV,CW),k<=z)))

def common_divisor(items,z,CV,CW):

	#setup Z3 variables
	Vl = [Int("V%i" % i) for i in range(n)] # value list
	Wl = [Int("W%i" % i) for i in range(n)] # weight list
	#CV = [Int("CV%i" % i) for i in range(n)] # chosen values
	#CW = [Int("CW%i" % i) for i in range(n)] # chosen weights
	CVi = [Int("CVi%i" % i) for i in range(n)] # chosen value index
	CWi = [Int("CWi%i" % i) for i in range(n)] # chosen weight index
	#TV = [Int("TV%i" % i) for i in range(n)] # total value
	c1 = And([Vl[i] == items[i][0] for i in range(n)])
	c2 = And([Wl[i] == items[i][1] for i in range(n)])
	c3 = (z3sum(Vl) >= V) # Max possible value of summing all items must exceed min value
	c4 = And([Or([And(CW[j] == Wl[i], CWi[j] == i) for i in range(n)] + [And(CW[j] == 0, CWi[j] == -1)]) for j in range(n)])
	c5 = And([Or([And(CV[j] == Vl[i], CVi[j] == i) for i in range(n)] + [And(CV[j] == 0, CVi[j] == -1)]) for j in range(n)])
	c6 = (z3sum(CW) <= W)
	c7 = (z3sum(CV) >= V)
	c8 = And([CV[i] >= CV[i+1] for i in range(n-1)])
	c9 = And([CWi[i] != CVi[j] for i in range(n) for j in range_j(n,i)]) # The helper takes i out of range(n) # but = -1 is fine
	c9 = And([Or(CWi[i] != CVi[j], CWi[i] == -1) for i in range(n) for j in range_j(n,i)]) # The helper takes i out of range(n) # but = -1 is fine
	c10 = And([CWi[i] == CVi[i] for i in range(n)])
	c11 = And(z == z3sum(CV))
	#c10 = And(z == 0)
	#c10 = True
	#c10 = And(z > V, z <= z3sum(CV))

	return And(c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11)


F = gcd(items,z,CV,CW)
#F = common_divisor(items, z, CV, CW)
print F
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
    #print m
    print'Values:'
    print([m[CV[i]] for i in range(n)])
    print'Weights:'
    print([m[CW[i]] for i in range(n)])
    #print m
    print'Z:'
    print(m[z])
    print'K:'
    print(m[k])
    ##################  Your Code Here  #####################
    #           print the answer using the model            #
    ##################  Your Code Here  #####################
    
    print("NP-Completed.")
else:
    print("This is NP too hard.")

#c3 = (MV == z3sum(Vl))
#c4 = (MV >= V) # Max possib
# CV = [Int("CV%i" % i) for i in range(n)]
# CW = [Int("CW%i" % i) for i in range(n)]


# c1 = And([Vl[i] == items[i][0] for i in range(n)])
# c2 = And([Wl[i] == items[i][1] for i in range(n)])
# c3 = (z3sum(Vl) >= V) # Max possible value of summing all items must exceed min value
# c4 = Or([CW[j] == Wl[i] for i in range(n) for j in range(n)] + [CW[i] == 0 for i in range(n)])
# c5 = Or([CV[j] == Vl[i] for i in range(n) for j in range(n)] + [CV[i] == 0 for i in range(n)])
# c6 = (z3sum(CW) < W)
# c7 = (z3sum(CV) > V)

# c2 = Or([Wl[j] == items[i][0]  for i in range(n) for j in range(n)] + [Wl[i] == 0 for i in range(n)])
# c3 = Or([Vl[j] == items[i][1]  for i in range(n) for j in range(n)] + [Vl[i] == 0 for i in range(n)])
# c4 = (z3sum(Wl) < W)
# # c5 = (z3sum(Vl) > V)

# c4 = And([Or([CW[j] == Wl[i] for i in range(n)] + [Wl[j] == 0]) for j in range(n)] + [CW[i] == 0 for i in range(n)])
# c5 = And([Or([CV[j] == Vl[i] for i in range(n)] + [Vl[j] == 0]) for j in range(n)] + [CV[i] == 0 for i in range(n)])

#And([ for i in range(n)])

#c4 =  [And([CW[i] == Wl[P[j][i]]  for i in range(n) ]) for j in range(len(P))]

# c2 = And([Wl[i] == items[i][1] for i in range(n)])
# c3 = (z3sum(Vl) >= V) # Max possible value of summing all items must exceed min value
# c4 = And([Or([CW[j] == Wl[i] for i in range(n)] + [CW[j] == 0]) for j in range(n)])
# c5 = And([Or([CV[j] == Vl[i] for i in range(n)] + [CV[j] == 0]) for j in range(n)])
# c6 = (z3sum(CW) < W)
# c7 = (z3sum(CV) > V)
# c8 = And([CV[i] != CV[j] for i in range(n)])

#constraints
#c1 = (z3sum(items[i][0]) >= V) # Max possible value of summing all items must exceed min value
# c2 = And([Or([Wl[j] == items[i][0]  for i in range(n)] + [Wl[j] == 0]) for j in range(n)])
# c3 = And([Or([Vl[j] == items[i][1]  for i in range(n)] + [Vl[j] == 0]) for j in range(n)])
# c4 = (z3sum(Wl) < W)
# c5 = (z3sum(Vl) > V)
#c5 = Or([CW[j] == Wl[i] for i in range(n) for j in range(n)])

# c4 = And([Or(And([CW[j] == Wl[i], CWi[j] == i)) for i in range(n)] + [CW[j] == 0]) for j in range(n)])
# c5 = And([Or(And([CV[j] == Vl[i], CVi[j] == i)) for i in range(n)] + [CV[j] == 0]) for j in range(n)])
#c4 = And([Or([CW[j] == Wl[i] for i in range(n)] + [CW[j] == 0]) for j in range(n)])
#c5 = And([Or([CV[j] == Vl[i] for i in range(n)] + [CV[j] == 0]) for j in range(n)])


#from itertools import permutations
#items = range(n)
#P = []
#for x in permutations(items):
#    P.append(list(x))
