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

#########################################################
#     Helper variables, functions, and Z3 variables     #
######################################################### 

# Constraint variables
s = Int('s')
t = Int('t')
u = Int('u')

# Two extra bodies to use for swapping.
# Will be in index n+1, n+2.
n_bodies = n+2

# Total number of game states is equal
# to the total possible pair combinations. Which 
# is equal to (n Choose k) where n is the number of 
# bodies and k = 2. Therefore total game states is 
# n*(n-1)/2.
total_states = n_bodies * (n_bodies - 1) / 2

# Keep track of all the bodies in a game state with 
# variable X. X[k] represents a z3 array of the minds at
# game state k. 
X = [ Array("x_%s" % i, IntSort(), IntSort()) for i in range(total_states) ]

# Keep track of all the swapped pairs that occured
# at each game state. Note, since only 1 swap occurs at each game state,
# there can only be k swaps at game state k. 
# Example: Swap[0]=[], Swap[1]=[[0,1]], Swap[2]=[[0,1],[1,2]]

# Ideally I would like to represent each Z3 value as a pair, but I am
# restricted to integers, so as an alternative I created two variables
# to represent index 0 and index 1 of each pair.
# Example: 
#       Swap[2][0] = [0,1] => 
#		Swap_zero[2][0]=0, Swap_one[2][0]=1
Swap_zero = [ Array("swap_zero_%s" % i, IntSort(), IntSort()) for i in range(total_states) ]
Swap_one = [ Array("swap_one_%s" % i, IntSort(), IntSort()) for i in range(total_states) ]

# Variables that represent the input values
# and the expected end values. The end values
# are where each mind is in the correct body.
start = [ Int("start_%s" % i) for i in range(n_bodies)]
end = [ Int("end_%s" % i) for i in range(n_bodies)]

#########################################################
#        The actual constraints for the problem         #
#########################################################

# Set start to equal input values
start_const = [start[i] == in_list[i] for i in range(n)]
start_const = start_const + [start[n] == n, start[n+1] == n+1]

# Set end to equal the minds in the correct bodies.
# Since body_i must contain mind_i, then we can set
# end[i] == i.
end_const = [end[i] == i for i in range(n_bodies)]

# The initial game state
game_state_initial = [ X[0][i] == start[i] for i in range(n_bodies) ]

# The core constraints
reduce_c = [
	# If the game state equals the end state, then the problem is satisfied
	If(
		And([X[k-1][z]==end[z] for z in range(n_bodies)]),

		# If true, then the game state should stay the same
		# until all the moves are used
		And([X[k][i] == X[k-1][i] for i in range(n_bodies)]),

		And(
			# If false, then set constraints to swap bodies.
			# Constraints breakdown:
			# s and t are indicies to be switched. They can not equal each other.
			# Set X[s] in current game state k, to equal X[t] in game state k-1, 
			# and vice versa to swap the values.
			ForAll(s, ForAll(t, Implies(
				And(
					s != t, s >= 0, s < n_bodies, t >= 0, t < n_bodies, 
					u != s, u != t, i >= 0, u < n_bodies),
				And(
					X[k][s] == X[k-1][t],
					X[k][t] == X[k-1][s],
					X[k][u] == X[k-1][u]
				))))
			,

			# Make sure the swapped values have not been used in the
			# previous game state.
			# We only have to check the swaps from the previous game state 
			# because every game state is an accumulation of the previous swaps.
			# We make sure that (s,t) and (t,s) does not match any previous swaps
			And([And(Swap_zero[k-1][i] != s, Swap_one[k-1][i] != t) for i in range(k+1)]),
			And([And(Swap_zero[k-1][i] != t, Swap_one[k-1][i] != s) for i in range(k+1)]),

			# Save the swapped value into z3 arrays Swap_zero and Swap_one.
			And(Swap_zero[k][k]==s, Swap_one[k][k]==t)
		)
	)
	# for k in range(1,total_states)]
	for k in range(1,total_states)]

print("------------------")
print("GAME initial:")
print game_state_initial

print("------------------")
print("reduce C:")
print reduce_c
# The final formula going in. Change this to your actual formula
F = start_const + end_const + game_state_initial + reduce_c

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
    print("Swap_zero: ")
    print([m[Swap_zero[i]] for i in range(total_states)])
    print("----------------------")
    print("Swap_one: ")
    print([m[Swap_one[i]] for i in range(total_states)])
    print("----------------------")
    print "Model:"
    print m
    print("----------------------")
    print("X: ")
    print([m[X[i]] for i in range(total_states)])

    print("----------------------")
    print("Bender's back!.")
else:
    print("Hey! Don't violate Keeler's Theorem.")

