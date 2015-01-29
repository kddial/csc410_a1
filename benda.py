import sys
from z3 import *

# Checks the usage in the command line
if len(sys.argv) != 2:
    print("Usage: python benda.py <input_file>")
    sys.exit(0)

# Opens the file passed in the command line for reading
_in = open(sys.argv[1], "r")

in_list = _in.readline().strip("[]\n").split(",")
in_list = [i for i in in_list if i!='']
in_list = map(int, in_list)

#########################################################
#     Helper variables, functions, and Z3 variables     #
######################################################### 


##################  Your Code Here  #####################


#########################################################
#        The actual constraints for the problem         #
#########################################################


##################  Your Code Here  #####################

# The final formula going in. Change this to your actual formula
F = simplify(Bool('p')==Bool('p'))

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

    ##################  Your Code Here  #####################
    #           print the answer using the model            #
    ##################  Your Code Here  #####################

    print("Bender's back!.")
else:
    print("Hey! Don't violate Keeler's Theorem.")

