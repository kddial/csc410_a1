import sys
from z3 import *

def z3sort(i,X):
   if len(X) == 1:
      return [Y[i] == X[0]]
   else:
      return [Y[i] == X[0]] + z3sort(i, X[1:])

#def z3sort(n,i,X):
#   if len(X) == 1:
#      return [Y[i] == X[0]]
#   else:
#      return [(Y[i] == X[0], And([Y[z] != X[0] for z in range(n)])] + z3sort(i, X[1:])

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

# The final formula going in. Change this to your actual formula

# Set X constraints
X_const = ([X[i] == in_list[i] for i in range(n)])

# Set Y constraints
Y_const1 = ([(Y[i] <= Y[i+1]) for i in range(n-1)])

# Set Y constraints
#Y2_const = [Or(tuple(Y[i] == X[j] for i in range(n-1) for j in range(n-1)))]
#Y2_const = [Or(tuple(Y[i] == X[1:] for i in range(n-1)))]

Y_const2 = [Or(z3sort(i,X)) for i in range(n)]



#Y_const = Y2_const + Y1_const
#Y_const = Y1_const + Y2_const


#for i in range(n):
#	Y_const = Y_const + [Or(tuple(Y[i] == X[j] for j in range(n)))]

F = And(X_const + Y_const1 + Y_const2)

# debugging purposes
print 'X constraint:', X_const
print 'Y1 constraint:', Y_const1
print 'Y2 constraint:', Y_const2
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

# def z3sort(X):
#    if X=[]:
#       return 0
#    else:
#       return X[0] + z3sum(X[1:])