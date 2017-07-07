import numpy as np
import random
from cost_functions import *
from constants import *

WEIGHTED_COST_FUNCTIONS = [
    (time_diff_cost,    0),
    (s_diff_cost,       1),
    (d_diff_cost,       1),
    (efficiency_cost,   1),
    (max_jerk_cost,     0),
    (total_jerk_cost,   0),
    (collision_cost,    0),
    (buffer_cost,       0),
    (max_accel_cost,    0),
    (total_accel_cost,  0),
]

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
def PTG(start_s, start_d, target_vehicle, delta, T, predictions):
    target = predictions[target_vehicle]
    # generate alternative goals
    all_goals = []
    timestep = 0.5
    t = T - 4 * timestep
    while t <= T + 4 * timestep:
        target_state = np.array(target.state_in(t)) + np.array(delta)
        goal_s = target_state[:3]
        goal_d = target_state[3:]
        goals = [(goal_s, goal_d, t)]
        for _ in range(N_SAMPLES):
            perturbed = perturb_goal(goal_s, goal_d)
            goals.append((perturbed[0], perturbed[1], t))
        all_goals += goals
        t += timestep
    
    # find best trajectory
    trajectories = []
    for goal in all_goals:
        s_goal, d_goal, t = goal
        s_coefficients = JMT(start_s, s_goal, t)
        d_coefficients = JMT(start_d, d_goal, t)
        trajectories.append(tuple([s_coefficients, d_coefficients, t]))
    
    best = min(trajectories, key=lambda tr: calculate_cost(tr, target_vehicle, delta, T, predictions, WEIGHTED_COST_FUNCTIONS))
    return best
    

def calculate_cost(trajectory, target_vehicle, delta, goal_t, predictions, cost_functions_with_weights ):
    cost = 0
    for cf, weight in cost_functions_with_weights:
        cost += weight * cf(trajectory, target_vehicle, delta, goal_t, predictions)
    return cost

def perturb_goal(goal_s, goal_d):
    new_s_goal = []
    for mu, sig in zip(goal_s, SIGMA_S):
        new_s_goal.append(random.gauss(mu, sig))

    new_d_goal = []
    for mu, sig in zip(goal_d, SIGMA_D):
        new_d_goal.append(random.gauss(mu, sig))
        
    return tuple([new_s_goal, new_d_goal])

def JMT(start, end, T):
    a_0, a_1, a_2 = start[0], start[1], start[2] / 2.0
    c_0 = a_0 + a_1 * T + a_2 * T**2
    c_1 = a_1 + a_2 * T
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
    alphas = np.concatenate([np.array([a_0, a_1, a_2]), a_3_4_5])
    return alphas