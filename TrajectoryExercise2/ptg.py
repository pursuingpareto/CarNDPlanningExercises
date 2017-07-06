import numpy as np


def PTG(start, goal, T, predictions):
	"""
	Returns a polynomial trajectory connecting (or almost connecting)
	start to goal over a duration of approximately T seconds. This
	trajectory should avoid collisions with any of the vehicles given
	in predictions.

	INPUTS

	start - length 6 array corresponding to INITIAL values of:
	  [s, s_dot, s_double_dot, d, d_dot, d_double_dot]

	goal - length 6 array corresponding to FINAL values of state variables.

	T - desired duration of maneuver (in seconds)

	predictions - array of vehicle predictions. Each "vehicle prediction" 
	  is itself an array of (s,d,t) coordinates. The example below shows 
	  predictions for two vehicles. The first moves along at 1 m/s at d=0, 
	  while the second moves at 3 m/s and changes from d=4 to d=0.

	  example - [
	  	[
	  		(0, 0, 0),
	  		(1, 0, 1),
	  		(2, 0, 2),
	  		(3, 0, 3)
	  	],
	  	[
	  		(0, 4, 0),
	  		(3, 4, 1),
	  		(6, 2, 2),
	  		(9, 0, 3)
	  	]
	  ] 
	"""
###################
#
# HELPER FUNCTIONS
#
def JMT(start, end, T):
	"""
	Helper function. Given a length THREE start and end state (corresponding
		to boundary conditions in s OR d) and a desired duration (T), 
		returns the 6 coefficients associated w/ the corresponding JMT.
	"""
    a_0, a_1, a_2 = start[0], start[1], start[2] / 2.0
    c_0 = a_0 + a_1 * T + a_2 * T**2
    c_1 = a_1 +  a_2 * T
    c_2 = 2 * a_2
    
    A = np.array([
            [  T**3,   T**4,    T**5],
            [3*T**2, 4*T**3,  5*T**4],
            [6*T,   12*T**2, 20*T**5],
        ])
    B = np.array([
            end[0] - c_0,
            end[1] - c_1,
            end[2] - c_2
        ])
    a_3_4_5 = np.linalg.solve(A,B)
    print a_3_4_5
    alphas = np.concatenate([np.array([a_0, a_1, a_2]), a_3_4_5])
    return alphas

def coefficients_to_points(s_coeffs, d_coeffs, horizon=5.0, timestep=1.0):
	
	def s(t):
		value = 0
		for i, coeff in enumerate(s_coeffs):
			value += (coeff * t**i)
		return value
	
	def d(t):
		value = 0
		for i, coeff in enumerate(d_coeffs):
			value += (coeff * t**i)
		return value

	t = 0
	points = []
	while t <= horizon:
		point = (s(t), d(t), t)
		points.append(point)
		t += timestep
	return points