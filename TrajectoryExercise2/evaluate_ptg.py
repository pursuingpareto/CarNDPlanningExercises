#!/usr/bin/env python

from ptg import PTG
from helpers import Vehicle
# from cost_functions import *



def main():
	vehicle = Vehicle([0,10,0, 0,0,0])
	predictions = {0: vehicle}
	target = 0
	delta = [-5, 0, 0, 0, 0 ,0]
	start_s = [10, 10, 0]
	start_d = [4, 0, 0]
	T = 5.0
	best = PTG(start_s, start_d, target, delta, T, predictions)
	print 'best is {}'.format(best)
	# show_trajectory(best[0], best[1], best[2])

if __name__ == "__main__":
	main()