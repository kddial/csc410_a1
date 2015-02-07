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
n = len(in_list)
n_extra_range = range(n+2)

#########################################################
#     Helper variables, functions, and Z3 variables     #
######################################################### 

print in_list

swapped_pairs = []

start = [ Int("start_%s" % i) for i in n_extra_range]
end = [ Int("end_%s" % i) for i in n_extra_range]

print start
print end

# Set start to equal input
start_const = [start[i] == in_list[i] for i in range(n)]
start_const = start_const + [start[n] == n, start[n+1] == n+1]

# Set end to equal correct bodies
# Since body_i must contain mind_i, then we can just set 
# the constraint that the end[i] == i
end_const = [end[i] == i for i in n_extra_range]



swap_const = []






##################  Your Code Here  #####################


#########################################################
#        The actual constraints for the problem         #
#########################################################


##################  Your Code Here  #####################

# The final formula going in. Change this to your actual formula
F = start_const + end_const
print("------------------")
print("F:")
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
    ##################  Your Code Here  #####################
    #           print the answer using the model            #
    ##################  Your Code Here  #####################
    print("----------------------")
    print("Start: ")
    print([m[start[i]] for i in range(n)])
    print("----------------------")
    print("End: ")
    print([m[end[i]] for i in range(n)])
    print("----------------------")
    print("Bender's back!.")
else:
    print("Hey! Don't violate Keeler's Theorem.")

