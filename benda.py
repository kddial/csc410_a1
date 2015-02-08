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
# at each game state. Note, since only one swap occurs
# during each game state, we will use a 1D array where
# the k index represents the swap on the k-th game state.

# Ideally I would like to represent each Z3 value as a pair, but I am
# restricted to integers, so as an alternative I created two variables
# to represent index 0 and index 1 of each pair.
# Example: 
# [(1,2), (3,4)] <=>
#  swap_zero = [1,3]
#  swap_one =  [2,4]
Swap_zero = [ Int("swap_zero_%s" % i) for i in range(total_states)]
Swap_one = [ Int("swap_one_%s" % i) for i in range(total_states)]

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

# Set the intial swap values. The first swap would be
# the bad swap that rearranged the minds into the wrong
# bodies. We had to initialize this swap because
# we have to keep a log of all the past swaps to satisfy
# the constraint of switching between two bodies only once.
# If this swap was not initialized, then the solver would fine
# a solution in one swap, which was the reverse of the bad swap.
swap_zero_initial = [ Swap_zero[0] == start[0] ]
swap_one_initial = [ Swap_one[0] == start[1] ]
swap_const = swap_zero_initial + swap_one_initial

# The core constraints
reduce_c = [
	# If the previous game state equals the end state, then the problem is satisfied
	If(
		And([X[k-1][z]==end[z] for z in range(n_bodies)]),

		# If true, then the game state should stay the same
		# until all the moves are used.
		And([X[k][i] == X[k-1][i] for i in range(n_bodies)]),

		And(
			# If false, then set constraints to swap bodies.
			# Constraints breakdown:
			# s and t are indicies to be switched. They can not equal each other.
			ForAll(s, 
				ForAll(t, 
					Implies(
						And(
							s >= 0, s < n_bodies, 
							t >= 0, t < n_bodies, 
							u >= 0, u < n_bodies,
							s != t, u != s, u != t
						),
						And(
							# Set X[s] in current game state k, to equal X[t] in game state k-1, 
							# and vice versa to swap the values.
							X[k][s] == X[k-1][t],
							X[k][t] == X[k-1][s],
							X[k][u] == X[k-1][u],

							# Make sure the swapped values have not been used in any
							# previous game state.
							# We make sure that (s,t) and (t,s) does not match any previous swaps
							And([And(Swap_zero[j] != s, Swap_one[j] != t) for j in range(k)]),
							And([And(Swap_zero[j] != t, Swap_one[j] != s) for j in range(k)]),
							
							# Save the swapped value into z3 arrays Swap_zero and Swap_one.
							And(Swap_zero[k]==s, Swap_one[k]==t)
						)
					)
				)
			)
		)
	)
	for k in range(1,total_states)]

# The final formula going in. Change this to your actual formula
F = start_const + end_const + game_state_initial + swap_const + reduce_c

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
    # Contruct pair list
    temp = [m[Swap_zero[i]] for i in range(total_states)]
    temp2 = [m[Swap_one[i]] for i in range(total_states)]
    swap_zero_result = [(temp[i], temp2[i]) for i in range(total_states)]
    print swap_zero_result[1:]
else:
    print("Hey! Don't violate Keeler's Theorem.")

