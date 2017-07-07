from math import sqrt, exp
# from matplotlib import pyplot as plt

class Vehicle(object):
    def __init__(self, start):
        self.start_state = start
    
    def state_in(self, t):
        s = self.start_state[:3]
        d = self.start_state[3:]
        state = [
            s[0] + (s[1] * t) + s[2] * t**2 / 2.0,
            s[1] + s[2] * t,
            s[2],
            d[0] + (d[1] * t) + d[2] * t**2 / 2.0,
            d[1] + d[2] * t,
            d[2],
        ]
        return state

def logistic(x):
    return 2.0 / (1 + exp(-x)) - 1.0

def to_equation(coefficients):
    def f(t):
        total = 0.0
        for i, c in enumerate(coefficients): 
            total += c * t ** i
        return total
    return f

def differentiate(coefficients):
    new_cos = []
    for deg, prev_co in enumerate(coefficients[1:]):
        new_cos.append((deg+1) * prev_co)
    return new_cos

def nearest_approach_to_any_vehicle(traj, vehicles):
    closest = 999999
    for v in vehicles.values():
        d = nearest_approach(traj,v)
        if d < closest:
            closest = d
    return closest

def nearest_approach(traj, vehicle):
    closest = 999999
    s_,d_,T = traj
    s = to_equation(s_)
    d = to_equation(d_)
    for i in range(100):
        t = float(i) / 100 * T
        cur_s = s(t)
        cur_d = d(t)
        targ_s, _, _, targ_d, _, _ = vehicle.state_in(t)
        dist = sqrt((cur_s-targ_s)**2 + (cur_d-targ_d)**2)
        if dist < closest:
            closest = dist
    return closest

# def show_trajectory(s_coeffs, d_coeffs, T, vehicle=None):
#     s = to_equation(s_coeffs)
#     d = to_equation(d_coeffs)
#     X = []
#     Y = []
#     if vehicle:
#         X2 = []
#         Y2 = []
#     t = 0
#     while t <= T:
#         X.append(s(t))
#         Y.append(d(t))
#         if vehicle:
#             s_, _, _, d_, _, _ = vehicle.state_in(t)
#             X2.append(s_)
#             Y2.append(d_)
#         t += 0.25
#     plt.scatter(X,Y)
#     if vehicle:
#         plt.scatter(X2, Y2)
#     plt.show()