import sys
from z3 import *

# Checks the usage in the command line
if len(sys.argv) != 2:
    print "Usage: python sorting.py <input_file>"
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
F = simplify(Bool('p')==Bool('p'))

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
    print [m[Y[i]] for i in range(n)]
else:
    print "Inconceivable! The specification must always be satisfiable."

